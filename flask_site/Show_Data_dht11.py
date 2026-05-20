import sqlite3
import os
from datetime import datetime
from time import sleep
import RPi.GPIO as GPIO
import dht11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dht11_data.db")


def get_humTemp():
    """Read temperature and humidity from the DHT11 sensor on pin 14."""
    dhtData = dht11.DHT11(pin=14)
    humTemp = dhtData.read()
    if humTemp.is_valid():
        temp = humTemp.temperature
        hum  = humTemp.humidity
        print(f"Temperatur: {temp}  Fugtighed: {hum}")
        return hum, temp
    else:
        print("Input fra DHT11 ikke valideret, prøver igen senere.")
        return None, None


def init_db():
    """Create the DHT_11 table if it doesn't already exist."""
    conn = None
    try:
        conn = sqlite3.connect(DB)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS DHT_11 (
                Dato TEXT,
                Temp REAL,
                Hum  REAL
            )
        """)
        conn.commit()
        print("Database initialised.")
    except sqlite3.Error as sql_e:
        print(f"Database init error: {sql_e}")
    finally:
        if conn:
            conn.close()


def Data_dht11(socketio):
    """
    Background thread: reads the DHT11 sensor every 5 seconds,
    inserts the reading into the DB, and emits it to all WebSocket clients.
    Skips the insert if the sensor reading is invalid.
    """
    init_db()

    while True:
        conn = None
        try:
            hum, temp = get_humTemp()

            if temp is None or hum is None:
                print("Skipping insert due to invalid sensor reading.")
            else:
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                conn = sqlite3.connect(DB)
                conn.execute(
                    "INSERT INTO DHT_11 (Dato, Temp, Hum) VALUES (?, ?, ?)",
                    (now, temp, hum)
                )
                conn.commit()
                print(f"Inserted: {now}  Temp={temp}  Hum={hum}")

                socketio.emit('new_reading', {
                    'dato': now,
                    'temp': temp,
                    'hum':  hum
                })

        except sqlite3.Error as sql_e:
            print(f"Database error: {sql_e}")
            if conn:
                conn.rollback()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if conn:
                conn.close()

        sleep(5)


def get_data(limit=10):
    """Fetch the most recent `limit` rows from the database, oldest first."""
    conn = None
    try:
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute(
            "SELECT Dato, Temp, Hum FROM DHT_11 ORDER BY Dato DESC LIMIT ?",
            (limit,)
        )
        rows = cur.fetchall()
        rows.reverse()
        dato = [r[0] for r in rows]
        temp = [r[1] for r in rows]
        hum  = [r[2] for r in rows]
        return dato, temp, hum
    except sqlite3.Error as sql_e:
        print(f"Database error: {sql_e}")
        return [], [], []
    finally:
        if conn:
            conn.close()