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

button = window.findChild(QPushButton, "pushButton")
label = window.findChild(QLabel, "label")
lineEdit = window.findChild(QLineEdit, "lineEdit")


# Threading init
uiQueue = Queue(maxsize=3) # ADC, ID, time
writerQueue = Queue(maxsize=500000)
producerCMD = Queue(maxsize=10)
uiCMD = Queue(maxsize=10)
writerCMD = Queue(maxsize=10)

producer_thread = Thread(target=DummyProducer, args=(uiQueue, writerQueue, producerCMD), daemon=True)
consumer_thread = Thread(target=UIconsumer, args=(uiQueue, label, uiCMD), daemon=True)
writer_thread = Thread(target=writer_consumer, args=(writerQueue, writerCMD))

producer_thread.start()
consumer_thread.start()
writer_thread.start()

writerCMD.put("DATA_WRITE")


def onClick(queue):
    label.setText(lineEdit.text())
    button.setText(str(randint(1, 100)))
    print("Button clicked!")
    queue.put("EXIT")


def onExit(app):
    sys.exit(app.exec())

if button is not None:
    button.clicked.connect(lambda: onClick(producerCMD))
else:
    print("Error: 'pushButton' not found in the UI.")


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
