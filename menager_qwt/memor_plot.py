import PyQt4.Qwt5 as Qwt
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import *
import psutil






class MemoryPlot(Qwt.QwtPlot):
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
        self.connect(self,QtCore.SIGNAL('legendChecked(QwtPlotItem*, bool)'),self.showCurve) #przepisac na nowy styl
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