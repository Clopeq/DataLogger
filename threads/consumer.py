from utilities import display
import time

def UIconsumer(sensorData, label):
    """
    Updates the label with the first ADC value from the data dictionary if available, otherwise displays 'No data'.

    Parameters:
        data (dict): Dictionary containing ADC data under the 'ADC' key.
        label: UI label object with a setText(str) method.
    """

    data = {}

    while True:

        if not sensorData.empty():
            data = sensorData.get()
        else:
            continue

        try:
            label.setText(str(data["ID"]) + " " + str(data["time"]))
        except:
            print("UI consumer: No data")
            label.setText("No data")

        time.sleep(0.1)