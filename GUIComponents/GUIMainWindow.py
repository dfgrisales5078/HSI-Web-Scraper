import qdarkstyle
from PyQt6.QtWidgets import QApplication, QMainWindow
from Backend.Facade import Facade
from MainWindow_ui import Ui_HSIWebScraper

# To make changes to UI: do NOT edit MainWindow_ui.py, make changes to UI using Qt Creator and then run the following
# command: pyuic6 MainWindow.ui -o MainWindow_ui.py

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.selection = ''
        self.ui = Ui_HSIWebScraper()
        self.ui.setupUi(self)

        # dark mode
        self.setStyleSheet(qdarkstyle.load_stylesheet('pyqt6'))

        # bind websiteSelectionDropdown to website_selection_dropdown function
        self.ui.websiteSelectionDropdown.currentIndexChanged.connect(self.website_selection_dropdown)

        # bind searchButton to search_button_clicked function
        self.ui.searchButton.clicked.connect(self.search_button_clicked)

    def website_selection_dropdown(self):
        print(self.ui.websiteSelectionDropdown.currentText())
        self.selection = self.ui.websiteSelectionDropdown.currentText()

    def search_button_clicked(self):
        facade = Facade()
        if self.selection == 'escortalligator':
            facade.initialize_escortalligator_scraper()
        
        if self.selection == 'megapersonals':
            facade.initialize_megapersonals_scraper()

        if self.selection == 'skipthegames':
            facade.initialize_skipthegames_scraper()

        if self.selection == 'yesbackpage':
            facade.initialize_yesbackpage_scraper()

        # TODO - fix eros bug
        if self.selection == 'eros':
            facade.initialize_eros_scraper()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
