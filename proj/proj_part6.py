import numpy as np
import sys
import time
import pylab
import matplotlib.pyplot as plt
import copy
import cProfile
import re
import line_profiler
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QMessageBox, QVBoxLayout, QSizePolicy, QWidget
import ui

# qtCreatorFile = "ui.ui"
# using uic to load ui.ui
# Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

# import memory_profiler


###############################   Data Preparation   ##############################################
#   0       1     2   3      4       5        6       7
# Index:  Number   x   y   length   width   height   weigh
#
#
#
#
#####################################################################################################
dummyEnd = int(999999)
distHistory = [1]
efftHistory = [1]
ndistHistory = []
cartweight = 0
cartcapacity = 99999
getorder = []
orderbatch = []
modeNum = 1
optdepth = int(8000)
optN=34
bnbk=2
batchmode=0
historder=0


startPoint = np.array([])
endPoint = np.array([])
# strfile = input("Hello user, where is your worker? (format: 0,0)");
# startPoint = strfile.split(",")
# startPoint = [int(startPoint[i]) for i in range(len(startPoint))]
startPoint=[0,0]
startPoint.insert(0, 0)  # dummy item/position
# strfile = input("Where is your worker's end location? (format: 0,0)");
# endPoint = strfile.split(",")
# endPoint = [int(endPoint[i]) for i in range(len(endPoint))]
endPoint=[0,0]
endPoint.insert(0, dummyEnd)  # dummy item/position
#print("startPoint", startPoint)
#print("endPoint", endPoint)
# strfile = input("Which order?");
# orderLineNum = int(strfile)-1

warehouseData = np.loadtxt('warehouse-grid.csv', delimiter=',', unpack=False)
warehouseData = np.row_stack((startPoint, warehouseData, endPoint))
warehouseIndex = warehouseData[:, 0]
warehouseDict = dict(zip(warehouseIndex, warehouseData[:, 0:]))

dementionData = np.loadtxt('item-dimensions-tabbed.txt', delimiter='\t', skiprows=1, unpack=False)
dementionIndex = dementionData[:, 0]
dementionDict = dict(zip(dementionIndex, dementionData[:, 1:]))

orderList = open('warehouse-orders-v01.csv')
orderList = orderList.readlines()
orderInput = np.array([np.append(startPoint, [0, 0, 0, 0])])


def orderPrepare(orderLineNum):
    orderInput = np.array([np.append(startPoint, [0, 0, 0, 0])])
    order = orderList[orderLineNum].split('\t')
    while '' in order:
        order.remove('')
    while '\n' in order:
        order.remove('\n')
    order = [int(x) for x in order]
    itemNum = len(order)
    print("Default order: ", order)
    for i in order:
        if i in dementionDict:
            orderInput = np.row_stack((orderInput, np.append(warehouseDict[i], dementionDict[i])))
        else:
            orderInput = np.row_stack((orderInput, np.append(warehouseDict[i], [0, 0, 0, 0])))
            print("Missing item dimension: ", i)
    orderInput = orderInput[np.lexsort(orderInput[:, 0:3].T)]
    orderInput = np.row_stack((orderInput, np.append(endPoint, [0, 0, 0, 0])))
    optdepth = int(8000)
    if itemNum <= 100:
        optdepth = int(optN*120)
    if itemNum <= 50:
        optdepth = int(optN*40)
    if itemNum <= 35:
        optdepth = int(optN*24)
    if itemNum <= 20:
        optdepth = int(optN*16)
    if itemNum <= 10:
        optdepth = int(optN*8)
    if itemNum <= 3:
        optdepth = optN
    print(orderInput)
    return orderInput

