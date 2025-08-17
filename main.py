
import backend.ADS1263 as ADC
import time
import eel
import os
import threading

DEV_MODE = False

eel.init('app')

if DEV_MODE:
    mode=None
else:
    mode="netsurf"

#print("Starting the browser...")
#os.popen('netsurf http://DAQ:8080')

def web_server():
    print("Starting the application...")
    eel.start('index.html', size=(1024,600), mode=mode, host="0.0.0.0", port=8000)

# Run ADC loop in a separate thread
app_thread = threading.Thread(target=web_server)
app_thread.daemon = True
app_thread.start()


# main loop
ADC1 = ADC.ADS1263('GAIN_1', '14400SPS')

while True:
    print("\033[H\033[J", end="")  # console clear
    print("A0: %f" % ADC1.read(0))
    time.sleep(0.01)
