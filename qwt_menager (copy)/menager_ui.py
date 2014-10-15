# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'menager.ui'
#
# Created: Fri Sep 19 15:31:36 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.Qwt5 import QwtPlot
import sys

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.uiFillterProcess = QtGui.QLineEdit(self.tab)
        self.uiFillterProcess.setObjectName(_fromUtf8("uiFillterProcess"))
        self.horizontalLayout_2.addWidget(self.uiFillterProcess)
        self.uiFillterUser = QtGui.QLineEdit(self.tab)
        self.uiFillterUser.setObjectName(_fromUtf8("uiFillterUser"))
        self.horizontalLayout_2.addWidget(self.uiFillterUser)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.uiTable = QtGui.QTableView(self.tab)
        self.uiTable.setObjectName(_fromUtf8("uiTable"))
        self.verticalLayout_2.addWidget(self.uiTable)
        self.uiRefreshButton = QtGui.QPushButton(self.tab)
        self.uiRefreshButton.setObjectName(_fromUtf8("uiRefreshButton"))
        self.verticalLayout_2.addWidget(self.uiRefreshButton)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.tab_2)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        #self.qwtPlot = QwtPlot(self.tab_2)
        #self.qwtPlot.setObjectName(_fromUtf8("qwtPlot"))
        #self.horizontalLayout_3.addWidget(self.qwtPlot)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.uiRefreshButton.setText(_translate("MainWindow", "Refresh", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Processes", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Resources", None))

