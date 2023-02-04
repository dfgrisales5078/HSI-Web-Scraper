import qdarkstyle
from PyQt6.QtWidgets import QApplication, QMainWindow
from Backend.Facade import Facade
from MainWindow import Ui_HSIWebScraper

"""Temporarily hardcoded search button to scrape yesbackpacge"""

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_HSIWebScraper()
        self.ui.setupUi(self)
        # dark mode
        self.setStyleSheet(qdarkstyle.load_stylesheet('pyqt6'))

        # bind searchButton to search_button_clicked function
        self.ui.searchButton.clicked.connect(self.search_button_clicked)

    @staticmethod
    def search_button_clicked():
        facade = Facade()
        facade.initialize_yesbackpage_scraper()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
