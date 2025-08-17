import backend.ADS1263 as ADC
import time

REF = 5.03

ADC1 = ADC.ADS1263('GAIN_1', '14400SPS')

while True:
    print("\033[H\033[J", end="") # consol clear
    print("A0: %f" % ADC1.read(0))
    time.sleep(0.01)