def orderCombineData(orderbatch,orderInput):
    orderInput = np.array([np.append(startPoint, [0, 0, 0, 0])])
    itemNum = len(orderbatch)
    for i in orderbatch:
        order = orderList[int(i)].split('\t')
        while '' in order:
            order.remove('')
        while '\n' in order:
            order.remove('\n')
        order = [int(x) for x in order]
        itemNum = len(order)
        print("Default order: ", order)
        for j in order:
            if j in dementionDict:
                orderInput = np.row_stack((orderInput, np.append(warehouseDict[j], dementionDict[j])))
            else:
                orderInput = np.row_stack((orderInput, np.append(warehouseDict[j], [0, 0, 0, 0])))
    orderInput = orderInput[np.lexsort(orderInput[:, 0:3].T)]
    orderInput = np.row_stack((orderInput, np.append(endPoint, [0, 0, 0, 0])))
    optdepth = int(8000)
    if itemNum <= 100:
        optdepth = int(optN*120)
    if itemNum <= 50:
        optdepth = int(optN*40)
    if itemNum <= 35:
        optdepth = int(optN*24)
    if itemNum <= 20:
        optdepth = int(optN*16)
    if itemNum <= 10:
        optdepth = int(optN*8)
    if itemNum <= 3:
        optdepth = optN
    return orderInput


######################################  Effort Calculation #############################################

def calEff(num1, num2, weight):
    weight = weight + orderInput[num2][6]
    dy = abs(orderInput[num1][2] - orderInput[num2][2])
    if int(orderInput[num1][2]) == int(orderInput[num2][2]):
        dx = abs(orderInput[num1][1] - orderInput[num2][1])
    else:
        if int(orderInput[num1][1]) == int(orderInput[num2][1]):
            dx = (orderInput[num1][1] % 1 + orderInput[num2][1] % 1)
            if dx > 1:
                dx = 2 - dx
        else:
            dx = abs(orderInput[num1][1] - orderInput[num2][1])
    dist = dx + dy
    efft = dist * weight
    return dist, efft, weight


def ttPathEff(optPath):
    distsum = 0.0
    efftsum = 0.0
    weight = cartweight
    for i in range(1, len(optPath)):
        sumtmp, effttmp, weight = calEff(optPath[i], optPath[i - 1], weight)
        distsum += sumtmp
        efftsum += effttmp
    return distsum, efftsum


# if path1 better/shotter than path2, then return true
def pathEffCompare(path1, path2):
    distsum1, efftsum1 = ttPathEff(path1)
    distsum2, efftsum2 = ttPathEff(path2)
    if efftsum1 <= efftsum2:
        return True
    return False


def efftOpt(bestPath):
    count = optdepth
    while count:
        distsum, efftsum = ttPathEff(bestPath)
        # print(efftsum)
        distHistory.append(efftsum)
        start, end, path = genRandomPath(bestPath)
        rePath = reversePath(path)
        if pathEffCompare(path, rePath):
            count -= 1
            continue
        else:
            count = optdepth
            bestPath[start:end + 1] = rePath
    return bestPath


def efftOpt2ed(bestPath):
    count = int(optdepth)
    while count:
        rePath = bestPath.copy()
        distsum, efftsum = ttPathEff(bestPath)
        distHistory.append(distsum)
        efftHistory.append(efftsum)
        start1, end1, path1 = genRandomPath(rePath)
        rePath[start1:end1 + 1] = reversePath(path1)
        start2, end2, path2 = genRandomPath(rePath)
        rePath[start2:end2 + 1] = reversePath(path2)
        start = min(start1, start2)
        end = max(end1, end2) + 1
        if pathEffCompare(bestPath[start:end], rePath[start:end]):
            count -= 1
            continue
        else:
            count = optdepth
            bestPath = rePath.copy()
    return bestPath


######################################  Distance Calculation#############################################

def calDist(num1, num2):
    dy = abs(orderInput[num1][2] - orderInput[num2][2])
    if int(orderInput[num1][2]) == int(orderInput[num2][2]):
        dx = abs(orderInput[num1][1] - orderInput[num2][1])
    else:
        if int(orderInput[num1][1]) == int(orderInput[num2][1]):
            dx = (orderInput[num1][1] % 1 + orderInput[num2][1] % 1)
            if dx > 1:
                dx = 2 - dx
        else:
            dx = abs(orderInput[num1][1] - orderInput[num2][1])
    return (dx + dy)


def ttPathDist(optPath):
    sum = 0.0
    for i in range(1, len(optPath)):
        sum += calDist(optPath[i], optPath[i - 1])
    return sum


# if path1 better/shotter than path2, then return true
def pathCompare(path1, path2):
    if ttPathDist(path1) <= ttPathDist(path2):
        return True
    return False


