import time
from Backend.Facade import Facade
from ui_Scraper import Ui_HSIWebScraper
from PyQt6.QtWidgets import QApplication, QMainWindow
from Backend.Keywords import Keywords


# To make changes to UI do NOT edit MainWindow_ui.py, instead make changes to UI using Qt Creator.

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
        self.keyword_sets = self.keywords_instance.get_set()
        self.keywords_selected = set()
        self.keys_to_add_to_new_set = []

        self.initialize_keywords(self.keywords)
        self.initialize_keyword_sets(self.keyword_sets)

        # dark mode
        # self.setStyleSheet(qdarkstyle.load_stylesheet('pyqt6'))

        ''' Bind GUI components to functions: '''
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

        # bind keywordInclusivecheckBox to keyword_inclusive_check_box function
        self.ui.keywordInclusivecheckBox.stateChanged.connect(self.keyword_inclusive_check_box)

        # bind setSelectionDropdown to set_selection_dropdown function
        self.ui.setSelectionDropdown.currentIndexChanged.connect(self.set_selection_dropdown)

        # bind addKeywordButton to add_keyword_button_clicked function
        self.ui.addKeywordButton.clicked.connect(self.add_keyword_button_clicked)

        # bind removeKeywordButton to remove_keyword_button_clicked function
        self.ui.removeKeywordButton.clicked.connect(self.remove_keyword_button_clicked)

        # bind addSetButton to add_set_button_clicked function
        self.ui.addSetButton.clicked.connect(self.add_set_button_clicked)
        # TODO - disable addSetButton until new set name is entered?

        # bind removeSetButton to remove_set_button_clicked function
        self.ui.removeSetButton.clicked.connect(self.remove_set_button_clicked)

        # bind locationTextBox to location_text_box function
        self.ui.setlocationDropdown.currentIndexChanged.connect(self.location_text_box)

    ''' Functions used to handle events: '''

    # remove set when button is clicked
    def remove_set_button_clicked(self):
        # get name of set to remove
        set_to_remove = self.ui.setList.currentItem().text()

        # remove set from keyword_sets
        self.keywords_instance.remove_set(set_to_remove)

        # remove set from GUI
        self.ui.setList.takeItem(self.ui.setList.currentRow())

        # update list of sets
        self.ui.setSelectionDropdown.clear()
        self.ui.setSelectionDropdown.addItems(self.keyword_sets)

    # TODO - get locations based on scraper selected 
    def location_text_box(self):
        self.location = self.ui.setlocationDropdown.currentText()

    # add new set when button is clicked
    def add_set_button_clicked(self):
        # get name of new set
        new_set_name = self.ui.newSetTextBox.text()

        # get text from list
        for item in self.ui.keywordList.selectedItems():
            self.keys_to_add_to_new_set.append(item.text())

        # call create_set function from keywords class
        self.keywords_instance.create_set(new_set_name, self.keys_to_add_to_new_set)

        # update list of sets
        self.ui.setList.addItem(new_set_name)

        # make self.keys_to_add_to_new_set a empty list
        self.keys_to_add_to_new_set = []

    # remove new keyword
    def remove_keyword_button_clicked(self):
        # find text of selected item
        keyword = self.ui.keywordList.currentItem().text()

        if keyword != '':
            self.remove_keyword(keyword)

    # add new keyword
    def add_keyword_button_clicked(self):
        keyword = self.ui.newKeywordTextBox.text()

        if keyword != '':
            self.ui.keywordlistWidget.addItem(keyword)
            self.ui.keywordList.addItem(keyword)
            # add keyword to text file
            self.keywords_instance.add_keywords(keyword)

    # initialize all keywords to scraper tab
    def initialize_keywords(self, keywords):
        for keyword in keywords:
            self.ui.keywordlistWidget.addItem(keyword)
            self.ui.keywordList.addItem(keyword)

    # initialize all keyword sets to GUI
    def initialize_keyword_sets(self, keyword_sets):
        for keyword_set in keyword_sets:
            self.ui.setSelectionDropdown.addItem(keyword_set)
            self.ui.setList.addItem(keyword_set)

    # remove keyword from keywordlistWidget
    def remove_keyword(self, keyword):
        # remove keyword from keywordlistWidget using keyword text
        for i in range(self.ui.keywordlistWidget.count()):
            if self.ui.keywordlistWidget.item(i).text() == keyword:
                self.ui.keywordlistWidget.takeItem(i)
                self.ui.keywordList.takeItem(i)

                # remove from text file
                self.keywords_instance.remove_keywords(keyword)
                break

    # hadle list of keywords to be searched
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

    # handle dropdown menu for keyword sets
    def set_selection_dropdown(self):
        selected_set = self.ui.setSelectionDropdown.currentText()
        print(selected_set)

        # if empty set, unselect all keywords
        if selected_set == '':
            for i in range(self.ui.keywordlistWidget.count()):
                self.ui.keywordlistWidget.item(i).setSelected(False)
            return

        # get keywords from selected set from keywords class
        keyword_in_set = self.keywords_instance.get_set_values(selected_set)

        print(keyword_in_set)

        # select keyword_in_set in keywordlistWidget
        for i in range(self.ui.keywordlistWidget.count()):
            if self.ui.keywordlistWidget.item(i).text() in keyword_in_set:
                self.ui.keywordlistWidget.item(i).setSelected(True)
            else:
                self.ui.keywordlistWidget.item(i).setSelected(False)

        # unselect all keywords in keywordlistWidget keyword_in_set is empty
        if not keyword_in_set:
            for i in range(self.ui.keywordlistWidget.count()):
                self.ui.keywordlistWidget.item(i).setSelected(False)


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

    # if checked, select all items in list widget
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

    # handle dropdown menu for payment method
    def website_selection_dropdown(self):
        self.website_selection = self.ui.websiteSelectionDropdown.currentText()
        print(self.ui.websiteSelectionDropdown.currentText())
        self.ui.searchButton.setEnabled(True)

    # scrape website selected when search button is clicked
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
