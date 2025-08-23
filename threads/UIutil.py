

def tareClick(producerCMD):
    producerCMD.put("TARE")


def calibrateClick(producerCMD, actualValue):
    producerCMD.put("CALIBRATE"+str(actualValue))
