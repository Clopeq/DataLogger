
import backend.ADS1263 as ADC
import time
import eel
import os
import threading

DEV_MODE = True

eel.init('app')

if DEV_MODE:
    mode=None
else:
    mode="netsurf"

print("Starting the browser...")
os.popen('netsurf http://DAQ:8080')

print("Starting the server...")
eel.start('index.html', size=(1024,600), mode=mode, host="0.0.0.0", port=8080, block=False)

#ADC1 = ADC.ADS1263('GAIN_1', '14400SPS')

#def read_adc_loop():
#    while True:
#        print("\033[H\033[J", end="")  # console clear
#        print("A0: %f" % ADC1.read(0))
#        time.sleep(0.01)

# Run ADC loop in a separate thread
#adc_thread = threading.Thread(target=read_adc_loop)
#adc_thread.daemon = True
#adc_thread.start()

# Keep the main thread alive so Eel stays running
while True:
    time.sleep(1)
