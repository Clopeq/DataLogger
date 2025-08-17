from utilities import display
from random import randint

def DummyProducer(queue, finished, max=-1):
    finished.put(False)
    i = 0
    while (i < max) or (max==-1): # max=-1 infinite loop
        v = randint(0, 100)
        queue.put_nowait(v)
        display(f"Dummy produced {i}: {v}")
        i += 1
    finished.put(True)
    display("Dummy producer finished!")