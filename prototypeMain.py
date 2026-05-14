from motor import open_window, close_window, turn_on_fan, turn_off_fan, fan_setup
from humTemp import get_humTemp
from netConnect import do_connect
from pirsensor import pir_setup, read_pir
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
pir_setup()
fan_setup()

smoke_detected = None

do_connect()

try:
  while True:
    # Indsæt flask-kode imellem disse 2 kommentarer - skal måske op under do_connect()
    
    # Indsæt flask-kode imellem disse 2 kommentarer - skal måske op under do_connect()
    
    hum, temp = get_humTemp()
    
    if smoke_detected == True:
      print("ADVARSEL: RØG REGISTRERET --- LUKKER VINDUE OG SLUKKER BLÆSER!")
      close_window()
      turn_off_fan()
      #smoke_alarm()
    else:
      if temp >= 30 and hum >= 70:
        print("Abnormale forhold, åbner vindue og tænder blæser.")
        open_window()
        turn_on_fan()
        
      elif hum >= 60:
        print("Høj fugtighed, åbner vindue.")
        open_window()
            
      elif hum < 60 and temp < 30:
        print("Abnormale forhold afsluttet, lukker vindue og slukker blæser.")
        close_window()
        turn_off_fan()
        
      elif hum < 60:
        print("Acceptabel luftfugtighed opnået, lukker vindue.")
        close_window()
        
      else:
        print("Der opstod en fejl.")
    
except KeyboardInterrupt:
    print("Program afbrudt, lukker ned.")
except Exception as e:
    print(f"Fejl opstod: {e}")
finally:
  GPIO.cleanup()