def genRandomPath(bestPath):
    a = np.random.randint(len(bestPath))
    while True:
        b = np.random.randint(len(bestPath))
        if np.abs(a - b) > 1:
            break
    if a > b:
        return b, a, bestPath[b:a + 1]
    else:
        return a, b, bestPath[a:b + 1]


def genRandomPath2(bestPath):
    a = np.random.randint(len(bestPath))
    while True:
        b = np.random.randint(len(bestPath))
        if np.abs(a - b) > 2:
            break
    if a > b:
        return b, a, bestPath[b:a + 1]
    else:
        return a, b, bestPath[a:b + 1]


def reversePath(path):
    rePath = path.copy()
    rePath[1:-1] = rePath[-2:0:-1]
    return rePath


def swapPath(path):
    rePath = path.copy()
    rePath[1], rePath[-2] = rePath[-2], rePath[1]
    return rePath


def pathOpt(bestPath):
    count = optdepth
    while count:
        distHistory.append(ttPathDist(bestPath))
        # print(ttPathDist(bestPath))
        start, end, path = genRandomPath(bestPath)
        rePath = reversePath(path)
        if pathCompare(path, rePath):
            count -= 1
            continue
        else:
            count = optdepth
            bestPath[start:end + 1] = rePath
    return bestPath


def pathOpt2(bestPath):
    count = int(optdepth / 2)
    while count:
        # distHistory.append(ttPathDist(bestPath))
        # print(ttPathDist(bestPath))
        start, end, path = genRandomPath2(bestPath)
        rePath = reversePath2(path)
        if pathCompare(path, rePath):
            count -= 1
            continue
        else:
            count = optdepth
            bestPath[start:end + 1] = rePath
            print("pathOpt2 worked")
    return bestPath


def pathOpt2ed(bestPath):
    count = int(optdepth)
    while count:
        # print(rePath)
        rePath = bestPath.copy()
        distHistory.append(ttPathDist(bestPath))
        # print(ttPathDist(bestPath))
        start1, end1, path1 = genRandomPath(rePath)
        rePath[start1:end1 + 1] = reversePath(path1)
        # print(rePath)
        start2, end2, path2 = genRandomPath(rePath)
        rePath[start2:end2 + 1] = reversePath(path2)
        start = min(start1, start2)
        end = max(end1, end2) + 1
        # print(rePath)
        # if pathCompare(bestPath, rePath):
        if pathCompare(bestPath[start:end], rePath[start:end]):
            count -= 1
            continue
        else:
            count = optdepth
            # print(ttPathDist(bestPath),ttPathDist(rePath))
            bestPath = rePath.copy()
            # print("pathOpt2ed worked")
    return bestPath


##########################PLOTING####################################

def plotPath(bestPath):
    plt.figure(1)
    ax = plt.subplot(111, aspect='equal')
    ax.plot(orderInput[:, 1], orderInput[:, 2], 'x', color='blue')
    for i, order in enumerate(orderInput):
        ax.text(order[1], order[2], str(i))
    ax.step(orderInput[bestPath, 1], orderInput[bestPath, 2], color='red')
    plt.grid(True)
    plt.show()

figureNum=1
def plotRoute(route):
    global figureNum
    plt.figure(figureNum)
    bx = plt.subplot(111, aspect='equal')
    bx.set_title("Combo Order %i" % figureNum)
    bx.plot(orderInput[:, 1], orderInput[:, 2], 'x', color='blue')
    for i, order in enumerate(orderInput):
        bx.text(order[1], order[2], int(order[0]))
    route = np.array(route)
    bx.plot(route[:, 1], route[:, 2], color='red')
    # plt.xticks(np.arange(0, 20, 1))
    # plt.yticks(np.arange(0, 10, 1))
    plt.xticks(np.arange(0, max(orderInput[:, 1] + 1), 1))
    plt.yticks(np.arange(0, max(orderInput[:, 2] + 1), 1))
    plt.grid(True)
    plt.ion()
    plt.show()
    figureNum+=1


def plotDistHistory(distHistory):
    plt.figure(2)
    plt.xlabel('optimization count')
    plt.ylabel('total distance')
    x = np.arange(0, len(distHistory))
    plt.plot(x, distHistory)
    plt.grid(True)
    plt.show()


def plotnDistHistory(ndistHistory):
    plt.figure(2)
    plt.xlabel('optimization count')
    plt.ylabel('total distance')
    for i in range(len(ndistHistory)):
        x = range(len(ndistHistory[i]))
        plt.plot(x, ndistHistory[i])
    plt.grid(True)
    plt.show()


