from utilities import display
from random import randint
from timeit import default_timer as time
from queue import Queue
import numpy as np
import copy
import platform
import threading

if platform.system() == 'Linux':
    from backend import ADS1263

def DummyProducer(uiQueue: Queue, writerQueue: Queue, comm: Queue):
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
    t2 = time()
    productionRate = 5* 10**4

    ADC = [0]*10


    while True:
        
        # generate dummy data
        if platform.system() == 'Linux':
            pass
        else:
            for i in range(10): # generate dummy ADC data
                dataHolder["A"+str(i)] = randint(0, 1023)
        dataHolder["time"] = time()-t  # timestamp in seconds  
        dataHolder["ID"] = dataID
        

        # handle the UI queue
        if not uiQueue.full(): # if full then make some space and then put
            uiQueue.put_nowait(dict(dataHolder))
        else:
            try:
                if not uiQueue.empty(): # consumer is constantly consuming data so the state of uiQueue changes constantly
                    uiQueue.get_nowait()  # remove oldest data if queue is full
            except:
                pass # due to consumer existance the uiQueue.get_nowait() frequently produces an error
            uiQueue.put_nowait(dataHolder)

        # handle the writer queue
        if not writerQueue.full():
            writerQueue.put_nowait(dict(dataHolder))
        else:
            try:
                writerQueue.get_nowait()
            except:
                pass
            writerQueue.put_nowait(dict(dataHolder)) 

        dataID += 1

        # evaluate the CMD
        while True: # do while
            if not comm.empty():
                cmd = comm.get()

                if cmd == "EXIT":
                    print("producer Exit")
                    return

            if time()-t2 > 1/productionRate:
                break
        t2 = time()
        

        