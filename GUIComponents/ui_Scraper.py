# Form implementation generated from reading ui file '/Users/dg/Desktop/Scraper/GUIComponents/Scraper.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_HSIWebScraper(object):
    def setupUi(self, HSIWebScraper):
        HSIWebScraper.setObjectName("HSIWebScraper")
        HSIWebScraper.resize(953, 579)
        self.tabWidget = QtWidgets.QTabWidget(parent=HSIWebScraper)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 951, 581))
        self.tabWidget.setObjectName("tabWidget")
        self.MainScraper = QtWidgets.QWidget()
        self.MainScraper.setToolTipDuration(-1)
        self.MainScraper.setObjectName("MainScraper")
        self.keywordlistWidget = QtWidgets.QListWidget(parent=self.MainScraper)
        self.keywordlistWidget.setGeometry(QtCore.QRect(550, 130, 301, 221))
        self.keywordlistWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.MultiSelection)
        self.keywordlistWidget.setObjectName("keywordlistWidget")
        self.setSelectionDropdown = QtWidgets.QComboBox(parent=self.MainScraper)
        self.setSelectionDropdown.setGeometry(QtCore.QRect(130, 280, 161, 41))
        self.setSelectionDropdown.setCurrentText("")
        self.setSelectionDropdown.setObjectName("setSelectionDropdown")
        self.setSelectionDropdown.addItem("")
        self.setSelectionDropdown.setItemText(0, "")
        self.setSelectionLabel = QtWidgets.QLabel(parent=self.MainScraper)
        self.setSelectionLabel.setGeometry(QtCore.QRect(130, 260, 241, 16))
        self.setSelectionLabel.setObjectName("setSelectionLabel")
        self.keywordListLabel = QtWidgets.QLabel(parent=self.MainScraper)
        self.keywordListLabel.setGeometry(QtCore.QRect(550, 110, 161, 16))
        self.keywordListLabel.setObjectName("keywordListLabel")
        self.searchButton = QtWidgets.QPushButton(parent=self.MainScraper)
        self.searchButton.setGeometry(QtCore.QRect(440, 500, 80, 24))
        self.searchButton.setObjectName("searchButton")
        self.keywordInclusivecheckBox = QtWidgets.QCheckBox(parent=self.MainScraper)
        self.keywordInclusivecheckBox.setGeometry(QtCore.QRect(550, 430, 241, 22))
        self.keywordInclusivecheckBox.setObjectName("keywordInclusivecheckBox")
        self.textSearchLabel = QtWidgets.QLabel(parent=self.MainScraper)
        self.textSearchLabel.setGeometry(QtCore.QRect(130, 350, 201, 16))
        self.textSearchLabel.setObjectName("textSearchLabel")
        self.HSIScraperlabel = QtWidgets.QLabel(parent=self.MainScraper)
        self.HSIScraperlabel.setGeometry(QtCore.QRect(370, 20, 231, 61))
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(True)
        self.HSIScraperlabel.setFont(font)
        self.HSIScraperlabel.setObjectName("HSIScraperlabel")
        self.websiteSelectionDropdown = QtWidgets.QComboBox(parent=self.MainScraper)
        self.websiteSelectionDropdown.setGeometry(QtCore.QRect(130, 140, 161, 41))
        self.websiteSelectionDropdown.setCurrentText("")
        self.websiteSelectionDropdown.setObjectName("websiteSelectionDropdown")
        self.websiteSelectionDropdown.addItem("")
        self.websiteSelectionDropdown.setItemText(0, "")
        self.websiteSelectionDropdown.addItem("")
        self.websiteSelectionDropdown.addItem("")
        self.websiteSelectionDropdown.addItem("")
        self.websiteSelectionDropdown.addItem("")
        self.websiteSelectionDropdown.addItem("")
        self.websiteSelectionLabel = QtWidgets.QLabel(parent=self.MainScraper)
        self.websiteSelectionLabel.setGeometry(QtCore.QRect(130, 120, 161, 16))
        self.websiteSelectionLabel.setObjectName("websiteSelectionLabel")
        self.searchTextBox = QtWidgets.QLineEdit(parent=self.MainScraper)
        self.searchTextBox.setGeometry(QtCore.QRect(140, 370, 161, 31))
        self.searchTextBox.setText("")
        self.searchTextBox.setObjectName("searchTextBox")
        self.selectAllKeywordscheckBox = QtWidgets.QCheckBox(parent=self.MainScraper)
        self.selectAllKeywordscheckBox.setGeometry(QtCore.QRect(550, 370, 201, 22))
        self.selectAllKeywordscheckBox.setObjectName("selectAllKeywordscheckBox")
        self.paymentMethodcheckBox = QtWidgets.QCheckBox(parent=self.MainScraper)
        self.paymentMethodcheckBox.setGeometry(QtCore.QRect(550, 400, 271, 22))
        self.paymentMethodcheckBox.setObjectName("paymentMethodcheckBox")
        self.setlocationDropdown = QtWidgets.QComboBox(parent=self.MainScraper)
        self.setlocationDropdown.setGeometry(QtCore.QRect(130, 210, 161, 41))
        self.setlocationDropdown.setCurrentText("")
        self.setlocationDropdown.setObjectName("setlocationDropdown")
        self.setlocationDropdown.addItem("")
        self.setlocationDropdown.setItemText(0, "")
        self.setLocationLabel = QtWidgets.QLabel(parent=self.MainScraper)
        self.setLocationLabel.setGeometry(QtCore.QRect(130, 190, 201, 16))
        self.setLocationLabel.setObjectName("setLocationLabel")
        self.tabWidget.addTab(self.MainScraper, "")
        self.EditKeywords = QtWidgets.QWidget()
        self.EditKeywords.setObjectName("EditKeywords")
        self.setList = QtWidgets.QListWidget(parent=self.EditKeywords)
        self.setList.setGeometry(QtCore.QRect(600, 180, 256, 192))
        self.setList.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.setList.setObjectName("setList")
        self.newSetTextBox = QtWidgets.QLineEdit(parent=self.EditKeywords)
        self.newSetTextBox.setGeometry(QtCore.QRect(600, 130, 121, 31))
        self.newSetTextBox.setObjectName("newSetTextBox")
        self.addKeywordButton = QtWidgets.QPushButton(parent=self.EditKeywords)
        self.addKeywordButton.setGeometry(QtCore.QRect(240, 130, 121, 32))
        self.addKeywordButton.setObjectName("addKeywordButton")
        self.newKeywordTextBox = QtWidgets.QLineEdit(parent=self.EditKeywords)
        self.newKeywordTextBox.setGeometry(QtCore.QRect(110, 130, 121, 31))
        self.newKeywordTextBox.setObjectName("newKeywordTextBox")
        self.keywordList = QtWidgets.QListWidget(parent=self.EditKeywords)
        self.keywordList.setGeometry(QtCore.QRect(110, 180, 256, 192))
        self.keywordList.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.keywordList.setObjectName("keywordList")
        self.removeKeywordButton = QtWidgets.QPushButton(parent=self.EditKeywords)
        self.removeKeywordButton.setGeometry(QtCore.QRect(140, 380, 191, 32))
        self.removeKeywordButton.setObjectName("removeKeywordButton")
        self.newKeywordLabel = QtWidgets.QLabel(parent=self.EditKeywords)
        self.newKeywordLabel.setGeometry(QtCore.QRect(110, 110, 131, 16))
        self.newKeywordLabel.setObjectName("newKeywordLabel")
        self.newSetLabel = QtWidgets.QLabel(parent=self.EditKeywords)
        self.newSetLabel.setGeometry(QtCore.QRect(600, 110, 321, 16))
        self.newSetLabel.setObjectName("newSetLabel")
        self.addSetButton = QtWidgets.QPushButton(parent=self.EditKeywords)
        self.addSetButton.setGeometry(QtCore.QRect(730, 130, 121, 32))
        self.addSetButton.setObjectName("addSetButton")
        self.removeSetButton = QtWidgets.QPushButton(parent=self.EditKeywords)
        self.removeSetButton.setGeometry(QtCore.QRect(630, 380, 191, 32))
        self.removeSetButton.setObjectName("removeSetButton")
        self.tabWidget.addTab(self.EditKeywords, "")

        self.retranslateUi(HSIWebScraper)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(HSIWebScraper)

    def retranslateUi(self, HSIWebScraper):
        _translate = QtCore.QCoreApplication.translate
        HSIWebScraper.setWindowTitle(_translate("HSIWebScraper", "HSI Web Scraper"))
        self.setSelectionLabel.setText(_translate("HSIWebScraper", "  Select set of keywords (optional):"))
        self.keywordListLabel.setText(_translate("HSIWebScraper", "List of keywords:"))
        self.searchButton.setText(_translate("HSIWebScraper", "Search"))
        self.keywordInclusivecheckBox.setText(_translate("HSIWebScraper", "Keyword inclusive search (AND)"))
        self.textSearchLabel.setText(_translate("HSIWebScraper", "  Type text to scrape (optional):"))
        self.HSIScraperlabel.setText(_translate("HSIWebScraper", "HSI Web Scraper"))
        self.websiteSelectionDropdown.setItemText(1, _translate("HSIWebScraper", "escortalligator"))
        self.websiteSelectionDropdown.setItemText(2, _translate("HSIWebScraper", "megapersonals"))
        self.websiteSelectionDropdown.setItemText(3, _translate("HSIWebScraper", "skipthegames"))
        self.websiteSelectionDropdown.setItemText(4, _translate("HSIWebScraper", "yesbackpage"))
        self.websiteSelectionDropdown.setItemText(5, _translate("HSIWebScraper", "eros"))
        self.websiteSelectionLabel.setText(_translate("HSIWebScraper", "  Select website to scrape:"))
        self.selectAllKeywordscheckBox.setText(_translate("HSIWebScraper", "Select all keywords from list"))
        self.paymentMethodcheckBox.setText(_translate("HSIWebScraper", "Find only posts with payment methods"))
        self.setLocationLabel.setText(_translate("HSIWebScraper", "  Select location (optional)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.MainScraper), _translate("HSIWebScraper", "Scraper"))
        self.addKeywordButton.setText(_translate("HSIWebScraper", "Add keyword"))
        self.removeKeywordButton.setText(_translate("HSIWebScraper", "Remove selected keyword"))
        self.newKeywordLabel.setText(_translate("HSIWebScraper", "Enter new keyword:"))
        self.newSetLabel.setText(_translate("HSIWebScraper", "Enter new set name (select keywords below)"))
        self.addSetButton.setText(_translate("HSIWebScraper", "Add set"))
        self.removeSetButton.setText(_translate("HSIWebScraper", "Remove selected set"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.EditKeywords), _translate("HSIWebScraper", "Edit Keywords"))
