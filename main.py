import subprocess

import os

import re

import sys
from USBAdapter import UsbAdapter
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtWidgets import QAction, QTableWidgetItem, QTableView, QHeaderView, QItemDelegate, QAbstractItemView, \
    QMessageBox, QApplication, QMainWindow

from mainwindow import Ui_MainWindow


class MyWin(QtWidgets.QMainWindow):
    dirList = []
    usbAdapter = UsbAdapter()

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tableWidget.setColumnCount(3)
        self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
        header1 = QTableWidgetItem("name")
        header2 = QTableWidgetItem("directory")
        header3 = QTableWidgetItem("size: free/used/all (M)")
        self.ui.tableWidget.setHorizontalHeaderItem(0,header1)
        self.ui.tableWidget.setHorizontalHeaderItem(1,header2)
        self.ui.tableWidget.setHorizontalHeaderItem(2,header3)

        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        headers = self.ui.tableWidget.horizontalHeader()
        headers.setStretchLastSection(True)
        self.ui.tableWidget.setRowCount(0)

        self.ui.ejectButton.clicked.connect(self.eject)

    #action of refreshing all window
    def refresh(self):
        print("refresh")
        pass

    #close action
    def closeEvent(self, event):
        event.accept()

    def appendText(self, name, directory, size):
        item1 = QTableWidgetItem(name)
        item1.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item2 = QTableWidgetItem(directory)
        item2.setFlags(QtCore.Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item3 = QTableWidgetItem(size)
        item3.setFlags(QtCore.Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        table = self.ui.tableWidget

        item = table.item(table.rowCount()-1,0)
        if (item != None):

            table.insertRow(table.rowCount())
        if (table.rowCount() == 0):
            table.setRowCount(1)
        table.setItem(table.rowCount() - 1, 0, item1)
        table.setItem(table.rowCount() - 1, 1, item2)
        table.setItem(table.rowCount() - 1, 2, item3)

    def refreshDirectories(self):
        #self.clearTable()
        usbList = self.usbAdapter.getUsbList()
        mtpList = self.usbAdapter.mtpDevice()
        usbList = usbList + mtpList
        nameList = []
        flag = -1
        for usbInfo in usbList:
            nameList.append(usbInfo["name"])
            for index in range(self.ui.tableWidget.rowCount()):
                if (self.ui.tableWidget.item(index, 0) != None):
                    if (self.ui.tableWidget.item(index, 0).text() == usbInfo["name"]):
                        flag = index
            if (flag == -1):
                if (usbInfo != None):
                    self.appendText(usbInfo["name"], usbInfo["mountPoint"], str((usbInfo["size"])["free"]) + "/" + str((usbInfo["size"])["used"]) + "/" + str((usbInfo["size"])["all"]))
            else:
                self.updateRow(index, usbInfo)


        for i in range(0, self.ui.tableWidget.rowCount()):
            if (self.ui.tableWidget.item(i,0) != None):
                if (not (self.ui.tableWidget.item(i,0).text() in nameList)):
                    self.ui.tableWidget.removeRow(i)

    def clearTable(self):
        self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setRowCount(1)

    def eject(self):
        indexes = self.ui.tableWidget.selectionModel().selectedRows()
        for index in sorted(indexes):
            message = self.usbAdapter.eject(self.ui.tableWidget.item(index.row(), 0).text())
            self.errorInfo(message)


    def errorInfo(self, message):
        if (message != None):
            self.ui.infoLabel.setText("info: " + message)

    def updateRow(self, row, usbInfo):
        item1 = QTableWidgetItem(usbInfo["name"])
        item1.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item2 = QTableWidgetItem(usbInfo["mountPoint"])
        item2.setFlags(QtCore.Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item3 = QTableWidgetItem(str((usbInfo["size"])["free"]) + "/" + str((usbInfo["size"])["used"]) + "/" + str((usbInfo["size"])["all"]))
        item3.setFlags(QtCore.Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        table = self.ui.tableWidget

        if (row < table.rowCount()):
            table.setItem(row, 0, item1)
            table.setItem(row, 1, item2)
            table.setItem(row, 2, item3)

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWin()
    window.show()


    #creating timer for refresh main window
    timer = QTimer()
    timer.timeout.connect(window.refreshDirectories)
    timer.start(1000)

    sys.exit(app.exec_())
    exit()
