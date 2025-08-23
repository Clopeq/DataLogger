import logging
import threading
import multiprocessing
import logging
logging.basicConfig(format='%(levelname)s - %(asctime)s.%(msecs)03d: %(message)s',datefmt='%H:%M:%S', level=logging.DEBUG)

def display(msg):
    threadname = threading.current_thread().name
    processname = multiprocessing.current_process().name
    logging.info('%s\\%s: %s', processname, threadname, msg)

def dset_append(dataset, data):
    """
        appends a list to 1D dataset
    """

    expanded_dataset = dataset

    # TODO: Check the shape of the dataset
    # TODO: Check the shape of the list

    size = expanded_dataset.size
    expanded_dataset.resize( (size+len(data),) )
    expanded_dataset[size: (size+len(data))] = data

    return expanded_dataset
