# Denne fil eksistere kun som en backup af løsningens pir sensor funktion.

import RPi.GPIO as GPIO
import time
 
# Opæstning af anvendt Pin
PIR_PIN = 27  # På Educaboard
 
# Opsætning af GPIO
GPIO.setmode(GPIO.BCM) ### Denne linje indstiller pin nummereringssystemet, som der anvendes i koden.
                       For eksempel bruges der i dette tilfælde BCM, som står for Broadcom - dette betyder
                       at proccessorens interne nummereringssystem anvendes. Man kunne også bruge  BROAD,
                       som bare refererer til pins efter deres fysiske position på f.eks. Educaboard ###
GPIO.setup(PIR_PIN, GPIO.IN)
 
print("PIR Sensor klar! Afventer bevægelse.")
 
try:
    while True:
        if GPIO.input(PIR_PIN):
            print("Bevægelse påvist!")
        else:
            print("Intet bevægelse.")
        time.sleep(0.5)
 
except KeyboardInterrupt:
    print("\nLukker programmet.")
 
finally:
    GPIO.cleanup()
