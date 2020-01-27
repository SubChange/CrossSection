# -*- coding: utf-8 -*-

import sys
import os
from uidesign.boxui import Ui_Form
from PyQt5 import QtGui
from PyQt5.Qt import QIcon
from PyQt5.QtWidgets import QWidget, QApplication
import numpy as np
import base64
from images import logo

class MainWin(QWidget,Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Subchange")
        # 载入图片作为图标
        tmp = open("tmp.jpg","wb+")
        tmp.write(base64.b64decode(logo))
        tmp.close()
        self.setWindowIcon(QIcon("tmp.jpg"))
        os.remove("tmp.jpg")
        
        # 建立点击信号与槽的连接
        self.pushButton_1.clicked.connect(self.calcu_reponse)
        self.pushButton.clicked.connect(lambda:self.clear_reponse(16))
        
        self.DataModel = QtGui.QStandardItemModel()
        #设置数据头栏名称
        self.DataModel.setHorizontalHeaderItem(0, QtGui.QStandardItem("截面特性"))
        self.DataModel.setHorizontalHeaderItem(1, QtGui.QStandardItem("值."))
        self.DataModel.setItem(0, 0, QtGui.QStandardItem("A(mm^2)"))
        self.DataModel.setItem(1, 0, QtGui.QStandardItem("yb(mm)"))
        self.DataModel.setItem(2, 0, QtGui.QStandardItem("yu(mm)"))
        self.DataModel.setItem(3, 0, QtGui.QStandardItem("Ix-x(mm^4)"))

        for i in range(4,16+4):
                self.DataModel.setItem(i, 0, QtGui.QStandardItem("Area"+str(i-4)+"/y"+str(i-4)))

        for i in range(20):
                for j in range(1,2):
                    self.DataModel.setItem(i, j, QtGui.QStandardItem(""))

        # 设置列宽
        self.tableView.setColumnWidth(0,130)
        self.tableView.setColumnWidth(1,170)

        self.tableView.setModel(self.DataModel)

        # 获取输入数据
    def GetData(self):
        EditData = []
        for i in range(1,17):
            try:
                eval("EditData.append(float(self.lineEdit_"+str(i)+".text()))") 
            except ValueError as e:
                EditData.append(0)
        return EditData
        
    # 将输入数据转为顺序坐标 
    def Data2coor(self,Data):
        coorout = np.zeros([2,10])
        coorout[:,0] = [0,0]
        coorout[:,1] = [2*Data[11],0]
        coorout[:,2] = [2*Data[11]+Data[10],Data[2]]
        coorout[:,3] = [2*Data[11]+Data[10]+Data[9],Data[2]+Data[1]]
        coorout[:,4] = [2*Data[11]+Data[10]+Data[9]+Data[8],Data[2]+Data[1]]
        coorout[:,5] = [2*Data[11]+Data[10]+Data[9]+Data[8],Data[2]+Data[1]+Data[0]]
        coorout[:,6] = [-(Data[10]+Data[9]+Data[8]),Data[2]+Data[1]+Data[0]]
        coorout[:,7] = [-(Data[10]+Data[9]+Data[8]),Data[2]+Data[1]]
        coorout[:,8] = [-(Data[10]+Data[9]),Data[2]+Data[1]]
        coorout[:,9] = [-Data[10],Data[2]]
        
        coorin = np.zeros([2,8])
        coorin[:,0] = [Data[11]-Data[13],Data[6]+Data[7]]
        coorin[:,1] = [Data[11]-Data[14],Data[5]+Data[6]+Data[7]]
        coorin[:,2] = [Data[11]-Data[15],Data[4]+Data[5]+Data[6]+Data[7]]
        coorin[:,3] = [Data[11]+Data[15],Data[4]+Data[5]+Data[6]+Data[7]]
        coorin[:,4] = [Data[11]+Data[14],Data[5]+Data[6]+Data[7]]
        coorin[:,5] = [Data[11]+Data[13],Data[6]+Data[7]]
        coorin[:,6] = [Data[11]+Data[12],Data[7]]
        coorin[:,7] = [Data[11]-Data[12],Data[7]]
        #print(coorout)
        #print(coorin)
        return coorout,coorin


    def FeaCalcu(self,coorout,coorin):
        area = []
        y = []
        moment = []
        n = coorout.shape[1]
        for i in range(1,n-1):
            x2 = coorout[0,i]
            y2 = coorout[1,i]
            x3 = coorout[0,i+1]
            y3 = coorout[1,i+1]
            area.append(0.5*(x2*y3-x3*y2))
            y.append((y2+y3)/3)
            moment.append(0.5*(x2*y3-x3*y2)/18*(y3**2-y2*y3+y2**2))

        n = coorin.shape[1]
        for i in range(0,n):
            x2 = coorin[0,i%n]
            y2 = coorin[1,i%n]
            x3 = coorin[0,(i+1)%n]
            y3 = coorin[1,(i+1)%n]
            area.append(0.5*(x2*y3-x3*y2))
            y.append((y2+y3)/3)
            moment.append(0.5*(x2*y3-x3*y2)/18*(y3**2-y2*y3+y2**2))


        AreaAll = sum(area)
        StaticMoment = np.array(area).dot(np.array(y))
        if AreaAll == 0:
            yb = 0
            yt = 0
        else:
            yb = StaticMoment/AreaAll
            H = max(coorout[1,:])
            yt = H - yb

        MomentOfInteria = 0
        for i in range(len(area)):
            MomentOfInteria = MomentOfInteria+moment[i]+area[i]*(y[i]-yb)**2
        return area,y,yb,yt,MomentOfInteria
        

    def calcu_reponse(self):
        try:
            Data = self.GetData()
            coorout,coorin = self.Data2coor(Data)
            area,y,yb,yt,MomentOfInteria = self.FeaCalcu(coorout,coorin)
            #tableview显示数据
            self.DataModel.setItem(0, 1, QtGui.QStandardItem(str(round(sum(area),3))))
            self.DataModel.setItem(1, 1, QtGui.QStandardItem(str(round(yb,3))))
            self.DataModel.setItem(2, 1, QtGui.QStandardItem(str(round(yt,3))))
            self.DataModel.setItem(3, 1, QtGui.QStandardItem(str(round(MomentOfInteria,3))))

            for i in range(4,16+4):
                self.DataModel.setItem(i, 0, QtGui.QStandardItem("Area"+str(i-4)+"/y"+str(i-4)))
                self.DataModel.setItem(i, 1, QtGui.QStandardItem(str(round(area[i-4],3))+"/"+str(round(y[i-4],3))))
            
        except ValueError as e:
            self.DataModel.setItem(0, 1, QtGui.QStandardItem("ValueError"))
            self.DataModel.setItem(1, 1, QtGui.QStandardItem(str(e)))
            for i in range(1,16+4):
                for j in range(1,2):
                    self.DataModel.setItem(i, j, QtGui.QStandardItem("Err"))
            #print('ValueError:', e)
        finally:
            self.tableView.setModel(self.DataModel)


    def clear_reponse(self,n):
        for k in range(1,17):
            eval("self.lineEdit_"+str(k)+".setText('')")
        for i in range(0,4+n):
                    for j in range(1,2):
                        self.DataModel.setItem(i, j, QtGui.QStandardItem(""))
        self.tableView.setModel(self.DataModel)
     
     
if __name__ == '__main__':
    app = QApplication(sys.argv)
    Win = MainWin()
    Win.show()
    sys.exit(app.exec_())