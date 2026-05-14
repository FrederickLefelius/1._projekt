from motor import open_window, close_window, turn_on_fan, turn_off_fan
from humTemp import get_humTemp
from netConnect import do_connect
from pirsensor import pir_setup
from time import sleep
import RPi.GPIO as GPIO
import time

while True:
  try:
    do_connect()
  
    # Indsæt flask-kode imellem disse 2 kommentarer
    
    # Indsæt flask-kode imellem disse 2 kommentarer
    
    get_humTemp()
    
    if smoke_detected = True:
      print("ADVARSEL: RØG REGISTRERET --- LUKKER VINDUE OG SLUKKER BLÆSER!")
      close_window()
      turn_off_fan()
      smoke_alarm()
    else:
      if hum >= 60:
        print("Høj fugtighed, åbner vindue.")
        open_window()
        
      elif temp >= 30 && hum >= 60:
        print("Abnormale forhold, åbner vindue og tænder blæser.")
        open_window()
        turn_on_fan()
            
      elif hum < 60:
        print("Acceptabel luftfugtighed opnået, lukker vindue.")
        close_window()
            
      elif temp < 30 && hum < 60:
        print("Abnormale forhold afsluttet, lukker vindue og slukker blæser.")
        close_window()
        turn_off_fan()
      else:
        print("Sensorfejl:", result.error_code)
  
  
  except KeyboardInterrupt:
      print("Program afbrudt, lukker ned.")
  except Exception as e:
      print(f"Fejl opstod: {e}")
finally:
  GPIO.cleanup()