#######################ROUTE##############################

def calRoute(num1, num2, route):
    if int(orderInput[num1][2]) == int(orderInput[num2][2]):
        route.append(orderInput[num2][0:3])
    else:
        xmid = round((orderInput[num1][1] + orderInput[num2][1]) / 2)
        route.append([0, xmid, int(orderInput[num1][2])])
        route.append([0, xmid, int(orderInput[num2][2])])
        route.append([0, int(orderInput[num2][1]), int(orderInput[num2][2])])
    return route


def ttRoute(bestPath):
    route = []
    route.append(orderInput[0][0:3])
    n = len(bestPath)
    for i in range(1, n):
        calRoute(bestPath[i - 1], bestPath[i], route)
    # calRoute(bestPath[n-1], endPoint,route)
    return route


#########################  Branch and Bound  #################################

def bnbCalDist(num1, num2):
    dy = abs(orderInput[num1][2] - orderInput[num2][2])
    if int(orderInput[num1][2]) == int(orderInput[num2][2]):
        dx = abs(orderInput[num1][1] - orderInput[num2][1])
    else:
        if int(orderInput[num1][1]) == int(orderInput[num2][1]):
            dx = (orderInput[num1][1] % 1 + orderInput[num2][1] % 1)
            if dx > 1:
                dx = 2 - dx
        else:
            dx = abs(orderInput[num1][1] - orderInput[num2][1])
    return (dx + dy)


def bnbMatrix(bnbDistMatrix):
    orderlen = len(orderInput)
    for i in range(0, orderlen):
        for j in range(0, orderlen):
            bnbDistMatrix[i][j] = bnbCalDist(i, j)
    for i in range(0, orderlen):
        bnbDistMatrix[i][i] = float('inf')


def bnbCalCost(num1, num2, bnbDistMatrix):
    if num1 == num2:
        # first item, initial matrix calculation
        bnbCost = 0
    else:
        bnbCost = bnbDistMatrix[num1, num2]
        bnbDistMatrix[num1, :] = float('inf')
        bnbDistMatrix[:, num2] = float('inf')
        bnbDistMatrix[num2, num1] = float('inf')
    mintmp = 0
    orderlen = len(orderInput)
    for i in range(0, orderlen):
        mintmp = min(bnbDistMatrix[i, :])
        if mintmp != float('inf'):
            bnbCost += mintmp
            bnbDistMatrix[i, :] -= mintmp
    for j in range(0, orderlen):
        mintmp = min(bnbDistMatrix[:, j])
        if mintmp != float('inf'):
            bnbCost += mintmp
            bnbDistMatrix[:, j] -= mintmp
    return bnbCost


def BnB(orderInput):
    orderlen = len(orderInput)
    bnbStack = [i for i in range(0, orderlen)]
    bnbPath = []
    bnbDistMatrix = np.zeros((orderlen, orderlen))
    bnbMatrix(bnbDistMatrix)
    bnbLBound = bnbCalCost(0, 0, bnbDistMatrix)
    bnbPath.append(bnbStack.pop(0))
    endnode = bnbStack.pop(-1)
    while bnbStack:
        bnbCost = float('inf')
        for i in range(0, len(bnbStack)):
            bnbMatrixTmp = copy.deepcopy(bnbDistMatrix)
            bnbCostTmp = bnbCalCost(bnbPath[-1], bnbStack[i], bnbMatrixTmp)
            if bnbCost > bnbCostTmp:
                bnbCost = bnbCostTmp
                mini = i
        bnbLBound += bnbCost
        bnbPath.append(bnbStack.pop(mini))
    bnbPath.append(endnode)
    return bnbPath, bnbLBound


