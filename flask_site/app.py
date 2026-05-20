from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import base64
from io import BytesIO
from matplotlib.figure import Figure
from Show_Data_dht11 import get_data, Data_dht11
from Camera import stream_camera
from Smoke import stream_smoke
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app)
# Simple shared state — good enough for a single-device setup
state = {
    "alarm":     False,   # True = alarm active, ESP32 will beep
    "battery":   None,    # Last battery % received from ESP32 (0-100)
    "last_seen": None,    # Timestamp of last ESP32 contact
}

# --- Chart helpers ---

def generate_chart(x_data, y_data, bottom=0.3):
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=bottom)
    ax.tick_params(axis='x', rotation=45)
    ax.plot(x_data, y_data)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    return base64.b64encode(buf.getbuffer()).decode("ascii")

def get_charts():
    dato, temp, hum = get_data(10)
    return {
        'temp_chart': generate_chart(dato, temp, bottom=0.3),
        'hum_chart':  generate_chart(dato, hum,  bottom=0.4)
    }


# --- Routes ---

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/yolo/")
def yolo():
    return render_template("yolo.html")

@app.route("/målinger/")
def målinger():
    return render_template("målinger.html")

@app.route("/brand_alarm/")
def brand_alarm():
    return render_template("brand_alarm.html")

@app.route("/index/")
def index():
    return render_template("index.html")


@app.route("/api/alarm", methods=["GET"])
def get_alarm():
    state["last_seen"] = time.time()
    return jsonify({"alarm": state["alarm"]})


# ── Dashboard triggers or clears the alarm ─────────────────

@app.route("/api/alarm", methods=["POST"])
def set_alarm():
    data = request.get_json()
    state["alarm"] = bool(data.get("alarm", False))
    print(f"[ALARM] {'ON' if state['alarm'] else 'OFF'}")
    return jsonify({"ok": True, "alarm": state["alarm"]})


# ── ESP32 posts battery % every 10s ───────────────────────

@app.route("/api/battery", methods=["POST"])
def receive_battery():
    data = request.get_json()
    pct  = int(data.get("battery", 0))
    pct  = max(0, min(100, pct))          # clamp to 0-100
    state["battery"]   = pct
    state["last_seen"] = time.time()
    print(f"[BATTERY] {pct}%")
    return jsonify({"ok": True})


# ── Dashboard polls this every 3s ──────────────────────────

@app.route("/api/status", methods=["GET"])
def get_status():
    # Consider ESP32 "online" if it contacted us within the last 15 seconds
    online = (
        state["last_seen"] is not None and
        (time.time() - state["last_seen"]) < 15
    )
    return jsonify({
        "alarm":   state["alarm"],
        "battery": state["battery"],
        "online":  online,
    })
# --- SocketIO events ---

@socketio.on('connect')
def on_connect():
    emit('sensor_update', get_charts())

@socketio.on('request_update')
def on_request_update():
    emit('sensor_update', get_charts())


# --- Entry point ---

if __name__ == '__main__':
    print("Starting sensor thread...")
    threading.Thread(target=Data_dht11,args=(socketio,), daemon=True).start()

    print("Starting camera thread...")
    threading.Thread(target=stream_camera,args=(socketio,), daemon=True).start()

    print("Starting smoke thread...")
    threading.Thread(target=stream_smoke,args=(socketio,), daemon=True).start()

    print("All threads started.")
    socketio.run(app, host="0.0.0.0", debug=False)