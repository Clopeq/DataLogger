from backend import ADS1263
from time import time

ADC = ADS1263('GAIN_!', '14400SPS', ref=5.03)

t = time()
while time()-t < 5:
    print("A0: ", ADC.read(0))