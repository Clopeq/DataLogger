from utilities import display
import time

def Consumer(queue, finished, label):
    counter = 0
    while True:
        if not queue.empty():
            v = queue.get()
            display(f"Consuming {counter}: {v}")
            label.setText(str(v))
            counter += 1
            time.sleep(0.1)
        else:
            if not finished.empty():
                q = finished.get()
                if q is True:
                    break
        
    display("Consumer finished!")