import sys
from PyQt6 import QtWidgets, uic
import qdarkstyle

app = QtWidgets.QApplication(sys.argv)

# dark mode
app.setStyleSheet(qdarkstyle.load_stylesheet('pyqt6'))

window = uic.loadUi("MainWindow.ui")
window.show()
app.exec()
