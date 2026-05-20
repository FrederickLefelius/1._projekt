import sqlite3
import os
from datetime import datetime
from random import randint
from time import sleep


def Data_dht11():
    while True:
        query = """INSERT INTO DHT_11 (Dato, Temp, Hum) VALUES (?, ?, ?)"""
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        data = (now, randint(0, 30), randint(30, 80))
        conn = None
        try:
            conn = sqlite3.connect("dht11_data.db")
            cur = conn.cursor()
            cur.execute(query, data)
            conn.commit()
        except sqlite3.Error as sql_e:
            print(f"database error: {sql_e}")
            if conn:
                conn.rollback()
        except Exception as e:
            print(f"error: {e}")
        finally:
            if conn:
                conn.close()
            sleep(1)
Data_dht11()