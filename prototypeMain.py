from motor import open_window, close_window, turn_on_fan, turn_off_fan, fan_setup
from humTemp import get_humTemp
from netConnect import do_connect
from pirsensor import pir_setup, read_pir
from time import sleep, time
from camera import Camera
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
pir_setup()
fan_setup()
do_connect()
smoke_detected = None

horse_down_counter = 0
horse_was_laying = False
camera_active = False
motion_timer = None

try:
  while True:
    # Indsæt flask-kode imellem disse 2 kommentarer - skal måske op under do_connect()
    
    # Indsæt flask-kode imellem disse 2 kommentarer - skal måske op under do_connect()
    hum, temp = get_humTemp()
    #hum = int(hum)
    #temp = int(temp)
    
    if smoke_detected == True:
    print("ADVARSEL: RØG REGISTRERET --- LUKKER VINDUE OG SLUKKER BLÆSER!")
    close_window()
    turn_off_fan()
    # smoke_alarm()

else:
    # --- Blæser kontrol ---
    if temp >= 24 and fan_on == False:
        print("Høj temperatur, tænder blæser.")
        turn_on_fan()
    elif temp < 24 and fan_on == True:
        print("Temperatur acceptabel, slukker blæser.")
        turn_off_fan()

    # --- Vindue kontrol ---
    if hum >= 60 and window_open == False:
        print("Høj fugtighed, åbner vindue.")
        open_window()
    elif hum < 60 and window_open == True:
        print("Acceptabel luftfugtighed opnået, lukker vindue.")
        close_window()

    # --- Status Besked ---
    if fan_on == False and window_open == False and temp < 24 and hum < 60:
        print("Forhold er optimale, ingen handling påkrævet.")
      
# Jeg har forsøgt at planlægge fremad ift. at der stadig er noget kode vi mangler - som f.eks. Yolo og kamera.
# Derfor har jeg sørget for, at alle kommentarer efter dette punkt som har 3 hashtags i starten, refererer til
# kode/kommandoer, som skal indtastes når vi har dem. Når vi har koden, slettes de 3 hashtags og koden erstattes.
# Jeg tror måske at det er en god ide med nogle klasser alligevel.
      motion = read_pir()
      if motion:
        motion_timer = time()  # Nulstil timer hver gang bevægelse registreres
        if not camera_active:
          print("Bevægelse registreret — starter kamera.")
          ### camera = start_camera()
          camera_active = True

            if camera_active:
                if time() - motion_timer < 10:
                  ###frame = camera.get_frame()
                  ###yolo_result = yolo_model.analyse(frame)
                    if yolo_result == 'laying':
                        if not horse_was_laying:
                            horse_down_counter += 1
                      # Nu har vi en tæller på, så vi ved hvor mange gange hestene ligger sig ned. 
                      # Da tælleren skal indtastes i en SQL database/tabel, som kommer til at foregå
                      # gennem flask, kan jeg ikke lige finde ud af om denne hører til her - men den 
                      # hører i hvert fald til i main.py, hvilket hele flask koden også gør. 
                        horse_was_laying = True
                    else:
                        horse_was_laying = False
                else:
                    print("Ingen bevægelse i 10 sekunder — slukker kamera.")
                    ### camera.stop()
                    camera_active = False
                    motion_timer = None
        sleep(0.5)  #  Denne sættes til 0.5 sekunder for at få repsons fra pir sensoren hurtigere.


except KeyboardInterrupt:
    print("Program afbrudt, lukker ned.")
except Exception as e:
    print(f"Fejl opstod: {e}")
finally:
  GPIO.cleanup() # Yderst nødvendig, da den clearer alle GPIO setuppene til næste gang programmet køres.
