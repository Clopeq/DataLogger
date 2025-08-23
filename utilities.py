import logging
import threading
import multiprocessing
import logging
logging.basicConfig(format='%(levelname)s - %(asctime)s.%(msecs)03d: %(message)s',datefmt='%H:%M:%S', level=logging.DEBUG)

def display(msg):
    threadname = threading.current_thread().name
    processname = multiprocessing.current_process().name
    logging.info('%s\\%s: %s', processname, threadname, msg)


