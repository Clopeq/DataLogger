from backend import ADS1263
from time import time

ADC = ADS1263.ADS1263('GAIN_1', '14400SPS', ref=5.03)

channels = [0,1]
string = ""

t = time()
while time()-t < 5:
    for ch in channels:
        string += f"A{ch}: {ADC.read(ch)} | "
    print(string[:-2])
    print("\n")