import RPi.GPIO as GPIO
import dht11
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#Stepper motor pins
class Stepper:
    def __init__(self, pins, delay=0.002):
        self.pins = pins
        self.delay = delay

        #GPIO pins output
        for p in pins:
            GPIO.setup(p, GPIO.OUT)
            GPIO.output(p, 0)

        #Halv step sekvens
        self.sequence = [
            [1,0,0,0],
            [1,1,0,0],
            [0,1,0,0],
            [0,1,1,0],
            [0,0,1,0],
            [0,0,1,1],
            [0,0,0,1],
            [1,0,0,1]
        ]
    def step(self, steps, direction=1):
        #  når = 1 åbner vindue
        # når = -1 lukker vindue
        seq = self.sequence if direction == 1 else self.sequence[::-1]
        for _ in range(steps):
            for pattern in seq:
                for pin, val in zip(self.pins, pattern):
                    GPIO.output(pin, val)
                sleep(self.delay)
    
    def stop(self):
        for p in self.pins:
            GPIO.output(p, 0)

#Starter stepper
stepper = Stepper(pins=[18, 17, 16, 19])
#husk man kan skifte pins her___

def fan_setup():
    fan_pin = 23
    GPIO.setup(fan_pin, GPIO.OUT)
    GPIO.output(fan_pin, 0)

#Funktioner til vindue og blæser
window_open = False
fan_on = False

def open_window():
    print("Åbner vindue")
    #Note Her defineres steps for motor
    #200 steps = lille åbning
    #800 steps = mellem åbning
    #2000 steps = stop åbning
    #4096 steps = fuld rotation
    stepper.step(steps=1200, direction=1)
    stepper.stop()
    window_open = True

def close_window():
    print("Lukker vindue")
    stepper.step(steps=1200, direction=-1)
    stepper.stop()
    window_open = False

def turn_on_fan():
    print("Tænder blæser")
    GPIO.output(fan_pin, 1)
    fan_on = True

def turn_off_fan():
    print("Slukker blæser")
    GPIO.output(fan_pin, 0)
    fan_on = False

sensor = dht11.DHT11(pin=14)

while True:
    result = sensor.read() # Husk at vi lige skal rette navnet på variablen her, så den matcher dem der kommer fra
    # andre filer.
    if result.is_valid():
        temp = result.temperature
        hum = result.humidity
        print(f"Temperature: {temp:.1f} C")
        print(f"Humidity: {hum:.1f} %") 
        
        if temp > 24: #or hum > 60:
            print("For varmt, starter blæser")
            turn_on_fan()
        
        elif temp >= 30 && hum >= 60:
            print("Abnormale forhold, åbner vindue og tænder blæser.")
            open_window()
            turn_on_fan()
            
        elif hum >= 60:
            print("Høj fugtighed, åbner vindue.")
            open_window()
            
        elif smoke_detected = True:
            print("ADVARSEL: RØG REGISTRERET --- LUKKER VINDUE OG SLUKKER BLÆSER ØJEBLIKKELIGT")
            close_window()
            turn_off_fan()
            
        elif temp < 24:
            print("Acceptabel temperatur opnået, slukker blæser.")
            turn_off_fan()
            
        elif hum < 60:
            print("Acceptabel luftfugtighed opnået, lukker vindue.")
            close_window()
            
        elif temp < 30 && hum < 60:
            print("Abnormale forhold afsluttet, lukker vindue og slukker blæser.")
            close_window()
            turn_off_fan()
    else:
        print("Sensorfejl:", result.error_code)
    sleep(2)
