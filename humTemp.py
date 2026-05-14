import RPi.GPIO as GPIO
import dht11
from time import sleep

GPIO.setwarnings(False) # Ignorerer advarsler fra GPIO om allerede anvendte kanaler, og kører programmet
                        # uden at printe dem
GPIO.setmode(GPIO.BCM)

# Oprettelse af funktion til temperatur og fugtighedsmåling
def get_humTemp():
    dhtData = dht11.DHT11(pin=14)
    humTemp = dhtData.read()

    if humTemp.is_valid():
        temp = humTemp.temperature
        hum = humTemp.humidity
        print("Temperatur: ", temp)
        print("Fugtighed: ", hum)
        return hum, temp
    else:
        print("Input fra DHT11 ikke valideret, prøver igen senere.")
        return None, None # Der returneres None, None hvis dataaflæsningen fejler, så programmet staid køres.
        
# Skriv "hum, temp = get_humTemp()" i main filen når disse skal kaldes og defineres. Husk at alle sensorfiler
# osv. skal importeres til main.py, når den laves. GPIO.cleanup() skal desuden også kaldes i en "finally" i
# main.py. Den er derfor ikke til stede her.
