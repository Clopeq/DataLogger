import backend.ADS1263 as ADC
import time

REF = 5.03

ADC1 = ADC.ADS1263('GAIN_1', '14400SPS')

while True:
    print("\033[H\033[J", end="")
    print("A0: %f" % ADC1.GetChannalValue(0))
    print("A1: %f" % ADC1.GetChannalValue(1))
    print("A2: %f" % ADC1.GetChannalValue(2))
    print("A3: %f" % ADC1.GetChannalValue(3))
    print("A4: %f" % ADC1.GetChannalValue(4))
    print("A5: %f" % ADC1.GetChannalValue(5))
    print("A6: %f" % ADC1.GetChannalValue(6))
    print("A7: %f" % ADC1.GetChannalValue(7))
    time.sleep(0.1)

