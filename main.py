from PySide6.QtWidgets import QApplication, QPushButton, QLabel, QLineEdit
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QObject, Signal
from random import randint
from threads import *
from threading import Thread
from queue import Queue
import sys
from threading import Lock
from os import system

system("cls")




# UI init
app = QApplication([])

# open the .ui file
ui_file = QFile("app/app.ui")
ui_file.open(QFile.ReadOnly)

# Load the UI
loader = QUiLoader()
window = loader.load(ui_file)
ui_file.close()

if window is None:
    print("Error: Failed to load UI from app/app.ui")
    sys.exit(1)


# Threading init
uiQueue = Queue(maxsize=3) # ADC, ID, time
writerQueue = Queue(maxsize=500000)
producerCMD = Queue(maxsize=10)
uiCMD = Queue(maxsize=10)
writerCMD = Queue(maxsize=10)

producer_thread = Thread(target=DummyProducer, args=(uiQueue, writerQueue, producerCMD), daemon=True)
consumer_thread = Thread(target=UIconsumer, args=(uiQueue, window, uiCMD), daemon=True)
writer_thread = Thread(target=writer_consumer, args=(writerQueue, writerCMD))

producer_thread.start()
consumer_thread.start()
writer_thread.start()

writerCMD.put("DATA_WRITE")


def onExit(app):
    print("EXIT onExit")
    sys.exit(app.exec())




# Show the window
window.show()
app_ref = app.exec()

print("EXIT APP")
writerCMD.put("DATA_STOP")
writerCMD.put("EXIT")
producerCMD.put("EXIT")
uiCMD.put("EXIT")

producer_thread.join(timeout=2)
consumer_thread.join(timeout=10)
writer_thread.join(timeout=10)

sys.exit(app_ref)
