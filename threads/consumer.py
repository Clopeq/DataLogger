from utilities import display
from timeit import default_timer as time
from queue import Queue

def UIconsumer(sensorData: Queue, label, comm: Queue):
    """
    Updates the label with the first ADC value from the data dictionary if available, otherwise displays 'No data'.

    Parameters:
        data (dict): Dictionary containing ADC data under the 'ADC' key.
        label: UI label object with a setText(str) method.
    """

    data = {} # container for the queue data
    refreshrate = 100 
    t = time()
    cmd = None

    while True:

        if not sensorData.empty():
            data = sensorData.get() # sensorData queue is very small (max 3 elements) and its contents are being overriten constantly with fresh new data by the producer so even if the data is being collected from the oldest element in the queue at reduced refreshrate the dataitself is propably few ms old at most depending on the production rate
        else:
            continue # no new data available

        try: 
            label.setText(str(data["A0"]) + " " + str(data["ID"]) + " " + str(data["time"]))
        except:     # if there is no data being collected at the initialization the try block will produce an error
            print("UI consumer: No data")
            label.setText("No data")

        
        while True: # do while to ensure the cmd communication protocol is being checked at least once
            if not comm.empty():
                cmd = comm.get()
                if cmd == "EXIT":
                    return
            
            if time()-t > 1/refreshrate: # do-while argument
                break
        t = time()
