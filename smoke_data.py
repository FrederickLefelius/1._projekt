from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15
import board 
import busio 
from time import sleep 


i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115(i2c)


kanal = AnalogIn(ads, ads1x15.Pin.A0)


def get_smoke_adc():
    smoke_data_adc = kanal.value
    if kanal.value > 10000:
        print("Røgniveau er for højt")
    else:
        print("RØGNIVEAU ADC:", kanal.value)
        return kanal.value
    
def get_smoke_voltage():
    smoke_data_voltage = kanal.voltage
    if kanal.voltage > 5.0:
        print("Røgniveau i VOLT er for høj")
        print(kanal.voltage)
        return kanal.voltage
    else:
        print("RØGNIVEAU I VOLT:", kanal.voltage)
        return kanal.voltage


        


    


