import board
import busio
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15 import ads1x15
import sqlite3
import os
from datetime import datetime
from time import sleep
 
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dht11_data.db")
SMOKE_THRESHOLD = 10000
 
 
def init_smoke_db():
    """Create the SMOKE table if it doesn't already exist."""
    conn = None
    try:
        conn = sqlite3.connect(DB)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS SMOKE (
                Dato  TEXT,
                Value INTEGER,
                Volt  REAL,
                Alert INTEGER  -- 1 if above threshold, 0 if stable
            )
        """)
        conn.commit()
        print("Smoke table initialised.")
    except sqlite3.Error as e:
        print(f"Smoke DB init error: {e}")
    finally:
        if conn:
            conn.close()
 
 
def stream_smoke(socketio):
    """
    Background thread: reads the smoke sensor every 0.5s,
    inserts into DB every 5s, and emits live readings to WebSocket clients.
    """
    init_smoke_db()
 
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS1115(i2c)
    kanal = AnalogIn(ads, ads1x15.Pin.A0)
 
    last_insert = 0
 
    while True:
        try:
            value   = kanal.value
            voltage = kanal.voltage
            alert   = value > SMOKE_THRESHOLD
            now     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
            status = "Røgniveau er for højt!" if alert else "Røgniveau er stabilt"
            print(f"Røgniveau — ADC: {value}  VOLT: {voltage:.3f}  {status}")
 
            # Emit live reading to all connected clients
            socketio.emit('smoke_reading', {
                'dato':    now,
                'value':   value,
                'voltage': round(voltage, 3),
                'alert':   alert,
                'status':  status
            })
 
            # Insert into DB every 5 seconds
            last_insert += 0.5
            if last_insert >= 5:
                last_insert = 0
                conn = None
                try:
                    conn = sqlite3.connect(DB)
                    conn.execute(
                        "INSERT INTO SMOKE (Dato, Value, Volt, Alert) VALUES (?, ?, ?, ?)",
                        (now, value, voltage, int(alert))
                    )
                    conn.commit()
                    print(f"Smoke inserted: {now}  ADC={value}  Volt={voltage:.3f}  Alert={alert}")
                except sqlite3.Error as e:
                    print(f"Smoke DB error: {e}")
                    if conn:
                        conn.rollback()
                finally:
                    if conn:
                        conn.close()
 
        except Exception as e:
            print(f"Smoke sensor error: {e}")
 
        sleep(0.5)