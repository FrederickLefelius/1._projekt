from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15
import board 
import busio 
from time import sleep 


i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115(i2c)


kanal = AnalogIn(ads, ads1x15.Pin.A0)

while True:
    print("Røgniveau: ", "ADC:", kanal.value,"VOLT:", kanal.voltage)
    if kanal.value > 10000:
        print("Røgniveau er for højt!")
    else: 
        print("røgniveau er stabilt")
    sleep(0.5)

        


    


