from motor import open_window, close_window, turn_on_blæser, turn_off_blæser
from humTemp import get_humTemp
from netConnect import do_connect
from time import sleep
import RPi.GPIO as GPIO
import time

while True:
  try:
    if smoke_detected = True:
      
  except KeyboardInterrupt:
      print("Program afbrudt, lukker ned.")
  except Exception as e:
      print(f"Fejl opstod: {e}")
  finally:
GPIO.cleanup()
