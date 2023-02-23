import time
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
from Backend.Facade import Facade
from Backend.Keywords import Keywords
from Scraper import Ui_HSIWebScraper


# To make changes to UI do NOT edit MainWindow_ui.py, instead make changes to UI using Qt Creator.

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_HSIWebScraper()
        self.ui.setupUi(self)
        self.keywords_instance = Keywords()
        self.facade = Facade()

        # TODO - center app when screen maximized
        # self.central_widget = QWidget(self)
        # self.layout = QVBoxLayout(self.central_widget)
        # self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.setCentralWidget(self.central_widget)
        # self.showMaximized()

        # attributes used to handle events
        self.website_selection = ''
        self.include_payment_method = False
        self.search_text = ''
        self.keywords = self.keywords_instance.get_keywords()
        self.keyword_sets = self.keywords_instance.get_set()
        self.keywords_selected = set()
        self.keys_to_add_to_new_set = []
        self.manual_keyword_selection = set()
        self.set_keyword_selection = set()
        self.locations = []
        self.location = ''

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

        # bind removeSetButton to remove_set_button_clicked function
        self.ui.removeSetButton.clicked.connect(self.remove_set_button_clicked)

        # bind locationTextBox to location_text_box function
        self.ui.setlocationDropdown.currentIndexChanged.connect(self.set_location)

    ''' Functions used to handle events: '''

    # popup to confirm set removal
    @staticmethod
    def remove_set_popup_window(set_to_remove):
        popup = QtWidgets.QMessageBox()

        popup.setWindowTitle("Confirm Set Removal")
        popup.setText(f"Are you sure you want to remove {set_to_remove} from the list of sets?")
        popup.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)

        if popup.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
            return True
        else:
            return False

    # remove set when button is clicked
    def remove_set_button_clicked(self):
        # get name of set to remove
        set_to_remove = self.ui.setList.currentItem().text()

        confirmation = self.remove_set_popup_window(set_to_remove)
        if not confirmation:
            return

        # remove set from keyword_sets
        self.keywords_instance.remove_set(set_to_remove)

        # remove set from GUI
        self.ui.setList.takeItem(self.ui.setList.currentRow())

        # update list of sets
        self.ui.setSelectionDropdown.clear()
        self.ui.setSelectionDropdown.addItems(self.keyword_sets)

    # set location based on selection from the dropdown
    def set_location(self):
        self.location = self.ui.setlocationDropdown.currentText()

        if self.website_selection == 'eros':
            self.facade.set_eros_city(self.location)

        if self.website_selection == 'escortalligator':
            self.facade.set_escortalligator_city(self.location)

        if self.website_selection == 'yesbackpage':
            self.facade.set_yesbackpage_city(self.location)

        if self.website_selection == 'megapersonals':
            self.facade.set_megapersonals_city(self.location)

        if self.website_selection == 'skipthegames':
            self.facade.set_skipthegames_city(self.location)

    # initialize locations based on website that is selected
    def initialize_location_dropdown(self):
        self.ui.setlocationDropdown.clear()
        for location in self.locations:
            self.ui.setlocationDropdown.addItem(location)

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

        # make self.keys_to_add_to_new_set of an empty list
        self.keys_to_add_to_new_set = []

        # add new set to setSelectionDropdown
        self.ui.setSelectionDropdown.addItem(new_set_name)

        # clear new set text box
        self.ui.newSetTextBox.clear()

    # popup to confirm keyword removal
    @staticmethod
    def remove_keyword_popup_window(keyword_to_remove):
        popup = QtWidgets.QMessageBox()
        popup.setWindowTitle("Confirm Keyword Removal")
        popup.setText(f"Are you sure you want to remove {keyword_to_remove} from the list of keywords? \n\nWarning: "
                      f"{keyword_to_remove} will be removed from all sets.")
        font = popup.font()
        font.setBold(True)
        popup.setFont(font)
        popup.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)

        if popup.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
            return True
        else:
            return False

    # TODO BUG - last item clicked on is deleted even if not selected
    # remove new keyword
    def remove_keyword_button_clicked(self):
        # find text of selected item
        keyword = self.ui.keywordList.currentItem().text()

        # confirm keyword removal
        confirmation = self.remove_keyword_popup_window(keyword)

        if not confirmation:
            return

        if keyword != '':
            self.remove_keyword(keyword)

            # loop through sets and remove keyword from each set
            for set_name in self.keyword_sets:
                if keyword in self.keywords_instance.get_set_values(set_name):
                    self.keywords_instance.remove_keyword_from_set(keyword, set_name)

    # add new keyword
    def add_keyword_button_clicked(self):
        keyword = self.ui.newKeywordTextBox.text()

        if keyword != '':
            self.ui.keywordlistWidget.addItem(keyword)
            self.ui.keywordList.addItem(keyword)
            # add keyword to text file
            self.keywords_instance.add_keywords(keyword)

            # clear new keyword text box
            self.ui.newKeywordTextBox.clear()

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

    # handle list of keywords to be searched
    def keyword_list_widget(self):
        for item in self.ui.keywordlistWidget.selectedItems():
            self.manual_keyword_selection.add(item.text())

        # if a keyword is unselected, remove it from the set
        for i in range(self.ui.keywordlistWidget.count()):
            if not self.ui.keywordlistWidget.item(i).isSelected():
                self.manual_keyword_selection.discard(self.ui.keywordlistWidget.item(i).text())

        print(self.manual_keyword_selection)

    # handle dropdown menu for keyword sets
    def set_selection_dropdown(self):
        selected_set = self.ui.setSelectionDropdown.currentText()
        print(selected_set)

        # if empty set, unselect all keywords
        if selected_set == '':
            for i in range(self.ui.keywordlistWidget.count()):
                if self.ui.keywordlistWidget.item(i).text() not in self.manual_keyword_selection:
                    self.ui.keywordlistWidget.item(i).setSelected(False)

            return

        # get keywords from selected set from keywords class
        keywords_of_selected_set = set(self.keywords_instance.get_set_values(selected_set))

        print('values of keyword selected: ', keywords_of_selected_set)

        # select keywords_of_selected_set in keywordlistWidget
        for i in range(self.ui.keywordlistWidget.count()):
            if self.ui.keywordlistWidget.item(i).text() in keywords_of_selected_set:
                self.ui.keywordlistWidget.item(i).setSelected(True)

            elif self.ui.keywordlistWidget.item(i).text() not in self.manual_keyword_selection:
                self.ui.keywordlistWidget.item(i).setSelected(False)

        # unselect keywords that are not in selected set
        if not keywords_of_selected_set:
            print('self.manual_keyword_selection: ', self.manual_keyword_selection)
            for i in range(self.ui.keywordlistWidget.count()):
                if self.ui.keywordlistWidget.item(i).text() not in self.manual_keyword_selection:
                    self.ui.keywordlistWidget.item(i).setSelected(False)

    # scrape using text box input
    def search_text_box(self):
        self.search_text = self.ui.searchTextBox.text()

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
            self.include_payment_method = True
            print('payment box checked')
        else:
            self.ui.paymentMethodcheckBox.setEnabled(False)
            self.include_payment_method = False
            print('payment box unchecked')

        # enable checkbox after it's unchecked
        self.ui.paymentMethodcheckBox.setEnabled(True)

    # handle dropdown menu for payment method
    def website_selection_dropdown(self):
        self.website_selection = self.ui.websiteSelectionDropdown.currentText()
        print(self.ui.websiteSelectionDropdown.currentText())
        self.ui.searchButton.setEnabled(True)

        if self.website_selection == 'eros':
            self.locations = self.facade.get_eros_cities()
            self.set_location()
            self.initialize_location_dropdown()

        if self.website_selection == 'escortalligator':
            self.locations = self.facade.get_escortalligator_cities()
            self.set_location()
            self.initialize_location_dropdown()

        if self.website_selection == 'yesbackpage':
            self.locations = self.facade.get_yesbackpage_cities()
            self.set_location()
            self.initialize_location_dropdown()

        if self.website_selection == 'megapersonals':
            self.locations = self.facade.get_megapersonals_cities()
            self.set_location()
            self.initialize_location_dropdown()

        if self.website_selection == 'skipthegames':
            self.locations = self.facade.get_skipthegames_cities()
            self.set_location()
            self.initialize_location_dropdown()

    # TODO - pop up when search button is clicked - show progress bar, status? & cancel button
    @staticmethod
    def search_popup_window(website_selection):
        popup = QtWidgets.QMessageBox()
        popup.setWindowTitle("Scraping in Progress")
        popup.setText(f"Scraping {website_selection} in progress...")
        popup.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Cancel)

        if popup.exec() == QtWidgets.QMessageBox.StandardButton.Cancel:
            print('scraping interrupted')
            popup.close()

    # scrape website selected when search button is clicked
    def search_button_clicked(self):
        # self.search_popup_window(self.website_selection)

        self.keywords_selected = set()

        # add input text to self.keywords_selected set
        print('text box: ', self.keywords_selected)

        # find keywords selected in keyword list widget
        for i in range(self.ui.keywordlistWidget.count()):
            if self.ui.keywordlistWidget.item(i).isSelected():
                self.keywords_selected.add(self.ui.keywordlistWidget.item(i).text())

        if self.search_text:
            self.keywords_selected.add(self.search_text)

        print('list widget keywords: ', self.keywords_selected)

        if self.website_selection == 'escortalligator':
            try:
                self.facade.initialize_escortalligator_scraper(self.keywords_selected)
            except:
                print('Error occurred, please try again. ')
            time.sleep(2)

        if self.website_selection == 'megapersonals':
            try:
                self.facade.initialize_megapersonals_scraper(self.keywords_selected)
            except:
                print('Error occurred, please try again. ')
            time.sleep(2)

        if self.website_selection == 'skipthegames':
            try:
                self.facade.initialize_skipthegames_scraper(self.keywords_selected)
            except:
                print('Error occurred, please try again. ')
            time.sleep(2)

        if self.website_selection == 'yesbackpage':
            try:
                self.facade.initialize_yesbackpage_scraper(self.keywords_selected)
            except:
                print('Error occurred, please try again. ')
            time.sleep(2)

        if self.website_selection == 'eros':
            try:
                # self.run_threads(self.search_popup_window(self.website_selection),
                #                  self.facade.initialize_eros_scraper(self.keywords_selected))
                self.facade.initialize_eros_scraper(self.keywords_selected)
            except:
                print('Error occurred, please try again.')
            time.sleep(2)

    # TODO
    # function to run two threads at once
    # @staticmethod
    # def run_threads(function1, function2):
    #     thread1 = threading.Thread(target=function1)
    #     thread2 = threading.Thread(target=function2)
    #     thread1.start()
    #     thread2.start()
    #     thread2.join()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
