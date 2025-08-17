from PySide6.QtWidgets import QApplication, QPushButton, QLabel, QLineEdit
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QObject, Signal
from random import randint
from threads import *
from threading import Thread
from queue import Queue
import sys



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


max = 50
work = Queue()
finished = Queue()

producer_thread = Thread(target=DummyProducer, args=[work, finished, max], daemon=True)
consumer_thread = Thread(target=Consumer, args=[work, finished, label], daemon=True)

producer_thread.start()
consumer_thread.start()


def onClick():
    label.setText(lineEdit.text())
    button.setText(str(randint(1, 100)))
    print("Button clicked!")


if button is not None:
    button.clicked.connect(onClick)
else:
    print("Error: 'pushButton' not found in the UI.")


# Show the window
window.show()
app.exec()


producer_thread.join()
consumer_thread.join()