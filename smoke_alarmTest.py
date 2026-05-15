# Denne fil er direkte taget fra Joy-ITs manual til røgsensoren (Sen-MQ).
# Den skal 100 % rettes til, men nu har vi noget at prøve af.
from time import sleep
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from gpiozero import DigitalInputDevice
# Set up the digital input device for the gas sensor
gas_sensor = DigitalInputDevice(17)
# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
ads.gain = 2/3
# Create single-ended input on channel
chan0 = AnalogIn(ads, ADS.P0)
try:
   while True:
       print("{:>5.3f}".format(chan0.voltage))
       if not gas_sensor.value: # True when the sensor is triggered
      # (typically active low)
           print("Warning: Threshold exceeded!!!")           
        sleep(1)
except KeyboardInterrupt:
    pass  # No need for cleanup, gpiozero handles it automatically
