from utilities import display
from random import randint
from time import time

import threading

def DummyProducer(uiQueue, saveQueue, comm):
    """
        Producer which generates random data for testing on PC.

        data: Dictionary to store current data.
        queue: Queue to store produced data for saving
        comm: communication queue to signal the producer
        data_lock: threading.Lock() instance for synchronizing access to data
    """

    dataHolder = {}
    dataID = 0
    t = time()

    ADC = [0]*10


    while True:
        
        # generate dummy data
        for i in range(10):
            ADC[i] = randint(0, 100)

        dataHolder["time"] = time()-t  # timestamp in seconds  
        dataHolder["ID"] = dataID
        dataHolder["ADC"] = ADC

        # handle the UI queue
        if not uiQueue.full():
            uiQueue.put_nowait(dataHolder)
        else:
            uiQueue.get_nowait()  # remove oldest data if queue is full
            uiQueue.put_nowait(dataHolder)

        # handle the saving queue
        if not saveQueue.full():
            saveQueue.put_nowait(dataHolder)
        else:
            saveQueue.get_nowait()
            saveQueue.put_nowait(dataHolder) 

        dataID += 1
        while time()-t < 1/50000:
            pass