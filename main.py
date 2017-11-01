import subprocess

import os

import re

import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QAction, QTableWidgetItem, QTableView, QHeaderView, QItemDelegate, QAbstractItemView, \
    QMessageBox

from mainwindow import Ui_MainWindow


class MyWin(QtWidgets.QMainWindow):
    dirList = []

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
        subprocess.call("lsblk -p | grep 'sd[^a][0-9]' > " + os.getcwd() + "/log.txt", shell=True)
        logfile = open(os.getcwd() + "/log.txt", "r+")
        usbList = []
        for i in logfile:
            s = re.split(r" +",i)
            dev = s[0][s[0].index("/"):]
            flag = -1
            usbList.append(dev)
            for index in range(self.ui.tableWidget.rowCount()):
                if (self.ui.tableWidget.item(index, 0) != None):
                    if (self.ui.tableWidget.item(index, 0).text() == dev):
                        flag = index
            if (flag == -1):
                mount = s[6]
                subprocess.call("df -hm | grep " + dev + " > " + os.getcwd() + "/memory.txt", shell=True)
                memoryfile = open(os.getcwd() + "/memory.txt")

            # saving memory
                memdict = {"all": 0, "free": 0, "used": 0}
                line = memoryfile.readline()
                result = re.split(r" +", line)
                if (len(result) >= 3):
                    memdict["all"] = memdict["all"] + int(result[1])
                    memdict["used"] = memdict["used"] + int(result[2])
                    memdict["free"] = memdict["free"] + int(result[3])
                    self.appendText(dev, mount, str(memdict["free"]) + "/" + str(memdict["used"]) + "/" + str(memdict["all"]))
                memoryfile.close()
        for i in range(0, self.ui.tableWidget.rowCount()):
            if (self.ui.tableWidget.item(i,0) != None):
                if (not (self.ui.tableWidget.item(i,0).text() in usbList)):
                    self.ui.tableWidget.removeRow(i)
        logfile.close()

    def clearTable(self):
        self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setRowCount(1)

    def eject(self):
        indexes = self.ui.tableWidget.selectionModel().selectedRows()
        for index in sorted(indexes):
            subprocess.call("eject " + self.ui.tableWidget.item(index.row(),0).text() + " > " + os.getcwd() + "/eject.txt", shell=True)
            ejectFile = open(os.getcwd() + "/eject.txt", "r+")
            message = ejectFile.read()
            if (message != None):
                error = QMessageBox(self)
                error.setText(message)


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
