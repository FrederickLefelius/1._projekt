import RPi.GPIO as GPIO
import dht11
from time import sleep

# Opsætning af gpio 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# Oprettelse af funktion til temperatur og fugtighedsmåling
def get_humTemp():
    dhtData = dht11.DHT11(pin=14)

    humTemp = dhtData.read()

    if humTemp.is_valid():
        temp = humTemp.temperature
        hum = humTemp.humidity
        print(f"Temperatur: ", temp)
        print("Fugtighed: ", hum)
        return hum, temp
    else:
        print("Input fra DHT11 ikke valideret, prøv igen.")
