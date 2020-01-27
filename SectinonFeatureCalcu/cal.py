# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 14:59:07 2019

@author: 2273
"""

import sys,os
#if hasattr(sys, 'frozen'):
#    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from uifea.ui import Ui_Form
#import images
from PyQt5 import QtGui
from PyQt5.Qt import QIcon
from PyQt5.QtWidgets import QWidget, QApplication
import numpy as np
import math
import base64
from images import logo

class MainWin(QWidget,Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Subchange")
        tmp = open("tmp.ico","wb+")
        tmp.write(base64.b64decode(logo))
        tmp.close()
        #maindir,mainfile=os.path.split(os.path.abspath(sys.argv[0]))  #获取主执行文件所处的文件夹的绝对路径及文件名
        #logodir=os.path.normpath(os.path.join(maindir,'img/logo.jpg'))  #获取logo绝对路径
        self.setWindowIcon(QIcon("tmp.ico"))
        os.remove("tmp.ico")
        self.pushButton_1.clicked.connect(calcu_reponse)
        self.pushButton_2.clicked.connect(clear_reponse)
        self.DataModel = QtGui.QStandardItemModel()
        #设置数据头栏名称
        self.DataModel.setHorizontalHeaderItem(0, QtGui.QStandardItem("截面特性"))
        self.DataModel.setHorizontalHeaderItem(1, QtGui.QStandardItem("值."))
        for i in range(1,9):
                for j in range(2):
                    self.DataModel.setItem(i, j, QtGui.QStandardItem(""))
        self.tableView.setModel(self.DataModel)
        # 设置列宽
        self.tableView.setColumnWidth(0,108)
        self.tableView.setColumnWidth(1,150)
    
    
def GetData():
    EditData = []
    EditData.append(float(Win.lineEdit_1.text()))
    EditData.append(float(Win.lineEdit_2.text()))
    EditData.append(float(Win.lineEdit_3.text()))
    EditData.append(float(Win.lineEdit_4.text()))
    EditData.append(float(Win.lineEdit_5.text()))
    EditData.append(float(Win.lineEdit_6.text()))
    EditData.append(float(Win.lineEdit_7.text()))
    EditData.append(float(Win.lineEdit_8.text()))
    EditData.append(float(Win.lineEdit_9.text()))
    EditData.append(float(Win.lineEdit_10.text()))
    EditData.append(float(Win.lineEdit_11.text()))
    
    # 按照分层法处理数据
    b = np.zeros((2,7)) # 上结线
    b[0,0] = EditData[0]
    b[1,0] = EditData[0]
    b[0,1] = EditData[2]+EditData[3]+EditData[4]
    b[1,1] = EditData[3]
    b[0,2] = EditData[3]
    b[1,2] = EditData[3]
    b[0,3] = EditData[3]
    b[1,3] = EditData[5]
    b[0,4] = EditData[5]
    b[1,4] = EditData[5]
    h = EditData[7:11]
    h.append(EditData[6]-(EditData[7]+EditData[8]+EditData[9]+EditData[10]))
    return b,h

def calcu_reponse():

    try:
        #LisEdit = ['lineEdit','lineEdit_2','lineEdit_3','lineEdit_4','lineEdit_5','lineEdit_6','lineEdit_7','lineEdit_8']
        b,h = GetData()
        # 分块面积
        area = np.zeros(5)
        for i in range(5):
            area[i] = (b[0,i]+b[1,i])*h[i]/2
        AreaAll = sum(area)
        #print(area)
        
        # 分块形心距离下边缘的距离
        y = np.zeros(5)
        for i in range(4):
            y[i] = h[i]/3*(2*b[0,i]+b[1,i])/(b[0,i]+b[1,i])+sum(h[i+1:])
        y[4] = h[4]/3*(2*b[0,4]+b[1,4])/(b[0,4]+b[1,4])
        #print(h)
        #print(y)
        #截面形心距离边缘的距离
        yb = area.dot(y)/AreaAll #下距离
        yt = sum(h) - yb #上距离
        
        
        # 截面对自身x-x轴的惯性矩
        MomentInteriax_x = np.zeros(5)
        for i in range(5):
            MomentInteriax_x[i] = math.pow(h[i],3)/(36*(b[0,i]+b[1,i]))*(b[0,i]**2+4*b[0,i]*b[1,i]+b[1,i]**2)
        
        # 截面对形心轴的净距
        StaticMoment = np.zeros(6)
        for i in range(1,6):
            StaticMoment[i] = StaticMoment[i-1]+area[i-1]*(y[i-1]-yb)  #从1开始记录数据
        
        # 移轴的惯性矩
        MomentInteriax_c = np.zeros(5)
        for i in range(5):
            MomentInteriax_c[i] = area[i]*(y[i]-yb)**2
        
        MomentInteria = sum(MomentInteriax_x) + sum(MomentInteriax_c)
            
        #tableview显示数据
        Win.DataModel.setItem(0, 0, QtGui.QStandardItem("A(mm^2)"))
        Win.DataModel.setItem(0, 1, QtGui.QStandardItem(str(round(AreaAll,3))))
        #print(AreaAll)
    		
        Win.DataModel.setItem(1, 0, QtGui.QStandardItem("yb(mm)"))
        Win.DataModel.setItem(1, 1, QtGui.QStandardItem(str(round(yb,3))))
        
        Win.DataModel.setItem(2, 0, QtGui.QStandardItem("yt(mm)"))
        Win.DataModel.setItem(2, 1, QtGui.QStandardItem(str(round(yt,3))))
        
        Win.DataModel.setItem(3, 0, QtGui.QStandardItem("Ix-x(mm^4)"))
        Win.DataModel.setItem(3, 1, QtGui.QStandardItem(str(round(MomentInteria,3))))
        
        
        for i in range(4,9):
            Win.DataModel.setItem(i, 0, QtGui.QStandardItem("S"+str(i-3)+"-"+str(i-3)))
            Win.DataModel.setItem(i, 1, QtGui.QStandardItem(str(round(StaticMoment[i-3],3))))
            #print(StaticMoment[i-3])
        
    except ValueError as e:
        Win.DataModel.setItem(0, 0, QtGui.QStandardItem("ValueError"))
        Win.DataModel.setItem(0, 1, QtGui.QStandardItem(str(e)))
        for i in range(1,9):
            for j in range(2):
                Win.DataModel.setItem(i, j, QtGui.QStandardItem(""))
        #print('ValueError:', e)
    finally:
        Win.tableView.setModel(Win.DataModel)


def clear_reponse():
    Win.lineEdit_1.setText('')
    Win.lineEdit_2.setText('')
    Win.lineEdit_3.setText('')
    Win.lineEdit_4.setText('')
    Win.lineEdit_5.setText('')
    Win.lineEdit_6.setText('')
    Win.lineEdit_7.setText('')
    Win.lineEdit_8.setText('')
    Win.lineEdit_9.setText('')
    Win.lineEdit_10.setText('')
    Win.lineEdit_11.setText('')
    for i in range(0,9):
                for j in range(2):
                    Win.DataModel.setItem(i, j, QtGui.QStandardItem(""))
    Win.tableView.setModel(Win.DataModel)
     
     
if __name__ == '__main__':
    app = QApplication(sys.argv)
    Win = MainWin()
    Win.show()
    sys.exit(app.exec_())
    