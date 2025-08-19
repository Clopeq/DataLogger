import time
import h5py


# ID - i8
# time - f8
# ADC - f4[10]

def wirter_consumer(sensorQueue, comm):

    DATA_WRITE = False


    while True:
        if not comm.empty(): # if there is a cmd message, read it
            cmd = comm.get()
        
        # interpret the cmd
        if cmd == "DATA_WRITE": # begin writing to the hard drive
            DATA_WRITE = True

            # initilize the write file
            now = time.localtime()
            filename = "output/data_" + time.strftime("%Y%M%D_%H%M%S", now) + ".h5"
            file = h5py.File(filename, "a")

        elif cmd == "DATA_STOP":
            DATA_WRITE = False

        if DATA_WRITE and not sensorQueue.empty():
            try:
                data = sensorQueue.get(timeout=0.5)
            except Exception:
                continue

            if 'file' in locals() and file is not None:
                for key, value in data.items():
                    if key not in file:
                        maxsize = (None,) + value.shape[1:]
                        file.create_dataset(key, data=value, maxshape=maxsize, chunks=True)
                    else:
                        dset = file[key]
                        old_size = dset.shape[0]
                        new_size = old_size + value.shape[0]
                        dset.resize((new_size,) + dset.shape[1:])
                        dset[old_size:new_size] = value
                    dset[old_size:new_size] = value
