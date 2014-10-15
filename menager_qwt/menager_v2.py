from PyQt4 import QtGui, QtCore, uic
#import sys
#from sh import ps
from PyQt4.QtCore import *
import time
import numpy
import PyQt4.Qwt5 as Qwt
from PyQt4.Qwt5 import *
from PyQt4.Qwt5.qplt import *
from PyQt4.Qwt5 import QwtPlot
from menager_ui import *
from PyQt4.Qwt5.anynumpy import *
import menager_ui
#import timeit

import psutil
from reportlab.graphics.widgets.grids import Grid


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

# class WatekTest(QtCore.QThread):

            
            


class WatekTestSignal(QtCore.QThread):
    signalUpdateProcess = QtCore.pyqtSignal(list)
    #co wpisac w nawias
    def __init__(self,parent=None):
        super(WatekTestSignal,self).__init__(parent)
        
    def run(self):
        while True:
            data=[]
            pids = psutil.pids()
            for pid in pids:
                try:
                    proces=psutil.Process(pid)
                    data.append([proces.name(),proces.username(),proces.cpu_percent(),proces.memory_percent(),pid])
                except NoSuchProcess:
                    print "zniknal proces"
            self.signalUpdateProcess.emit(data)
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


class CpuPlot(Qwt.QwtPlot):
    colors=[Qt.red,
              Qt.green,
              Qt.blue,
              Qt.cyan,
              Qt.magenta,
              Qt.yellow,
              Qt.darkBlue,
              Qt.darkGreen
              ] 
    data=[]

    def __init__(self, *args):
        Qwt.QwtPlot.__init__(self, *args)
        self.cpu_count=psutil.cpu_count()
        self.x = arange(-60,0, 1)
        self.cpu_percent=[]
        self.curve=[]
        legend = Qwt.QwtLegend()
        legend.setItemMode(Qwt.QwtLegend.CheckableItem)
        self.insertLegend(legend, Qwt.QwtPlot.RightLegend)
        for cpu_number in range(self.cpu_count):
            self.cpu_percent.append(0*self.x)
            self.curve.append(Qwt.QwtPlotCurve('CPU'+str(cpu_number)))
            self.curve[cpu_number].attach(self)
            self.curve[cpu_number].setData(self.x, self.cpu_percent[cpu_number])
            self.curve[cpu_number].setPen(QtGui.QPen(self.colors[cpu_number], 2))
            self.showCurve(self.curve[cpu_number], True)          
        
        #ustawienie osi
        self.setAxisScale(Qwt.QwtPlot.yLeft, 0, 100)
        self.setAxisTitle(Qwt.QwtPlot.yLeft, "Usage [%]")
                
        #Grid
        grid = Qwt.QwtPlotGrid()
        pen = QtGui.QPen(Qt.DotLine)
        pen.setColor(Qt.black)
        pen.setWidth(0)
        grid.setPen(pen)
        grid.attach(self)
        self.startTimer(1000)
        self.connect(self,QtCore.SIGNAL('legendChecked(QwtPlotItem*, bool)'),self.showCurve) #przepisac na nowy typ
        self.replot()
        
    def timerEvent(self, e):
        data=psutil.cpu_percent(0, percpu=True)        
        for cpu_number in range(self.cpu_count):
            self.cpu_percent[cpu_number][0]=data[cpu_number]
            self.cpu_percent[cpu_number]=numpy.roll(self.cpu_percent[cpu_number],-1)
            self.curve[cpu_number].setData(self.x,self.cpu_percent[cpu_number])
        self.replot()
            
        
    def showCurve(self, item, on):
        item.setVisible(on)
        widget = self.legend().find(item)
        if isinstance(widget, Qwt.QwtLegendItem):
            widget.setChecked(on)
        self.replot()
        
        
        


#Create window from ui
#base, form = uic.loadUiType("menager.ui")
class MenagerWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(QtGui.QMainWindow, self).__init__(parent)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
#        self.setupUi(self)
        self._proxyModel = QtGui.QSortFilterProxyModel()
        headers = ["Process Name", "User", "CPU %", "MEM %", "PID"]
#        tableData0 = [ [ QtGui.QColor("#FFFF00") for i in range(columnCount)] for j in range(rowCount)]
        self.tableData0=[] #self.getProcessInformation()
#        print tableData0
        self._model = ProcessTableModel(self.tableData0, headers)
        self._proxyModel.setSourceModel(self._model)
        self._proxyModel.setDynamicSortFilter(True)
        self.ui.uiTable.setModel(self._proxyModel)
        self.ui.uiTable.setSortingEnabled(True)
        QtCore.QObject.connect(self.ui.uiFillterProcess, QtCore.SIGNAL("textChanged(QString)"), self.procesFilter)
        QtCore.QObject.connect(self.ui.uiFillterUser, QtCore.SIGNAL("textChanged(QString)"), self.userFilter)
        #QtCore.QObject.connect(self.uiRefreshButton,QtCore.SIGNAL("clicked()"),self.refreshProcessInformation)
        self.actionUpdateProcess = QtGui.QAction(self)
        self.actionUpdateProcess.triggered.connect(self.updateProcess)
        
        self.actionUpadateWykres = QtGui.QAction(self)
        self.actionUpadateWykres.triggered.connect(self.updateWykres)
        
        self.updateProcess()
        #self.refreshProcessInformation()
        #self.updateProcess()
          # calculate 3 NumPy arrays
          
          
          
#''' urzycie procesora '''
#         self.cpu_count=psutil.cpu_count()
#         self.x = arange(-60,0, 1)
#         self.cpu_percent=[]
#         self.curve=[]
#         legend = Qwt.QwtLegend()
#         legend.setItemMode(Qwt.QwtLegend.CheckableItem)
#         self.ui.qwtPlot.insertLegend(legend, Qwt.QwtPlot.RightLegend)
#         for cpu_number in range(self.cpu_count):
#             self.cpu_percent.append(0*self.x)
#             self.curve.append(Qwt.QwtPlotCurve('CPU'+str(cpu_number)))
#             self.curve[cpu_number].attach(self.ui.qwtPlot)
#             self.curve[cpu_number].setData(self.x, self.cpu_percent[cpu_number])
#             self.showCurve(self.curve[cpu_number], True)
# 
#         
#         self.ui.qwtPlot.replot()
#         #self.ui.qwtPlot.legendChecked.connect(self.showCurve())
#         
#         QtCore.QObject.connect(self.ui.qwtPlot,QtCore.SIGNAL('legendChecked(QwtPlotItem*, bool)'),self.showCurve)
        self.cpu_plot=CpuPlot(self.ui.tab_2)
        self.ui.horizontalLayout_3.addWidget(self.cpu_plot)
        #self.updateWykres()
        
        
    @pyqtSlot()   
    def updateProcess(self):
        self.watek = WatekTestSignal()
        self.watek.signalUpdateProcess.connect(self.updated)
        self.watek.start()
        
    def updated(self,tableData1):
        self._model.update(tableData1)
        
        
        
    @pyqtSlot()
    def updateWykres(self):
        self.watekWykres = WatekTestWykres()
        self.watekWykres.signalUpdateWykres.connect(self.replot)
        self.watekWykres.start()
         
         
    def replot(self,data):
        self.cpu_plot.replot_wykres()
#sds
         
        

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