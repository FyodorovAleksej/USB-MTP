import subprocess

import os

import re

import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QAction, QTableWidgetItem, QTableView, QHeaderView, QItemDelegate

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
        header3 = QTableWidgetItem("size")
        self.ui.tableWidget.setHorizontalHeaderItem(0,header1)
        self.ui.tableWidget.setHorizontalHeaderItem(1,header2)
        self.ui.tableWidget.setHorizontalHeaderItem(2,header3)

        headers = self.ui.tableWidget.horizontalHeader()
        headers.setStretchLastSection(True)


    #action of refreshing all window
    def refresh(self):
        print("refresh")
        pass

    #close action
    def closeEvent(self, event):
        event.accept()

    def appendText(self, name, directory, size):
        item1 = QTableWidgetItem(name)
        item1.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled|(not QtCore.Qt.ItemIsEditable))
        item2 = QTableWidgetItem(directory)
        item2.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled|(not QtCore.Qt.ItemIsEditable))
        item3 = QTableWidgetItem(size)
        item3.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled|(not QtCore.Qt.ItemIsEditable))
        table = self.ui.tableWidget
        item = table.item(table.rowCount()-1,0)
        if (item != None):
            table.insertRow(table.rowCount())
        table.setItem(table.rowCount() - 1, 0, item1)
        table.setItem(table.rowCount() - 1, 1, item2)
        table.setItem(table.rowCount() - 1, 2, item3)

    def refreshDirectories(self):
        subprocess.call("ls /media/alexey > " + os.getcwd() + "/log.txt", shell=True)
        logfile = open(os.getcwd() + "./log.txt", "r+")
        current = [i for i in logfile]
        for i in range(0, len(current)):
            if current[i] != self.dirList[i]:
                self.dirList = current
                return current[i]
        return None

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    #window = MyWin()

    #window.show()

    #creating timer for refresh main window
    #timer = QTimer()
    #timer.timeout.connect(window.refresh)
    #timer.start(100)




    sys.exit(app.exec_())
