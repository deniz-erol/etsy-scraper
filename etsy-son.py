## This is a work in progress. Not all functions work as intended yet.


import urllib.request
from bs4 import BeautifulSoup
import pymysql.cursors
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableView, QApplication
from PyQt5.QtCore import QAbstractTableModel, Qt
import pandas as pd


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(710, 699)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 711, 741))
        self.widget.setObjectName("widget")
        self.dbButton = QtWidgets.QPushButton(self.widget)
        self.dbButton.setGeometry(QtCore.QRect(490, 10, 201, 31))
        self.dbButton.setObjectName("dbButton")
        self.productInput = QtWidgets.QLineEdit(self.widget)
        self.productInput.setGeometry(QtCore.QRect(10, 10, 481, 31))
        self.productInput.setAccessibleDescription("")
        self.productInput.setAutoFillBackground(False)
        self.productInput.setInputMask("")
        self.productInput.setText("")
        self.productInput.setReadOnly(False)
        self.productInput.setObjectName("productInput")
        self.idSearch = QtWidgets.QLineEdit(self.widget)
        self.idSearch.setGeometry(QtCore.QRect(10, 50, 151, 31))
        self.idSearch.setObjectName("idSearch")
        self.idSearchButton = QtWidgets.QPushButton(self.widget)
        self.idSearchButton.setGeometry(QtCore.QRect(170, 50, 201, 31))
        self.idSearchButton.setObjectName("idSearchButton")
        self.tableView = QtWidgets.QTableView(self.widget)
        self.tableView.setGeometry(QtCore.QRect(10, 90, 691, 561))
        self.tableView.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableView.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tableView.setLineWidth(1)
        self.tableView.setObjectName("tableView")
        self.tableView.verticalHeader().setStretchLastSection(True)
        self.getAll = QtWidgets.QPushButton(self.widget)
        self.getAll.setGeometry(QtCore.QRect(410, 660, 141, 31))
        self.getAll.setObjectName("getAll")
        self.clearAll = QtWidgets.QPushButton(self.widget)
        self.clearAll.setGeometry(QtCore.QRect(560, 660, 141, 31))
        self.clearAll.setObjectName("clearAll")
        self.getAll.raise_()
        self.clearAll.raise_()
        self.tableView.raise_()
        self.idSearch.raise_()
        self.productInput.raise_()
        self.dbButton.raise_()
        self.idSearchButton.raise_()
        MainWindow.setCentralWidget(self.centralwidget)


        self.retranslateUi(MainWindow)
        self.productInput.returnPressed.connect(self.dbButton.click)
        self.idSearch.returnPressed.connect(self.idSearchButton.click)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.dbButton.clicked.connect(self.linkass)
        self.dbButton.clicked.connect(self.dbinsert)

        self.getAll.clicked.connect(self.getall)
        #self.getAll.clicked.connect(self.pandasModel)

        self.idSearchButton.clicked.connect(self.getID)
        self.idSearchButton.clicked.connect(self.getone)


    def linkass(self):
        self.URL = self.productInput.text()
        self.productInput.clear()

    def dbinsert(self):
        page = urllib.request.urlopen(self.URL)
        soup = BeautifulSoup(page.read(), "html.parser")

        name = soup.find('h1', class_='wt-text-body-03 wt-line-height-tight wt-break-word wt-mb-xs-1').text.strip()
        price = soup.find('p', class_='wt-text-title-03 wt-mr-xs-2').text.strip()
        pimage = soup.find('img', class_='wt-max-width-full wt-horizontal-center wt-vertical-center carousel-image wt-rounded')
        image = str(pimage["data-src-zoom-image"])

        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='deniz',
                                     password='12151621',
                                     database='etsy',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        # Insert into MySQL table
        with connection:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `scrape_table` (`name`, `price`, `image`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (name, price, image))
            connection.commit()

    def getID(self):
        self.PID = self.idSearch.text()
        self.idSearch.clear()

    def getone(self):
        connection = pymysql.connect(host='localhost',
                                     user='deniz',
                                     password='12151621',
                                     database='etsy',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        with connection:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM `scrape_table` WHERE `product_id` =%s"
                cursor.execute(sql, self.PID)
                resultone = cursor.fetchone()
            print(resultone)

    def getall(self):
        connection = pymysql.connect(host='localhost',
                                     user='deniz',
                                     password='12151621',
                                     database='etsy',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)


        with connection:
            with connection.cursor() as cursor:
                # Read all
                sql = "SELECT * FROM `scrape_table`"
                cursor.execute(sql, )
                self.resultall = cursor.fetchall()
            print(self.resultall)

        # self.df = pd.DataFrame(self.resultall)
        # self.model = pandasModel(self.df)
        # self.tableView.setModel(self.model)

    # def createdf(self):
           # self.path = self.result.text()
            #self.df = pd.DataFrame(self.result)
            #model = PandasModel(df)
            #self.tableView.setModel(model)

 # class pandasModel(QAbstractTableModel):
 #
 #        def __init__(self, data):
 #            QAbstractTableModel.__init__(self)
 #            self._data = data
 #
 #        def rowCount(self, parent=None):
 #            return self._data.shape[0]
 #
 #        def columnCount(self, parnet=None):
 #            return self._data.shape[1]
 #
 #        def data(self, index, role=Qt.DisplayRole):
 #            if index.isValid():
 #                if role == Qt.DisplayRole:
 #                    return str(self._data.iloc[index.row(), index.column()])
 #            return None
 #
 #        def headerData(self, col, orientation, role):
 #            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
 #                return self._data.columns[col]
 #            return None




    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.dbButton.setText(_translate("MainWindow", "Add product to Database"))
        self.productInput.setPlaceholderText(_translate("MainWindow", "Input your Etsy link here."))
        self.idSearch.setPlaceholderText(_translate("MainWindow", "Search with Product ID."))
        self.idSearchButton.setText(_translate("MainWindow", "Search with ID"))
        self.getAll.setText(_translate("MainWindow", "Show all Products"))
        self.clearAll.setText(_translate("MainWindow", "Clear Table"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


# model = pandasModel(df)
    # view = QTableView()
    # view.setModel(model)
    # view.resize(800, 600)
    # view.show()
