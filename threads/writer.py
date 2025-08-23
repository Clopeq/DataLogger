import time
import h5py
import multiprocessing as Queue
import os
import copy
from timeit import default_timer as time

def dset_append(dataset, data: list):
    """
        appends a list to 1D dataset
    """

    expanded_dataset = dataset
    if type(data) != list:
        lst = [data]
    else:
        lst = data

    # TODO: Check the shape of the dataset
    # TODO: Check the shape of the list

    size = expanded_dataset.size
    expanded_dataset.resize( (size+len(lst),) )
    expanded_dataset[size: (size+len(lst))] = lst

    return expanded_dataset

def dset_write(dataset, data, index, resize_amount=10e6):

    dset = dataset
    size = dset.size

    if type(data) != list:
        data = [data]

    if size - index < len(data):
        dset.resize( (size+resize_amount,) )
    
    dset[index:index+len(data)] = data

    return dset

# ID - i8
# time - f8
# ADC - f4[10]

def init_file():
    # initilize the write file
    file = None
    fileID = 0
    try: # create output folder if does not exist
        os.makedirs("output")
    except:
        pass

    while True:
        try: # will generate the error until the new filename is reached
            filename = "output/data_" + str(fileID) + ".h5"
            file = h5py.File(filename, "w-")
            break
        except:
            try: # close any previously opened file if any
                file.close()
            except:
                pass

            if fileID < 100: # limit the maximum files which can be saved on a hard drive
                fileID += 1
            else:
                print("Error creating file - writer")
                file = None
                return file
    return file

def foo(name, object):
    print("Name: ", name, " | Object: ", object)

def writer_consumer(sensorQueue: Queue, comm: Queue):

    DATA_WRITE = False
    file = None
    batchsize = 1000
    datasets = []
    batchdata = []
    cmd = None
    data = []
    write_frequency = None
    production_frequency = None
    data_step = 1
    que_treshold_size = 10000
    write_index = 1
    freq_index = 1
    initial_data_size = 1e7
    initial_freq_size = 1e3
    data_step_rate = 2e3





    while True:

        if not comm.empty(): # if there is a cmd message, read it
            print("CMD received!")
            cmd = comm.get()
        
        # interpret the cmd
        if cmd == "DATA_WRITE": # begin writing to the hard drive
            cmd = None
            DATA_WRITE = True
            file = init_file()

            if file == None:
                print("failed to open file")
                return
            
            datasets = []     # initialize datasets
            try:
                receivedData = sensorQueue.get(timeout=1)
            except:
                print("Writer: Failed to read data")
                continue

            data = {}
            for item in receivedData.items():
                data[item[0]] = [item[1]]

            for item in data.items():
                datasets.append(file.create_dataset(str(item[0]),(initial_data_size,), maxshape=(None,), compression="lzf"))
                
            write_freq_dataset = file.create_dataset("WRITE_FREQUENCY",(initial_freq_size,), maxshape=(None,))
            production_freq_dataset = file.create_dataset("PRODUCTION_FREQUENCY",(initial_freq_size,), maxshape=(None,))


                

        elif cmd == "DATA_STOP":
            cmd = None
            DATA_WRITE = False
            file = None
            try:
                file.flush()
                file.close()
            except:
                print("Error: Failed to close file.")
            finally:
                return
        
        elif cmd == "EXIT":
            print("Writer exit")
            try:
                file.flush()
                file.close()
                file = None
            finally:
                return

        if DATA_WRITE and not sensorQueue.empty() and not file == None:
            t = time()
            last_que_size = sensorQueue.qsize()
            while  time()-t < 1: #len(batchdata) < batchsize and
                try:
                    for i in range(data_step):
                        data = sensorQueue.get(timeout=1)
                except Exception as e:
                    print(e)
                    continue
                batchdata.append(list(data.values()))
            batchsize = len(batchdata)

            i = 0
            for dset in datasets:
                dset = dset_write(dset, [item[i] for item in batchdata], write_index, initial_data_size)
                i += 1



            que_size = sensorQueue.qsize()
            write_frequency = batchsize/(time()-t)
            production_frequency = (que_size-last_que_size + batchsize*data_step)/(time()-t)

            # If producer is way faster than the consumer and if the que size is becoming large start skipping data
            if que_size > que_treshold_size:
                data_step = int((que_size-que_treshold_size) // data_step_rate)
                if data_step < 1:
                    data_step = 1
                

            write_freq_dataset = dset_write(write_freq_dataset, write_frequency, freq_index, initial_freq_size)
            production_freq_dataset = dset_write(production_freq_dataset, production_frequency,freq_index, initial_freq_size)

            write_index += batchsize
            freq_index += 1

            batchdata = []
            print("Queue size: ", que_size)
            print("Queue skiprate: ", data_step)

            