def BnBk(orderInput, k):
    orderlen = len(orderInput)
    bnbStack = [i for i in range(0, orderlen)]
    bnbPath = []
    bnbDistMatrix = np.zeros((orderlen, orderlen))
    bnbMatrix(bnbDistMatrix)
    bnbLBound = [bnbCalCost(0, 0, bnbDistMatrix)]
    bnbPath.append(bnbStack.pop(0))
    depth = 1
    maxdepth = 1
    endnode = bnbStack.pop(-1)
    bnbBackup = [[bnbLBound[:], bnbPath[:], bnbStack[:], bnbDistMatrix[:], depth]]
    while bnbStack:
        for i in range(0, len(bnbStack)):
            bnbCost, bnbPath, bnbStack, bnbDistMatrix, depth = copy.deepcopy(bnbBackup[0])
            bnbCost[0] += bnbCalCost(bnbPath[-1], bnbStack[i], bnbDistMatrix)
            bnbPath.append(bnbStack.pop(i))
            depth += 1
            bnbBackup.append([bnbCost[:], bnbPath[:], bnbStack[:], bnbDistMatrix[:], depth])
        bnbBackup.pop(0)
        for i in list(range(0, len(bnbBackup))):
            if bnbBackup[i][4] > maxdepth:
                maxdepth = bnbBackup[i][4]
        for i in list(range(len(bnbBackup) - 1, -1, -1)):
            if bnbBackup[i][4] <= (maxdepth - k):
                bnbBackup.pop(i)
        bnbBackup.sort()
        bnbCost, bnbPath, bnbStack, bnbDistMatrix, depth = copy.deepcopy(bnbBackup[0])
    bnbPath.append(endnode)
    return bnbPath, bnbCost


def BnBfull(orderInput):
    orderlen = len(orderInput)
    bnbStack = [i for i in range(0, orderlen)]
    bnbPath = []
    bnbDistMatrix = np.zeros((orderlen, orderlen))
    bnbMatrix(bnbDistMatrix)
    bnbLBound = [bnbCalCost(0, 0, bnbDistMatrix)]
    bnbPath.append(bnbStack.pop(0))
    endnode = bnbStack.pop(-1)
    bnbBackup = [[bnbLBound[:], bnbPath[:], bnbStack[:], bnbDistMatrix[:]]]
    while bnbStack:
        for i in range(0, len(bnbStack)):
            bnbCost, bnbPath, bnbStack, bnbDistMatrix = copy.deepcopy(bnbBackup[0])
            bnbCost[0] += bnbCalCost(bnbPath[-1], bnbStack[i], bnbDistMatrix)
            bnbPath.append(bnbStack.pop(i))
            bnbBackup.append([bnbCost[:], bnbPath[:], bnbStack[:], bnbDistMatrix[:]])
        bnbBackup.pop(0)
        bnbBackup.sort()
        bnbCost, bnbPath, bnbStack, bnbDistMatrix = copy.deepcopy(bnbBackup[0])
    bnbPath.append(endnode)
    return bnbPath, bnbCost


###############################################################
def opt2(orderInput):
    global distHistory
    global efftHistory
    global ndistHistory
    distHistory=[1]
    efftHistory=[1]
    bestPath = np.arange(0, len(orderInput))
    start = time.time()
    distHistory[0] = ttPathDist(bestPath)
    if len(orderInput) > 3:
        # run opt-2 algrithom
        bestPath = pathOpt(bestPath)
    if len(orderInput) > 5:
        # run opt-2ed algrithom
        bestPath = pathOpt2ed(bestPath)
    end = time.time()
    timecost = end - start
    print("2-opt algorithm  tt distance  ", distHistory[-1])
    # ui.Ui_Dialog.qtprint("2-opt algorithm  tt distance: " + str(distHistory[-1]))
    print("bestPath order")
    print(bestPath.tolist())
    # ui.Ui_Dialog.qtprint("bestPath order: " + str(bestPath.tolist()))
    # print("Path")
    # for i in bestPath:
    #    print(orderInput[i])

    print("2-opt algorithm total effort is ", ttPathEff(bestPath)[1])
    # ui.Ui_Dialog.qtprint("2-opt algorithm total effort is: " + str(ttPathEff(bestPath)[1]))
    repath = bestPath.copy()
    repath[1:-1] = bestPath[-2:0:-1]
    print("reverse path: ", repath)
    print("2-opt algorithm total effort(reverse) is ", ttPathEff(repath)[1])
    # ui.Ui_Dialog.qtprint("2-opt algorithm total effort(reverse) is: " + str(ttPathEff(repath)[1]))

    print("2-opt algorithm time cost", timecost)
    # ui.Ui_Dialog.qtprint("2-opt algorithm time cost: " + str(timecost))
    #plotDistHistory(distHistory)
    route = ttRoute(bestPath)
    plotRoute(route)
    return distHistory[-1],bestPath.tolist(),ttPathEff(bestPath)[1],ttPathEff(repath)[1],timecost


