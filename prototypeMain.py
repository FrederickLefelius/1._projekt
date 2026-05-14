from motor import open_window, close_window, turn_on_fan, turn_off_fan
from humTemp import get_humTemp
from netConnect import do_connect
from time import sleep
import RPi.GPIO as GPIO
import time

while True:
  try:
    do_connect()

    # Indsæt flask-kode imellem disse 2 kommentarer
    
    # Indsæt flask-kode imellem disse 2 kommentarer
    
    
    if smoke_detected = True:
      print("ADVARSEL: RØG REGISTRERET --- LUKKER VINDUE OG SLUKKER BLÆSER!")
      close_window()
      turn_off_fan()
      smoke_alarm()
    else:
      
            
  except KeyboardInterrupt:
      print("Program afbrudt, lukker ned.")
  except Exception as e:
      print(f"Fejl opstod: {e}")
  finally:
GPIO.cleanup()
