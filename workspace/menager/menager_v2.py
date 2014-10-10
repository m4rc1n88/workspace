from PyQt4 import QtGui, QtCore, uic
import sys
from sh import ps
from PyQt4.QtCore import *
import time

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

"""

class NumberSortModel(QtGui.QSortFilterProxyModel):
    def __init__(self, parent=None):
        QtGui.QSortFilterProxyModel.__init__(self, parent)

    def lessThan(self, left, right):
        try:
            return float( left.data()) > float( right.data() )
        except ValueError:
            return left.data() > right.data()
        
#        lvalue = left.data().toDouble()[0]
#        rvalue = right.data().toDouble()[0]
#        return lvalue < rvalue

"""

class WatekTest(QtCore.QThread):
    signalUpdateProcess = QtCore.pyqtSignal()
    #co wpisac w nawias
    def __init__(self,data):
        #na razie chuj znajet co znaczy data ale chyba klasa okna
        super(WatekTest,self).__init__()
        self.data=data
        
    def run(self):
        while True:
            #tableData1=self.data.getProcessInformation()
            
            self.signalUpdateProcess.emit(self.data)
            #self.data._model.update(tableData1)
            time.sleep(1)
        


class ProcessTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data = [[QObject]], headers = [], parent = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.__data = data
        self.__headers=headers


    def update(self, dataIn):
        print 'Updating Model'
        self.layoutAboutToBeChanged.emit()
        self.__data = dataIn
        self.layoutChanged.emit()
        


    def rowCount(self, parent):
        return len(self.__data)
    
    
    def columnCount(self, parent):
        return len(self.__data[0])


    def flags(self, index):
        return  QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        
        if role == QtCore.Qt.DisplayRole:
            
            if orientation == QtCore.Qt.Horizontal:
                
                if section < len(self.__headers):
                    return self.__headers[section]
                else:
                    return "not implemented"


    def data(self,index,role):
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            
            row = index.row()
            column = index.column()
            value = self.__data[row][column]
            
            return value



#Create windof from ui
base, form = uic.loadUiType("menager.ui")
class MenagerWindow(base,form):
    def __init__(self, parent=None):
        super(base, self).__init__(parent)
        self.setupUi(self)
        self._proxyModel = QtGui.QSortFilterProxyModel()
        headers = ["Process Name", "User", "CPU %", "MEM %", "PID"]
#        tableData0 = [ [ QtGui.QColor("#FFFF00") for i in range(columnCount)] for j in range(rowCount)]
        self.tableData0=self.getProcessInformation()
#        print tableData0
        self._model = ProcessTableModel(self.tableData0, headers)
        self._proxyModel.setSourceModel(self._model)
        self._proxyModel.setDynamicSortFilter(True)
        self.uiTable.setModel(self._proxyModel)
        self.uiTable.setSortingEnabled(True)
        QtCore.QObject.connect(self.uiFillterProcess, QtCore.SIGNAL("textChanged(QString)"), self.procesFilter)
        QtCore.QObject.connect(self.uiFillterUser, QtCore.SIGNAL("textChanged(QString)"), self.userFilter)
        QtCore.QObject.connect(self.uiRefreshButton,QtCore.SIGNAL("clicked()"),self.refreshProcessInformation)
        self.actionUpdateProcess = QtGui.QAction(self)
        self.actionUpdateProcess.triggered.connect(self.updateProcess)
        self.updateProcess()



    def getProcessInformation(self):
        lista=ps("-aux").split("\n")
#        print lista;
        data=[]
        for kolumna in lista[1:-1]:
            kolumna=kolumna.split()

            data.append([kolumna[10],kolumna[0],float(kolumna[2]),float(kolumna[3]),int(kolumna[1])])
        print kolumna[10],kolumna[0],kolumna[2],kolumna[3],kolumna[1]
        return data
                               
    @pyqtSlot()
    def refreshProcessInformation(self):
        tableData1=self.getProcessInformation()
        self._model.update(tableData1)
        self.watek=WatekTest(self)
        self.watek.start()
    @pyqtSlot()   
    def updateProcess(self):
        tableData1=self.getProcessInformation()
        self.watek = WatekTest(tableData1)
        self.watek.signalUpdateProcess.connect(self.updated)
        self.watek.start()
        
    def updated(self,tableData1):
        self.tableData0=tableData1

    @pyqtSlot('QString')
    def userFilter(self, arg1):
        self._proxyModel.setFilterKeyColumn(int(1));
        self._proxyModel.setFilterRegExp(arg1)

    @pyqtSlot('QString')
    def procesFilter(self, arg1):
        self._proxyModel.setFilterKeyColumn(int(0));
        self._proxyModel.setFilterRegExp(arg1)



if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
#    app.setStyle("cleanlooks")
    

    wnd = MenagerWindow()
    wnd.show()


    sys.exit(app.exec_())
