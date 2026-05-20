import RPi.GPIO as GPIO
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
        # når = 1 åbner vindue
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
stepper = Stepper(pins=[5, 17, 4, 15])
#husk man kan skifte pins her___
#fan_pin = 9

def fan_setup(fan_pin):
    GPIO.setup(fan_pin, GPIO.OUT)
    GPIO.output(fan_pin, 0)

#Funktioner til vindue og blæser

def open_window():
    # Note Her defineres steps for motor
    # 200 steps = lille åbning
    # 800 steps = mellem åbning
    # 2000 steps = stop åbning
    # 4096 steps = fuld rotation
    stepper.step(steps=1200, direction=1)
    stepper.stop()
    #stop_window()

def close_window():
    stepper.step(steps=1200, direction=-1)
    stepper.stop()
    #stop_window()

def turn_on_fan(fan_pin):
    GPIO.output(fan_pin, 1)

def turn_off_fan(fan_pin):
    #print("Slukker blæser")
    GPIO.output(fan_pin, 0)

#                    Skal vi bare bruge ultralydssensor???
#def stop_window():
    #global window_stop
    #stepper.stop()
#                    Fixet ved at begrænse antallet af temp og hum målinger.

def janitor():
    GPIO.cleanup()



#while True:
    #hum, temp = get_humTemp()
    #result = humTemp.read() # Husk at vi lige skal rette navnet på variablen her, så den matcher dem der kommer fra
    # andre filer.
    #if result.is_valid():
        #temp = result.temperature
        #hum = result.humidity
        #print(f"Temperature: {temp:.1f} C")
        #print(f"Humidity: {hum:.1f} %") 
        
        #if smoke_detected == True:
            #print("ADVARSEL: RØG REGISTRERET --- LUKKER VINDUE OG SLUKKER BLÆSER!")
            #close_window()
            #turn_off_fan()
    #else:
    # Blæser
    #if temp > 25 and fan_on == False:
    #    print("Høj temperatur, tænder blæser.")
    #    turn_on_fan()
    #if temp < 25 and fan_on == True:
    #    print("Temperatur acceptabel, slukker blæser.")
    #    turn_off_fan()
    #    sleep(2)
    # Vindue 
    #if hum >= 60 and window_open == False:
    #    print("Høj fugtighed, åbner vindue.")
    #    open_window()
    #    sleep(3)
    #elif window_open == True and hum < 60:
    #    print("Acceptabel luftfugtighed opnået, lukker vindue.")
    #    close_window()
    #    sleep(3)
    #    stop_window()

    # Status Besked
    #if temp <= 25 and window_stop == True and hum < 60:
    #    print("Forhold er optimale, ingen handling påkrævet - stopper blæser og vinduekontrol.")
    #    turn_off_fan()
    #    sleep(2)
    #else:
        #print("Sensorfejl:", result.error_code)
    #    sleep(2)
#sleep(2)
