# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
import numpy as np
import sys
import time
import pylab
import matplotlib.pyplot as plt
import copy
import cProfile
import re
import line_profiler
from PyQt5 import QtCore, QtGui, QtWidgets
import proj_part6 as opt



class Ui_Dialog(object):

    trigger = QtCore.pyqtSignal(str)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1101, 937)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 1081, 211))
        self.groupBox.setObjectName("groupBox")
        self.inputorders = QtWidgets.QLineEdit(self.groupBox)
        self.inputorders.setGeometry(QtCore.QRect(100, 180, 951, 20))
        self.inputorders.setObjectName("inputorders")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 100, 71, 21))
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(310, 140, 41, 21))
        self.label_4.setObjectName("label_4")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 140, 71, 21))
        self.label_3.setObjectName("label_3")
        self.startpoint = QtWidgets.QLineEdit(self.groupBox)
        self.startpoint.setGeometry(QtCore.QRect(100, 140, 101, 21))
        self.startpoint.setObjectName("startpoint")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 20, 71, 21))
        self.label.setObjectName("label")
        self.orderlist = QtWidgets.QLineEdit(self.groupBox)
        self.orderlist.setGeometry(QtCore.QRect(100, 100, 951, 20))
        self.orderlist.setObjectName("orderlist")
        self.endpoint = QtWidgets.QLineEdit(self.groupBox)
        self.endpoint.setGeometry(QtCore.QRect(380, 140, 101, 21))
        self.endpoint.setObjectName("endpoint")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(10, 180, 71, 21))
        self.label_5.setObjectName("label_5")
        self.warehousedata = QtWidgets.QLineEdit(self.groupBox)
        self.warehousedata.setGeometry(QtCore.QRect(100, 20, 951, 20))
        self.warehousedata.setObjectName("warehousedata")
        self.dimension = QtWidgets.QLineEdit(self.groupBox)
        self.dimension.setGeometry(QtCore.QRect(100, 60, 951, 20))
        self.dimension.setObjectName("dimension")
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        self.label_12.setGeometry(QtCore.QRect(10, 60, 71, 21))
        self.label_12.setObjectName("label_12")
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 230, 1081, 121))
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(10, 40, 71, 21))
        self.label_6.setObjectName("label_6")
        self.comboAlgorithm = QtWidgets.QComboBox(self.groupBox_2)
        self.comboAlgorithm.setGeometry(QtCore.QRect(100, 40, 171, 22))
        self.comboAlgorithm.setObjectName("comboAlgorithm")
        self.comboAlgorithm.addItem("")
        self.comboAlgorithm.addItem("")
        self.comboAlgorithm.addItem("")
        self.comboAlgorithm.addItem("")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(300, 40, 121, 21))
        self.label_7.setObjectName("label_7")
        self.textOptN = QtWidgets.QLineEdit(self.groupBox_2)
        self.textOptN.setGeometry(QtCore.QRect(420, 40, 81, 21))
        self.textOptN.setObjectName("textOptN")
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setGeometry(QtCore.QRect(520, 40, 151, 21))
        self.label_8.setObjectName("label_8")
        self.textK = QtWidgets.QLineEdit(self.groupBox_2)
        self.textK.setGeometry(QtCore.QRect(670, 40, 51, 21))
        self.textK.setObjectName("textK")
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setGeometry(QtCore.QRect(10, 80, 161, 21))
        self.label_9.setObjectName("label_9")
        self.comboCombine = QtWidgets.QComboBox(self.groupBox_2)
        self.comboCombine.setGeometry(QtCore.QRect(190, 80, 131, 22))
        self.comboCombine.setObjectName("comboCombine")
        self.comboCombine.addItem("")
        self.comboCombine.addItem("")
        self.label_10 = QtWidgets.QLabel(self.groupBox_2)
        self.label_10.setGeometry(QtCore.QRect(730, 40, 241, 21))
        self.label_10.setObjectName("label_10")
        self.textWeight = QtWidgets.QLineEdit(self.groupBox_2)
        self.textWeight.setGeometry(QtCore.QRect(970, 40, 91, 21))
        self.textWeight.setObjectName("textWeight")
        self.pushRun = QtWidgets.QPushButton(self.groupBox_2)
        self.pushRun.setGeometry(QtCore.QRect(975, 80, 81, 21))
        self.pushRun.setObjectName("pushRun")
        self.pushReset = QtWidgets.QPushButton(self.groupBox_2)
        self.pushReset.setGeometry(QtCore.QRect(870, 80, 81, 21))
        self.pushReset.setObjectName("pushReset")
        self.pushFind = QtWidgets.QPushButton(self.groupBox_2)
        self.pushFind.setGeometry(QtCore.QRect(765, 80, 81, 21))
        self.pushFind.setObjectName("pushFind")
        self.label_11 = QtWidgets.QLabel(self.groupBox_2)
        self.label_11.setGeometry(QtCore.QRect(390, 80, 111, 21))
        self.label_11.setObjectName("label_11")
        self.textOrder = QtWidgets.QLineEdit(self.groupBox_2)
        self.textOrder.setGeometry(QtCore.QRect(500, 80, 191, 21))
        self.textOrder.setObjectName("textOrder")
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(10, 360, 1061, 561))
        self.textBrowser.setObjectName("textBrowser")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(490, 360, 601, 561))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame.raise_()
        self.groupBox.raise_()
        self.groupBox_2.raise_()
        self.textBrowser.raise_()

        self.retranslateUi(Dialog)
        self.pushReset.clicked.connect(self.textBrowser.clear)
        self.warehousedata.editingFinished.connect(self.whdata)
        self.dimension.editingFinished.connect(self.ddata)
        self.orderlist.editingFinished.connect(self.listdata)
        self.startpoint.editingFinished.connect(self.stp)
        self.endpoint.editingFinished.connect(self.edp)
        self.inputorders.editingFinished.connect(self.inorders)
        self.comboAlgorithm.currentIndexChanged['int'].connect(self.algorithm)
        self.textOptN.editingFinished.connect(self.optN)
        self.textK.editingFinished.connect(self.bnbK)
        self.textWeight.editingFinished.connect(self.maxw)
        self.comboCombine.currentIndexChanged['int'].connect(self.comborders)
        self.textOrder.editingFinished.connect(self.historder)
        self.pushFind.clicked.connect(self.find)
        self.pushReset.clicked.connect(self.reset)
        self.pushRun.clicked.connect(self.run)
        # self.trigger.connect(self.qtprint)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def qtprint(self, string):
        self.textBrowser.append(string)
        # self.textBrowser.insertPlainText(string)


    def whdata(self):
        text=self.warehousedata.text()
        opt.warehouseData = np.loadtxt(text, delimiter=',', unpack=False)
        opt.warehouseData = np.row_stack((opt.startPoint, opt.warehouseData, opt.endPoint))
        opt.warehouseIndex = opt.warehouseData[:, 0]
        opt.warehouseDict = dict(zip(opt.warehouseIndex, opt.warehouseData[:, 0:]))
        print("New data ",text," is ready")
        return

    def ddata(self):
        text = self.dimension.text()
        opt.dementionData = np.loadtxt(text, delimiter='\t', skiprows=1, unpack=False)
        opt.dementionIndex = opt.dementionData[:, 0]
        opt.dementionDict = dict(zip(opt.dementionIndex, opt.dementionData[:, 1:]))
        print("New data ", text, " is ready")
        return

    def listdata(self):
        text = self.orderlist.text()
        opt.orderList = open(text)
        opt.orderList = opt.orderList.readlines()
        opt.orderInput = np.array([np.append(opt.startPoint, [0, 0, 0, 0])])
        print("New data ", text, " is ready")
        return

    def stp(self):
        text = self.startpoint.text()
        opt.startPoint = text.split(",")
        opt.startPoint = [int(opt.startPoint[i]) for i in range(len(opt.startPoint))]
        opt.startPoint.insert(0, 0)
        opt.orderInput[0]=np.array([np.append(opt.startPoint, [0, 0, 0, 0])])
        print("New start point ", opt.startPoint, " is ready")
        return

    def edp(self):
        text = self.endpoint.text()
        opt.endPoint = text.split(",")
        opt.endPoint = [int(opt.endPoint[i]) for i in range(len(opt.endPoint))]
        opt.endPoint.insert(0, opt.dummyEnd)
        print("New end point ", opt.endPoint, " is ready")
        return

    def inorders(self):
        text = self.inputorders.text()
        opt.getorder = text.split(",")
        opt.orderbatch = []
        opt.orderbatch = opt.transOrderNum(opt.getorder, opt.orderbatch)
        print("New input orders ", opt.orderbatch, " is set")
        return

    def algorithm(self, num):
        opt.modeNum = int(num) +1
        return

    def optN(self):
        text = self.textOptN.text()
        opt.optN = int(text)
        # print(opt.optN)
        return

    def bnbK(self):
        text = self.textK.text()
        opt.bnbk = int(text)
        # print(opt.bnbk)
        return

    def maxw(self):
        text = self.textWeight.text()
        opt.cartcapacity = int(text)
        # print(opt.cartcapacity)
        return

    def comborders(self, num):
        opt.batchmode = num
        return

    def historder(self):
        text = self.textOrder.text()
        opt.historder = int(text)
        return

    def find(self):
        return

    def reset(self):
        return

    def run(self):
        if opt.batchmode == 0:
            self.inorders()
            orderWeight = opt.orderWeightCal(opt.orderbatch)
            weight = np.array(orderWeight)
            weight = weight[np.lexsort(weight.T)]
            captmp = opt.cartcapacity
            weight = weight.tolist()
            print(weight)
            while len(weight):
                order = []
                for i in range(len(weight) - 1, -1, -1):
                    if captmp >= weight[i][1]:
                        captmp -= weight[i][1]
                        order.append(weight[i][0])
                        weight.pop(i)
                captmp = opt.cartcapacity
                print("Combine orders:", order)
                self.qtprint("#" + str(opt.figureNum))
                self.qtprint("Combine orders:"+str(order))
                opt.orderInput = opt.orderCombineData(order, opt.orderInput)
                if opt.modeNum == 1:
                    distHistory, bestPath, ttPathEff, ttrePathEff, timecost = opt.opt2(opt.orderInput)
                    self.qtprint("2-opt bestPath: " + str(bestPath))
                    self.qtprint("2-opt total distance :" + str(distHistory))
                    self.qtprint("2-opt total effort: " + str(ttPathEff))
                    self.qtprint("2-opt reverse effort: " + str(ttrePathEff))
                    self.qtprint("2-opt timecost: " + str(timecost))
                if opt.modeNum == 2:
                    distHistory, bestPath, ttPathEff, ttrePathEff, timecost = opt.efftopt2(opt.orderInput)
                    self.qtprint("2-effort-opt bestPath: " + str(bestPath))
                    self.qtprint("2-effort-opt total distance :" + str(distHistory))
                    self.qtprint("2-effort-opt total effort: " + str(ttPathEff))
                    self.qtprint("2-effort-opt reverse effort: " + str(ttrePathEff))
                    self.qtprint("2-effort-opt timecost: " + str(timecost))
                if opt.modeNum == 3:
                    # self.bnbK()
                    distHistory, bestPath, ttPathEff, ttrePathEff, timecost = opt.bnbktest(opt.bnbk, opt.orderInput)
                    self.qtprint("bnbk bestPath: " + str(bestPath))
                    self.qtprint("bnbk total distance :" + str(distHistory))
                    self.qtprint("bnbk total effort: " + str(ttPathEff))
                    self.qtprint("bnbk reverse effort: " + str(ttrePathEff))
                    self.qtprint("bnbk timecost: " + str(timecost))
                if opt.modeNum == 4:
                    distHistory, bestPath, ttPathEff, ttrePathEff, timecost = opt.opt2(opt.orderInput)
                    self.qtprint("2-opt bestPath: " + str(bestPath))
                    self.qtprint("2-opt total distance :" + str(distHistory))
                    self.qtprint("2-opt total effort: " + str(ttPathEff))
                    self.qtprint("2-opt reverse effort: " + str(ttrePathEff))
                    self.qtprint("2-opt timecost: " + str(timecost))
                    distHistory, bestPath, ttPathEff, ttrePathEff, timecost = opt.efftopt2(opt.orderInput)
                    self.qtprint("2-effort-opt bestPath: " + str(bestPath))
                    self.qtprint("2-effort-opt total distance :" + str(distHistory))
                    self.qtprint("2-effort-opt total effort: " + str(ttPathEff))
                    self.qtprint("2-effort-opt reverse effort: " + str(ttrePathEff))
                    self.qtprint("2-effort-opt timecost: " + str(timecost))
                    distHistory, bestPath, ttPathEff, ttrePathEff, timecost = opt.bnbktest(1, opt.orderInput)
                    self.qtprint("bnb1 bestPath: " + str(bestPath))
                    self.qtprint("bnb1 total distance :" + str(distHistory))
                    self.qtprint("bnb1 total effort: " + str(ttPathEff))
                    self.qtprint("bnb1 reverse effort: " + str(ttrePathEff))
                    self.qtprint("bnb1 timecost: " + str(timecost))
                    distHistory, bestPath, ttPathEff, ttrePathEff, timecost = opt.bnbktest(2, opt.orderInput)
                    self.qtprint("bnb2 bestPath: " + str(bestPath))
                    self.qtprint("bnb2 total distance :" + str(distHistory))
                    self.qtprint("bnb2 total effort: " + str(ttPathEff))
                    self.qtprint("bnb2 reverse effort: " + str(ttrePathEff))
                    self.qtprint("bnb2 timecost: " + str(timecost))
                    distHistory, bestPath, ttPathEff, ttrePathEff, timecost = opt.bnbktest(3, opt.orderInput)
                    self.qtprint("bnb3 bestPath: " + str(bestPath))
                    self.qtprint("bnb3 total distance :" + str(distHistory))
                    self.qtprint("bnb3 total effort: " + str(ttPathEff))
                    self.qtprint("bnb3 reverse effort: " + str(ttrePathEff))
                    self.qtprint("bnb3 timecost: " + str(timecost))
        else:
            for i in opt.orderbatch:
                opt.orderInput = opt.orderPrepare(i)
                if opt.modeNum == 1:
                    distHistory, bestPath, ttPathEff, ttrePathEff, timecost = opt.opt2(opt.orderInput)
                    self.qtprint("2-opt bestPath: " + str(bestPath))
                    self.qtprint("2-opt total distance :" + str(distHistory))
                    self.qtprint("2-opt total effort: " + str(ttPathEff))
                    self.qtprint("2-opt reverse effort: " + str(ttrePathEff))
                    self.qtprint("2-opt timecost: " + str(timecost))
                if opt.modeNum == 2:
                    distHistory, bestPath, ttPathEff, ttrePathEff, timecost = opt.efftopt2(opt.orderInput)
                    self.qtprint("2-effort-opt bestPath: " + str(bestPath))
                    self.qtprint("2-effort-opt total distance :" + str(distHistory))
                    self.qtprint("2-effort-opt total effort: " + str(ttPathEff))
                    self.qtprint("2-effort-opt reverse effort: " + str(ttrePathEff))
                    self.qtprint("2-effort-opt timecost: " + str(timecost))
                if opt.modeNum == 3:
                    # self.bnbK()
                    distHistory, bestPath, ttPathEff, ttrePathEff, timecost = opt.bnbktest(opt.bnbk, opt.orderInput)
                    self.qtprint("bnbk bestPath: " + str(bestPath))
                    self.qtprint("bnbk total distance :" + str(distHistory))
                    self.qtprint("bnbk total effort: " + str(ttPathEff))
                    self.qtprint("bnbk reverse effort: " + str(ttrePathEff))
                    self.qtprint("bnbk timecost: " + str(timecost))
                if opt.modeNum == 4:
                    distHistory, bestPath, ttPathEff, ttrePathEff, timecost = opt.opt2(opt.orderInput)
                    self.qtprint("2-opt bestPath: " + str(bestPath))
                    self.qtprint("2-opt total distance :" + str(distHistory))
                    self.qtprint("2-opt total effort: " + str(ttPathEff))
                    self.qtprint("2-opt reverse effort: " + str(ttrePathEff))
                    self.qtprint("2-opt timecost: " + str(timecost))
                    distHistory, bestPath, ttPathEff, ttrePathEff, timecost = opt.efftopt2(opt.orderInput)
                    self.qtprint("2-effort-opt bestPath: " + str(bestPath))
                    self.qtprint("2-effort-opt total distance :" + str(distHistory))
                    self.qtprint("2-effort-opt total effort: " + str(ttPathEff))
                    self.qtprint("2-effort-opt reverse effort: " + str(ttrePathEff))
                    self.qtprint("2-effort-opt timecost: " + str(timecost))
                    distHistory, bestPath, ttPathEff, ttrePathEff, timecost = opt.bnbktest(1, opt.orderInput)
                    self.qtprint("bnb1 bestPath: " + str(bestPath))
                    self.qtprint("bnb1 total distance :" + str(distHistory))
                    self.qtprint("bnb1 total effort: " + str(ttPathEff))
                    self.qtprint("bnb1 reverse effort: " + str(ttrePathEff))
                    self.qtprint("bnb1 timecost: " + str(timecost))
                    distHistory, bestPath, ttPathEff, ttrePathEff, timecost = opt.bnbktest(2, opt.orderInput)
                    self.qtprint("bnb2 bestPath: " + str(bestPath))
                    self.qtprint("bnb2 total distance :" + str(distHistory))
                    self.qtprint("bnb2 total effort: " + str(ttPathEff))
                    self.qtprint("bnb2 reverse effort: " + str(ttrePathEff))
                    self.qtprint("bnb2 timecost: " + str(timecost))
                    distHistory, bestPath, ttPathEff, ttrePathEff, timecost = opt.bnbktest(3, opt.orderInput)
                    self.qtprint("bnb3 bestPath: " + str(bestPath))
                    self.qtprint("bnb3 total distance :" + str(distHistory))
                    self.qtprint("bnb3 total effort: " + str(ttPathEff))
                    self.qtprint("bnb3 reverse effort: " + str(ttrePathEff))
                    self.qtprint("bnb3 timecost: " + str(timecost))
        return


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "Data Input"))
        self.inputorders.setText(_translate("Dialog", "1,2,3:9,10"))
        self.label_2.setText(_translate("Dialog", "Order List File"))
        self.label_4.setText(_translate("Dialog", "End Point"))
        self.label_3.setText(_translate("Dialog", "Start Point"))
        self.startpoint.setText(_translate("Dialog", "0,0"))
        self.label.setText(_translate("Dialog", "Warehouse data"))
        self.orderlist.setText(_translate("Dialog", "warehouse-orders-v01.csv"))
        self.endpoint.setText(_translate("Dialog", "0,0"))
        self.label_5.setText(_translate("Dialog", "Input Orders"))
        self.warehousedata.setText(_translate("Dialog", "warehouse-grid.csv"))
        self.dimension.setText(_translate("Dialog", "item-dimensions-tabbed.txt"))
        self.label_12.setText(_translate("Dialog", "Dimension Data"))
        self.groupBox_2.setTitle(_translate("Dialog", "Algorithm Configuration"))
        self.label_6.setText(_translate("Dialog", "Algorithm:"))
        self.comboAlgorithm.setItemText(0, _translate("Dialog", "2-opt (distance)"))
        self.comboAlgorithm.setItemText(1, _translate("Dialog", "2-opt (effort)"))
        self.comboAlgorithm.setItemText(2, _translate("Dialog", "BnB k-layer"))
        self.comboAlgorithm.setItemText(3, _translate("Dialog", "Test bench (all algorithms)"))
        self.label_7.setText(_translate("Dialog", "N value (for 2-opt)"))
        self.textOptN.setText(_translate("Dialog", "50"))
        self.label_8.setText(_translate("Dialog", "K value (for BnB-k)"))
        self.textK.setText(_translate("Dialog", "2"))
        self.label_9.setText(_translate("Dialog", "Combine orders :"))
        self.comboCombine.setItemText(0, _translate("Dialog", "Yes"))
        self.comboCombine.setItemText(1, _translate("Dialog", "No"))
        self.label_10.setText(_translate("Dialog", "Max Weight (for combined orders):"))
        self.textWeight.setText(_translate("Dialog", "34"))
        self.pushRun.setText(_translate("Dialog", "Run"))
        self.pushReset.setText(_translate("Dialog", "Reset"))
        self.pushFind.setText(_translate("Dialog", "Find"))
        self.label_11.setText(_translate("Dialog", "Find in History："))
        self.textOrder.setText(_translate("Dialog", "1"))

