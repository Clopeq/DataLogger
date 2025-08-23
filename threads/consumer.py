from utilities import display
from timeit import default_timer as time
from queue import Queue
from PySide6.QtWidgets import QApplication, QPushButton, QLabel, QLineEdit
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QObject, Signal
import UIutil

def UIconsumer(sensorData: Queue, window, comm: Queue):
    """
    Updates the label with the first ADC value from the data dictionary if available, otherwise displays 'No data'.

    Parameters:
        data (dict): Dictionary containing ADC data under the 'ADC' key.
        label: UI label object with a setText(str) method.
    """

    data = {} # container for the queue data
    refreshrate = 8 
    t = time()
    cmd = None

    tare_button = window.findChild(QPushButton, "tareButton")
    title_label = window.findChild(QLabel, "titleLabel")

    if tare_button is not None:
        tare_button.clicked.connect(lambda: tareClick(producerCMD))
    else:
        print("Error: 'pushButton' not found in the UI.")

    while True:

        if not sensorData.empty():
            data = sensorData.get() # sensorData queue is very small (max 3 elements) and its contents are being overriten constantly with fresh new data by the producer so even if the data is being collected from the oldest element in the queue at reduced refreshrate the dataitself is propably few ms old at most depending on the production rate
        else:
            continue # no new data available

        try: 
            title_label.setText(str(data["A0"]) + " N")
        except:     # if there is no data being collected at the initialization the try block will produce an error
            print("UI consumer: No data")
            title_label.setText("No data")

        
        while True: # do while to ensure the cmd communication protocol is being checked at least once
            if not comm.empty():
                cmd = comm.get()
                if cmd == "EXIT":
                    return
            
            if time()-t > 1/refreshrate: # do-while argument
                break
        t = time()