def efftopt2(orderInput):
    global distHistory
    global efftHistory
    global ndistHistory
    distHistory=[1]
    efftHistory=[1]
    bestPath = np.arange(0, len(orderInput))
    start = time.time()
    distHistory[0] = ttPathEff(bestPath)[0]
    efftHistory[0] = ttPathEff(bestPath)[1]
    if len(orderInput) > 3:
        # run opt-2 algrithom
        bestPath = efftOpt(bestPath)
    if len(orderInput) > 5:
        # run opt-2ed algrithom
        bestPath = efftOpt2ed(bestPath)
    end = time.time()
    timecost = end - start
    print("Effort 2-opt algorithm: total distance  ", distHistory[-1])
    # ui.Ui_Dialog.qtprint("Effort 2-opt algorithm: total distance: " + str(distHistory[-1]))
    print("Effort 2-opt algorithm: total effort  ", efftHistory[-1])
    # ui.Ui_Dialog.qtprint("Effort 2-opt algorithm: total effort: " + str(efftHistory[-1]))
    print("bestPath order")
    print(bestPath.tolist())
    # ui.Ui_Dialog.qtprint("bestPath order: " + str(bestPath.tolist()))
    # print("Path")
    # for i in bestPath:
    #    print(orderInput[i])
    print("2-opt algorithm time cost", timecost)
    # ui.Ui_Dialog.qtprint("2-opt algorithm time cost " + str(timecost))
    #plotDistHistory(distHistory)
    route = ttRoute(bestPath)
    plotRoute(route)
    return distHistory[-1], bestPath.tolist(), efftHistory[-1], efftHistory[-1], timecost


def optTest(orderInput):
    for i in range(20):
        bestPath = np.arange(0, len(orderInput))
        start = time.time()
        del distHistory[:]
        distHistory.append(ttPathDist(bestPath))
        bestPath = pathOpt(bestPath)
        print(bestPath)
        ndistHistory.append(distHistory)
        print("total distance:  ", ttPathDist(bestPath))
        # print(ndistHistory)
        # print(i)
    plotnDistHistory(ndistHistory)


def bnbktest(k,orderInput):
    start = time.time()
    optPath, lowerBound = BnBk(orderInput, k)
    end = time.time()
    timecost = end - start
    print("bnb ", k, "-layer optPath")
    print(optPath)
    print("bnb ", k, "-layer lower bound is ", lowerBound)
    print("bnb ", k, "-layer total distance is ", ttPathDist(optPath))

    print("bnb ", k, "-layer total effort is ", ttPathEff(optPath)[1])
    repath = optPath.copy()
    repath[1:-1] = optPath[-2:0:-1]
    print("reverse path: ", repath)
    print("bnb ", k, "-layer total effort(reverse) is ", ttPathEff(repath)[1])

    print("bnb ", k, "-layer total effort is ", ttPathEff(optPath)[1])
    print("bnb ", k, "-layer time cost", timecost)
    route = ttRoute(optPath)
    plotRoute(route)
    return ttPathDist(optPath), optPath, ttPathEff(optPath)[1], ttPathEff(repath)[1], timecost


#################################################################

def findcolon(order):
    for i in range(len(order)):
        if order[i] == ':':
            return True
    return False


def transOrderNum(getorder, orderbatch):
    for i in range(len(getorder)):
        if findcolon(getorder[i]):
            orderrange = getorder[i].split(":")
            for k in range(int(orderrange[0]), int(orderrange[1]) + 1):
                orderbatch.append(k)
        else:
            orderbatch.append(int(getorder[i]))
    return orderbatch


def orderWeightCal(orderbatch):
    orderWeight=[]
    for i in orderbatch:
        order = orderList[i].split('\t')
        while '' in order:
            order.remove('')
        while '\n' in order:
            order.remove('\n')
        order = [int(x) for x in order]
        sumWeight = 0
        for j in order:
            if j in dementionDict:
                sumWeight += dementionDict[j][3]
            else:
                print("Missing item dimention: ", j)
        orderWeight.append([i,sumWeight])
    return orderWeight
    #weightDict = dict(zip(orderbatch, orderWeight))
    #return weightDict

