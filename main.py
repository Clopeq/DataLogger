from PySide6.QtWidgets import QApplication, QPushButton, QLabel, QLineEdit
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from random import randint


app = QApplication([])

# open the .ui file
ui_file = QFile("app/app.ui")
ui_file.open(QFile.ReadOnly)

# Load the UI
loader = QUiLoader()
window = loader.load(ui_file)
ui_file.close()




button = window.findChild(QPushButton, "pushButton")
label = window.findChild(QLabel, "label")
lineEdit = window.findChild(QLineEdit, "lineEdit")

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
