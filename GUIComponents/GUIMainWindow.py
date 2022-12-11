import sys
from PyQt6 import QtWidgets, uic
import qdarkstyle


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("MainWindow.ui", self)
        # dark mode
        self.setStyleSheet(qdarkstyle.load_stylesheet('pyqt6'))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
