"""
Flask backend — Smoke Alarm System
===================================
Run with:  python app.py
Then open: http://localhost:5000

API endpoints:
  GET  /api/alarm    → ESP32 polls this to know if it should beep
  POST /api/alarm    → dashboard sends {"alarm": true/false}
  POST /api/battery  → ESP32 sends {"battery": 85}
  GET  /api/status   → dashboard polls for current state
"""

from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

# Simple shared state — good enough for a single-device setup
state = {
    "alarm":     False,   # True = alarm active, ESP32 will beep
    "battery":   None,    # Last battery % received from ESP32 (0-100)
    "last_seen": None,    # Timestamp of last ESP32 contact
}


# ── Serve the dashboard ────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


# ── ESP32 polls this every 2s ──────────────────────────────

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


if __name__ == "__main__":
    # host="0.0.0.0" makes Flask reachable from other devices on your LAN
    # (the ESP32 needs to reach this server)
    app.run(host="0.0.0.0", port=5000, debug=True)
