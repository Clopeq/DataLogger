from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile


app = QApplication([])

# open the .ui file
ui_file = QFile("app/app.ui")
ui_file.open(QFile.ReadOnly)

# Load the UI
loader = QUiLoader()
window = loader.load(ui_file)
ui_file.close()

# Show the window
window.show()
app.exec()


print("foo")

