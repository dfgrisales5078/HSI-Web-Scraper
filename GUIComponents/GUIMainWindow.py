import time
from PyQt6 import QtWidgets
from Backend.Facade import Facade
from MainWindow_ui import Ui_HSIWebScraper
from PyQt6.QtWidgets import QApplication, QMainWindow
from Backend.Keywords import Keywords

# To make changes to UI do NOT edit MainWindow_ui.py, instead make changes to UI using Qt Creator and then run the
# following command: pyuic6 MainWindow.ui -o MainWindow_ui.py

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_HSIWebScraper()
        self.ui.setupUi(self)
        self.keywords_instance = Keywords()

        # TODO - center app when screen maximized
        # self.central_widget = QWidget(self)
        # self.layout = QVBoxLayout(self.central_widget)
        # self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.setCentralWidget(self.central_widget)
        # self.showMaximized()

        # attributes used to handle events
        self.website_selection = ''
        self.include_payment_method = ''
        self.search_text = ''
        self.keywords = self.keywords_instance.get_keywords()
        self.keywords_selected = set()

        # TODO - remove all hardcoded keywords
        self.initialize_keywords(self.keywords)
        # self.remove_keyword('test keyword')

        # dark mode
        # self.setStyleSheet(qdarkstyle.load_stylesheet('pyqt6'))

        # bind websiteSelectionDropdown to website_selection_dropdown function
        self.ui.websiteSelectionDropdown.currentIndexChanged.connect(self.website_selection_dropdown)

        # disable button until website is selected
        self.ui.searchButton.setEnabled(False)
        # bind searchButton to search_button_clicked function
        self.ui.searchButton.clicked.connect(self.search_button_clicked)

        # bind paymentMethodCheckBox to payment_method_check_box function
        self.ui.paymentMethodcheckBox.stateChanged.connect(self.payment_method_check_box)

        # bind selectAllKeywordscheckBox to select_all_keywords_check_box function
        self.ui.selectAllKeywordscheckBox.stateChanged.connect(self.select_all_keywords_check_box)

        # bind searchTextBox to search_text_box function
        self.ui.searchTextBox.textChanged.connect(self.search_text_box)

        # bind keywordlistWidget to keyword_list_widget function
        self.ui.keywordlistWidget.itemClicked.connect(self.keyword_list_widget)

        # bind toolButton to tool_button_clicked function
        self.ui.toolButton.clicked.connect(self.tool_button_clicked)

        # bind keywordInclusivecheckBox to keyword_inclusive_check_box function
        self.ui.keywordInclusivecheckBox.stateChanged.connect(self.keyword_inclusive_check_box)

        # bind setSelectionDropdown to set_selection_dropdown function
        self.ui.setSelectionDropdown.currentIndexChanged.connect(self.set_selection_dropdown)

        # TODO - bind these functions to the add and remove buttons & Keywords.py from backend
        # self.add_keyword('new keyword')
        # self.remove_keyword('new keyword')

    ''' Functions used to handle events: '''
    # add single keyword to keywordlistWidget
    def add_keyword(self, keyword):
        self.ui.keywordlistWidget.addItem(keyword)
        # add keyword to text file
        self.keywords_instance.add_keywords(keyword)

    # initialize all keywords to GUI
    def initialize_keywords(self, keywords):
        for keyword in keywords:
            self.ui.keywordlistWidget.addItem(keyword)

    # remove keyword from keywordlistWidget
    def remove_keyword(self, keyword):
        # remove keyword from keywordlistWidget using keyword text
        for i in range(self.ui.keywordlistWidget.count()):
            if self.ui.keywordlistWidget.item(i).text() == keyword:
                self.ui.keywordlistWidget.takeItem(i)
                # remove from text file
                self.keywords_instance.remove_keywords(keyword)
                break

    def keyword_list_widget(self):
        # print('selected keywords:')
        for item in self.ui.keywordlistWidget.selectedItems():
            print(item.text())
            self.keywords_selected.add(item.text())

        # if a keyword is unselected, remove it from the set
        for i in range(self.ui.keywordlistWidget.count()):
            if not self.ui.keywordlistWidget.item(i).isSelected():
                self.keywords_selected.discard(self.ui.keywordlistWidget.item(i).text())

        print(self.keywords_selected)

    # TODO - find way to edit list of sets
    def set_selection_dropdown(self):
        print(self.ui.setSelectionDropdown.currentText())

    # TODO - add logic to scrape with search text
    def search_text_box(self):
        self.search_text = self.ui.searchTextBox.text()
        print(self.search_text)

    # TODO - add logic to scrape with all inclusive keywords
    def keyword_inclusive_check_box(self):
        if self.ui.keywordInclusivecheckBox.isChecked():
            self.ui.keywordInclusivecheckBox.setEnabled(True)
            print('keyword inclusive box checked')
        else:
            self.ui.keywordInclusivecheckBox.setEnabled(False)
            print('keyword inclusive box unchecked')

        # enable checkbox after it's unchecked
        self.ui.keywordInclusivecheckBox.setEnabled(True)

    def select_all_keywords_check_box(self):
        if self.ui.selectAllKeywordscheckBox.isChecked():
            self.ui.selectAllKeywordscheckBox.setEnabled(True)
            print('select all keywords box checked')
            # select all items in list widget
            for i in range(self.ui.keywordlistWidget.count()):
                self.ui.keywordlistWidget.item(i).setSelected(True)
                print(self.ui.keywordlistWidget.item(i).text())
                self.keywords_selected.add(self.ui.keywordlistWidget.item(i).text())
        else:
            self.ui.selectAllKeywordscheckBox.setEnabled(False)
            print('select all keywords box unchecked')
            self.keywords_selected = set()
            # deselect all items in list widget
            for i in range(self.ui.keywordlistWidget.count()):
                self.ui.keywordlistWidget.item(i).setSelected(False)

        # enable checkbox after it's unchecked
        self.ui.selectAllKeywordscheckBox.setEnabled(True)
        print(self.keywords_selected)

    # TODO - add logic to scrape with payment method only 
    def payment_method_check_box(self):
        if self.ui.paymentMethodcheckBox.isChecked():
            self.ui.paymentMethodcheckBox.setEnabled(True)
            self.include_payment_method = 'checked'
            print('payment box checked')
        else:
            self.ui.paymentMethodcheckBox.setEnabled(False)
            self.include_payment_method = 'checked'
            print('payment box unchecked')

        # enable checkbox after it's unchecked
        self.ui.paymentMethodcheckBox.setEnabled(True)

    def website_selection_dropdown(self):
        self.website_selection = self.ui.websiteSelectionDropdown.currentText()
        print(self.ui.websiteSelectionDropdown.currentText())
        self.ui.searchButton.setEnabled(True)

    # TODO - edit popup window OR secondary screen in QT Creator
    def tool_button_clicked(self):
        print('tool button clicked')
        # pop up window
        self.popup = QtWidgets.QWidget()
        self.popup.setGeometry(100, 100, 400, 200)
        self.popup.setWindowTitle('Edit Keywords and sets')
        self.popup.show()

    def search_button_clicked(self):
        facade = Facade()
        if self.website_selection == 'escortalligator':
            try:
                facade.initialize_escortalligator_scraper()
            except:
                print('Error occurred, please try again. ')
            time.sleep(2)

        if self.website_selection == 'megapersonals':
            try:
                facade.initialize_megapersonals_scraper()
            except:
                print('Error occurred, please try again. ')
            time.sleep(2)

        if self.website_selection == 'skipthegames':
            try:
                facade.initialize_skipthegames_scraper()
            except:
                print('Error occurred, please try again. ')
            time.sleep(2)

        if self.website_selection == 'yesbackpage':
            try:
                facade.initialize_yesbackpage_scraper()
            except:
                print('Error occurred, please try again. ')
            time.sleep(2)

        if self.website_selection == 'eros':
            try:
                facade.initialize_eros_scraper()
            except:
                print('Error occurred, please try again.')
            time.sleep(2)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
