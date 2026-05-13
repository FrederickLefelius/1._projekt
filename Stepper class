from machine import Pin
from time import sleep

class Stepper:
    def __init__(self, pins, delay=0.01):
        self.pins = [Pin(p, Pin.OUT) for p in pins]
        self.delay = delay

        self.sequence = [
            [1,0,0,0],
            [0,1,0,0],
            [0,0,1,0],
            [0,0,0,1]
        ]

    def step_once(self, direction=1):
        seq = self.sequence if direction == 1 else self.sequence[::-1]

        for step in seq:
            for i in range(4):
                self.pins[i].value(step[i])
            sleep(self.delay)

    def stop(self):
        for p in self.pins:
            p.value(0)