def greedyCombine(orderWeight,orderbatch,modeNum,orderInput):
    weight=np.array(orderWeight)
    weight = weight[np.lexsort(-weight.T)]
    captmp = cartcapacity
    weight = weight.tolist()
    while len(weight):
        order=[]
        for i in range(len(weight)-1,-1,-1):
            if captmp >= weight[i][1]:
                captmp -= weight[i][1]
                order.append(weight[i][0])
                weight.pop(i)
        print("Combine orders:", order)
        orderInput=orderCombineData(order,orderInput)
        print("test", orderInput)
        if modeNum == 1:
            opt2(orderInput)
        if modeNum == 2:
            efftopt2(orderInput)
        if modeNum == 3:
            strfile = input("BnB-k algorithm depth: k=? (if items number>10, k should <4)")
            k = int(strfile)
            bnbktest(k,orderInput)
        if modeNum == 4:
            opt2(orderInput)
            efftopt2(orderInput)
            # optTest()
            bnbktest(1,orderInput)
            bnbktest(2,orderInput)
            bnbktest(3,orderInput)



# class myUI(QWidget):
#
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.setupUi(self)
#         self.setWindowTitle("Easy WareHouse")
#         self.show()





if (__name__ == '__main__'):

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    window = ui.Ui_Dialog()

    window.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

    # ex = uiInit()
    #
    # strfile = input("Input order number(s): (format: 1,2,start:end)");
    # getorder = strfile.split(",")

    # orderbatch = []
    # orderbatch = transOrderNum(getorder, orderbatch)

    # strfile = input("Which algorithm: 1.2-opt(distance)  2.2-opt(effort) 3.BnB k-layer 4.test(1+2+3)")
    # modeNum = int(strfile)
    # strfile = input("Combine orders?  0:no 1:yes(2-opt algorithm is suggested for processing time consideration)")
    # batchmode = int(strfile)
    # if batchmode:
    #     strfile = input("Cart capacity = ?  (default=99999 )")
    #     cartcapacity = int(strfile)
    #     #weightDict = orderWeightCal(orderbatch)
    #     orderWeight = orderWeightCal(orderbatch)
    #     #greedyCombine(orderWeight,orderbatch,modeNum,orderInput)
    #     weight = np.array(orderWeight)
    #     weight = weight[np.lexsort(weight.T)]
    #     captmp = cartcapacity
    #     weight = weight.tolist()
    #     print(weight)
    #     while len(weight):
    #         order = []
    #         for i in range(len(weight) - 1, -1, -1):
    #             if captmp >= weight[i][1]:
    #                 captmp -= weight[i][1]
    #                 order.append(weight[i][0])
    #                 weight.pop(i)
    #         captmp = cartcapacity
    #         print("Combine orders:", order)
    #         orderInput = orderCombineData(order, orderInput)
    #         if modeNum == 1:
    #             opt2(orderInput)
    #         if modeNum == 2:
    #             efftopt2(orderInput)
    #         if modeNum == 3:
    #             strfile = input("BnB-k algorithm depth: k=? (if items number>10, k should <4)")
    #             k = int(strfile)
    #             bnbktest(k, orderInput)
    #         if modeNum == 4:
    #             opt2(orderInput)
    #             efftopt2(orderInput)
    #             # optTest()
    #             bnbktest(1, orderInput)
    #             bnbktest(2, orderInput)
    #             bnbktest(3, orderInput)
    #
    # else:
    #     for i in orderbatch:
    #         orderInput = orderPrepare(i)
    #         if modeNum == 1:
    #             opt2(orderInput)
    #         if modeNum == 2:
    #             efftopt2(orderInput)
    #         if modeNum == 3:
    #             strfile = input("BnB-k algorithm depth: k=? (if items number>10, k should <4)")
    #             k = int(strfile)
    #             bnbktest(k,orderInput)
    #         if modeNum == 4:
    #             opt2(orderInput)
    #             efftopt2(orderInput)
    #             # optTest()
    #             bnbktest(1,orderInput)
    #             bnbktest(2,orderInput)
    #             bnbktest(3,orderInput)
    # print("end ", time.ctime())
    #
