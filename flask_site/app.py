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