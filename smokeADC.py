from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15
import board 
import busio 
from time import sleep 


i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115(i2c)


kanal = AnalogIn(ads, ads1x15.Pin.A0)


def smoke_check():
    smoke_data_adc = kanal.value
    if smoke_data_adc > 10000:
        print("ADVARSEL: RØG REGISTRERET --- LUKKER VINDUE OG SLUKKER BLÆSER!")
        smoke_detected = True
    else:
        smoke_detected = False
    return smoke_detected
