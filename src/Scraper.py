# Form implementation generated from reading ui file 'Scraper.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_HSIWebScraper(object):
    def setupUi(self, HSIWebScraper):
        HSIWebScraper.setObjectName("HSIWebScraper")
        HSIWebScraper.resize(1126, 688)
        self.tabWidget = QtWidgets.QTabWidget(parent=HSIWebScraper)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1131, 691))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.tabWidget.setFont(font)
        self.tabWidget.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.setFileSelectionButton = QtWidgets.QPushButton(parent=self.tab)
        self.setFileSelectionButton.setGeometry(QtCore.QRect(440, 350, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.setFileSelectionButton.setFont(font)
        self.setFileSelectionButton.setObjectName("setFileSelectionButton")
        self.keywordfileSelectionButton = QtWidgets.QPushButton(parent=self.tab)
        self.keywordfileSelectionButton.setGeometry(QtCore.QRect(440, 190, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.keywordfileSelectionButton.setFont(font)
        self.keywordfileSelectionButton.setObjectName("keywordfileSelectionButton")
        self.selectKeywordFilesLabel = QtWidgets.QLabel(parent=self.tab)
        self.selectKeywordFilesLabel.setGeometry(QtCore.QRect(440, 110, 221, 31))
        self.selectKeywordFilesLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.selectKeywordFilesLabel.setObjectName("selectKeywordFilesLabel")
        self.label = QtWidgets.QLabel(parent=self.tab)
        self.label.setGeometry(QtCore.QRect(300, 420, 511, 41))
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.storagePathSelectionButton = QtWidgets.QPushButton(parent=self.tab)
        self.storagePathSelectionButton.setGeometry(QtCore.QRect(440, 510, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.storagePathSelectionButton.setFont(font)
        self.storagePathSelectionButton.setObjectName("storagePathSelectionButton")
        self.keywordFilePathOutput = QtWidgets.QTextBrowser(parent=self.tab)
        self.keywordFilePathOutput.setGeometry(QtCore.QRect(440, 150, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.keywordFilePathOutput.setFont(font)
        self.keywordFilePathOutput.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.keywordFilePathOutput.setLineWrapMode(QtWidgets.QTextEdit.LineWrapMode.NoWrap)
        self.keywordFilePathOutput.setObjectName("keywordFilePathOutput")
        self.keywordSetsPathOutput = QtWidgets.QTextBrowser(parent=self.tab)
        self.keywordSetsPathOutput.setGeometry(QtCore.QRect(440, 310, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.keywordSetsPathOutput.setFont(font)
        self.keywordSetsPathOutput.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.keywordSetsPathOutput.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.keywordSetsPathOutput.setLineWrapMode(QtWidgets.QTextEdit.LineWrapMode.NoWrap)
        self.keywordSetsPathOutput.setObjectName("keywordSetsPathOutput")
        self.storagePathOutput = QtWidgets.QTextBrowser(parent=self.tab)
        self.storagePathOutput.setGeometry(QtCore.QRect(440, 470, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.storagePathOutput.setFont(font)
        self.storagePathOutput.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.storagePathOutput.setLineWrapMode(QtWidgets.QTextEdit.LineWrapMode.NoWrap)
        self.storagePathOutput.setObjectName("storagePathOutput")
        self.label_3 = QtWidgets.QLabel(parent=self.tab)
        self.label_3.setGeometry(QtCore.QRect(290, 30, 521, 61))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.selectKeywordFilesLabel_2 = QtWidgets.QLabel(parent=self.tab)
        self.selectKeywordFilesLabel_2.setGeometry(QtCore.QRect(410, 260, 291, 41))
        self.selectKeywordFilesLabel_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.selectKeywordFilesLabel_2.setObjectName("selectKeywordFilesLabel_2")
        self.keywordFileProgressBar = QtWidgets.QProgressBar(parent=self.tab)
        self.keywordFileProgressBar.setGeometry(QtCore.QRect(440, 230, 221, 16))
        font = QtGui.QFont()
        font.setPointSize(1)
        self.keywordFileProgressBar.setFont(font)
        self.keywordFileProgressBar.setProperty("value", 0)
        self.keywordFileProgressBar.setTextVisible(False)
        self.keywordFileProgressBar.setObjectName("keywordFileProgressBar")
        self.keywordSetsProgressBar = QtWidgets.QProgressBar(parent=self.tab)
        self.keywordSetsProgressBar.setGeometry(QtCore.QRect(440, 390, 221, 16))
        font = QtGui.QFont()
        font.setPointSize(1)
        self.keywordSetsProgressBar.setFont(font)
        self.keywordSetsProgressBar.setProperty("value", 0)
        self.keywordSetsProgressBar.setTextVisible(False)
        self.keywordSetsProgressBar.setObjectName("keywordSetsProgressBar")
        self.storagePathProgressBar = QtWidgets.QProgressBar(parent=self.tab)
        self.storagePathProgressBar.setGeometry(QtCore.QRect(440, 550, 221, 16))
        font = QtGui.QFont()
        font.setPointSize(1)
        self.storagePathProgressBar.setFont(font)
        self.storagePathProgressBar.setProperty("value", 0)
        self.storagePathProgressBar.setTextVisible(False)
        self.storagePathProgressBar.setObjectName("storagePathProgressBar")
        self.label_5 = QtWidgets.QLabel(parent=self.tab)
        self.label_5.setGeometry(QtCore.QRect(1000, 600, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.tabWidget.addTab(self.tab, "")
        self.MainScraper = QtWidgets.QWidget()
        self.MainScraper.setToolTipDuration(-1)
        self.MainScraper.setObjectName("MainScraper")
        self.keywordlistWidget = QtWidgets.QListWidget(parent=self.MainScraper)
        self.keywordlistWidget.setGeometry(QtCore.QRect(610, 180, 321, 221))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.keywordlistWidget.setFont(font)
        self.keywordlistWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.MultiSelection)
        self.keywordlistWidget.setObjectName("keywordlistWidget")
        self.setSelectionDropdown = QtWidgets.QComboBox(parent=self.MainScraper)
        self.setSelectionDropdown.setGeometry(QtCore.QRect(200, 370, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.setSelectionDropdown.setFont(font)
        self.setSelectionDropdown.setCurrentText("")
        self.setSelectionDropdown.setObjectName("setSelectionDropdown")
        self.setSelectionDropdown.addItem("")
        self.setSelectionDropdown.setItemText(0, "")
        self.setSelectionLabel = QtWidgets.QLabel(parent=self.MainScraper)
        self.setSelectionLabel.setGeometry(QtCore.QRect(190, 330, 361, 31))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.setSelectionLabel.setFont(font)
        self.setSelectionLabel.setObjectName("setSelectionLabel")
        self.keywordListLabel = QtWidgets.QLabel(parent=self.MainScraper)
        self.keywordListLabel.setGeometry(QtCore.QRect(610, 145, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.keywordListLabel.setFont(font)
        self.keywordListLabel.setObjectName("keywordListLabel")
        self.searchButton = QtWidgets.QPushButton(parent=self.MainScraper)
        self.searchButton.setGeometry(QtCore.QRect(500, 550, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        self.searchButton.setFont(font)
        self.searchButton.setObjectName("searchButton")
        self.keywordInclusivecheckBox = QtWidgets.QCheckBox(parent=self.MainScraper)
        self.keywordInclusivecheckBox.setGeometry(QtCore.QRect(610, 480, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.keywordInclusivecheckBox.setFont(font)
        self.keywordInclusivecheckBox.setObjectName("keywordInclusivecheckBox")
        self.textSearchLabel = QtWidgets.QLabel(parent=self.MainScraper)
        self.textSearchLabel.setGeometry(QtCore.QRect(180, 420, 331, 41))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.textSearchLabel.setFont(font)
        self.textSearchLabel.setObjectName("textSearchLabel")
        self.HSIScraperlabel = QtWidgets.QLabel(parent=self.MainScraper)
        self.HSIScraperlabel.setGeometry(QtCore.QRect(350, 10, 411, 101))
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setBold(True)
        self.HSIScraperlabel.setFont(font)
        self.HSIScraperlabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.HSIScraperlabel.setObjectName("HSIScraperlabel")
        self.websiteSelectionDropdown = QtWidgets.QComboBox(parent=self.MainScraper)
        self.websiteSelectionDropdown.setGeometry(QtCore.QRect(200, 190, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.websiteSelectionDropdown.setFont(font)
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
        self.websiteSelectionLabel.setGeometry(QtCore.QRect(190, 155, 291, 31))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.websiteSelectionLabel.setFont(font)
        self.websiteSelectionLabel.setObjectName("websiteSelectionLabel")
        self.searchTextBox = QtWidgets.QLineEdit(parent=self.MainScraper)
        self.searchTextBox.setGeometry(QtCore.QRect(200, 460, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.searchTextBox.setFont(font)
        self.searchTextBox.setText("")
        self.searchTextBox.setObjectName("searchTextBox")
        self.selectAllKeywordscheckBox = QtWidgets.QCheckBox(parent=self.MainScraper)
        self.selectAllKeywordscheckBox.setGeometry(QtCore.QRect(610, 410, 361, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.selectAllKeywordscheckBox.setFont(font)
        self.selectAllKeywordscheckBox.setObjectName("selectAllKeywordscheckBox")
        self.paymentMethodcheckBox = QtWidgets.QCheckBox(parent=self.MainScraper)
        self.paymentMethodcheckBox.setGeometry(QtCore.QRect(610, 440, 481, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.paymentMethodcheckBox.setFont(font)
        self.paymentMethodcheckBox.setObjectName("paymentMethodcheckBox")
        self.setlocationDropdown = QtWidgets.QComboBox(parent=self.MainScraper)
        self.setlocationDropdown.setGeometry(QtCore.QRect(200, 280, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.setlocationDropdown.setFont(font)
        self.setlocationDropdown.setCurrentText("")
        self.setlocationDropdown.setObjectName("setlocationDropdown")
        self.setLocationLabel = QtWidgets.QLabel(parent=self.MainScraper)
        self.setLocationLabel.setGeometry(QtCore.QRect(190, 240, 291, 31))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.setLocationLabel.setFont(font)
        self.setLocationLabel.setObjectName("setLocationLabel")
        self.label_6 = QtWidgets.QLabel(parent=self.MainScraper)
        self.label_6.setGeometry(QtCore.QRect(1000, 600, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.tabWidget.addTab(self.MainScraper, "")
        self.EditKeywords = QtWidgets.QWidget()
        self.EditKeywords.setObjectName("EditKeywords")
        self.setList = QtWidgets.QListWidget(parent=self.EditKeywords)
        self.setList.setGeometry(QtCore.QRect(660, 230, 311, 181))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.setList.setFont(font)
        self.setList.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.setList.setObjectName("setList")
        self.newSetTextBox = QtWidgets.QLineEdit(parent=self.EditKeywords)
        self.newSetTextBox.setGeometry(QtCore.QRect(660, 189, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.newSetTextBox.setFont(font)
        self.newSetTextBox.setObjectName("newSetTextBox")
        self.addKeywordButton = QtWidgets.QPushButton(parent=self.EditKeywords)
        self.addKeywordButton.setGeometry(QtCore.QRect(330, 169, 131, 32))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.addKeywordButton.setFont(font)
        self.addKeywordButton.setObjectName("addKeywordButton")
        self.newKeywordTextBox = QtWidgets.QLineEdit(parent=self.EditKeywords)
        self.newKeywordTextBox.setGeometry(QtCore.QRect(150, 169, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.newKeywordTextBox.setFont(font)
        self.newKeywordTextBox.setObjectName("newKeywordTextBox")
        self.keywordList = QtWidgets.QListWidget(parent=self.EditKeywords)
        self.keywordList.setGeometry(QtCore.QRect(150, 210, 311, 201))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.keywordList.setFont(font)
        self.keywordList.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.MultiSelection)
        self.keywordList.setObjectName("keywordList")
        self.removeKeywordButton = QtWidgets.QPushButton(parent=self.EditKeywords)
        self.removeKeywordButton.setGeometry(QtCore.QRect(200, 420, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.removeKeywordButton.setFont(font)
        self.removeKeywordButton.setObjectName("removeKeywordButton")
        self.newKeywordLabel = QtWidgets.QLabel(parent=self.EditKeywords)
        self.newKeywordLabel.setGeometry(QtCore.QRect(140, 135, 211, 31))
        self.newKeywordLabel.setObjectName("newKeywordLabel")
        self.newSetLabel = QtWidgets.QLabel(parent=self.EditKeywords)
        self.newSetLabel.setGeometry(QtCore.QRect(660, 154, 261, 31))
        self.newSetLabel.setObjectName("newSetLabel")
        self.addSetButton = QtWidgets.QPushButton(parent=self.EditKeywords)
        self.addSetButton.setGeometry(QtCore.QRect(870, 189, 101, 32))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.addSetButton.setFont(font)
        self.addSetButton.setObjectName("addSetButton")
        self.removeSetButton = QtWidgets.QPushButton(parent=self.EditKeywords)
        self.removeSetButton.setGeometry(QtCore.QRect(720, 419, 191, 32))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.removeSetButton.setFont(font)
        self.removeSetButton.setObjectName("removeSetButton")
        self.newSetLabel_2 = QtWidgets.QLabel(parent=self.EditKeywords)
        self.newSetLabel_2.setGeometry(QtCore.QRect(660, 120, 411, 31))
        self.newSetLabel_2.setObjectName("newSetLabel_2")
        self.label_2 = QtWidgets.QLabel(parent=self.EditKeywords)
        self.label_2.setGeometry(QtCore.QRect(90, 470, 451, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(parent=self.EditKeywords)
        self.label_4.setGeometry(QtCore.QRect(260, 10, 591, 81))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_7 = QtWidgets.QLabel(parent=self.EditKeywords)
        self.label_7.setGeometry(QtCore.QRect(1000, 600, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.tabWidget.addTab(self.EditKeywords, "")

        self.retranslateUi(HSIWebScraper)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(HSIWebScraper)

    def retranslateUi(self, HSIWebScraper):
        _translate = QtCore.QCoreApplication.translate
        HSIWebScraper.setWindowTitle(_translate("HSIWebScraper", "NetSpider"))
        self.setFileSelectionButton.setText(_translate("HSIWebScraper", "Select keyword_sets.txt"))
        self.keywordfileSelectionButton.setText(_translate("HSIWebScraper", "Select keywords.txt"))
        self.selectKeywordFilesLabel.setText(_translate("HSIWebScraper", "Select keyword file:"))
        self.label.setText(_translate("HSIWebScraper", "Select folder to store screenshots and csv file:"))
        self.storagePathSelectionButton.setText(_translate("HSIWebScraper", "Select folder to store files"))
        self.keywordFilePathOutput.setPlaceholderText(_translate("HSIWebScraper", "No file chosen"))
        self.keywordSetsPathOutput.setPlaceholderText(_translate("HSIWebScraper", "No file chosen"))
        self.storagePathOutput.setPlaceholderText(_translate("HSIWebScraper", "No folder chosen"))
        self.label_3.setText(_translate("HSIWebScraper", "Choose file settings for scraper."))
        self.selectKeywordFilesLabel_2.setText(_translate("HSIWebScraper", "Select keyword sets file:"))
        self.label_5.setText(_translate("HSIWebScraper", "NetSpider v1.0.0"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("HSIWebScraper", "Settings"))
        self.setSelectionLabel.setText(_translate("HSIWebScraper", "  Select set of keywords (optional):"))
        self.keywordListLabel.setText(_translate("HSIWebScraper", "List of keywords:"))
        self.searchButton.setText(_translate("HSIWebScraper", "Search"))
        self.keywordInclusivecheckBox.setText(_translate("HSIWebScraper", "Keyword inclusive search (AND)."))
        self.textSearchLabel.setText(_translate("HSIWebScraper", "   Type text to scrape (optional):"))
        self.HSIScraperlabel.setText(_translate("HSIWebScraper", "Web Scraper"))
        self.websiteSelectionDropdown.setItemText(1, _translate("HSIWebScraper", "escortalligator"))
        self.websiteSelectionDropdown.setItemText(2, _translate("HSIWebScraper", "megapersonals"))
        self.websiteSelectionDropdown.setItemText(3, _translate("HSIWebScraper", "skipthegames"))
        self.websiteSelectionDropdown.setItemText(4, _translate("HSIWebScraper", "yesbackpage"))
        self.websiteSelectionDropdown.setItemText(5, _translate("HSIWebScraper", "eros"))
        self.websiteSelectionLabel.setText(_translate("HSIWebScraper", "  Select website to scrape:"))
        self.searchTextBox.setPlaceholderText(_translate("HSIWebScraper", " Type text to search here. "))
        self.selectAllKeywordscheckBox.setText(_translate("HSIWebScraper", "Select all keywords from list."))
        self.paymentMethodcheckBox.setText(_translate("HSIWebScraper", "Find only posts with payment methods."))
        self.setLocationLabel.setText(_translate("HSIWebScraper", "  Select location:"))
        self.label_6.setText(_translate("HSIWebScraper", "NetSpider v1.0.0"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.MainScraper), _translate("HSIWebScraper", "Scraper"))
        self.newSetTextBox.setPlaceholderText(_translate("HSIWebScraper", " Type new set name."))
        self.addKeywordButton.setText(_translate("HSIWebScraper", "Add keyword"))
        self.newKeywordTextBox.setPlaceholderText(_translate("HSIWebScraper", " Type new keyword."))
        self.removeKeywordButton.setText(_translate("HSIWebScraper", "Remove selected keyword"))
        self.newKeywordLabel.setText(_translate("HSIWebScraper", " Enter new keyword:"))
        self.newSetLabel.setText(_translate("HSIWebScraper", "Enter new set name:"))
        self.addSetButton.setText(_translate("HSIWebScraper", "Add set"))
        self.removeSetButton.setText(_translate("HSIWebScraper", "Remove selected set"))
        self.newSetLabel_2.setText(_translate("HSIWebScraper", "Select keywords from list on the left."))
        self.label_2.setText(_translate("HSIWebScraper", "Warning: Remove only one keyword at a time."))
        self.label_4.setText(_translate("HSIWebScraper", "Edit keywords and sets for scraper."))
        self.label_7.setText(_translate("HSIWebScraper", "NetSpider v1.0.0"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.EditKeywords), _translate("HSIWebScraper", "Edit Keywords"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    HSIWebScraper = QtWidgets.QWidget()
    ui = Ui_HSIWebScraper()
    ui.setupUi(HSIWebScraper)
    HSIWebScraper.show()
    sys.exit(app.exec())
