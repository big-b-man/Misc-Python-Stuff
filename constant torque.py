import numpy as np
import csv
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
from matplotlib import cm
import time
#program to extrapolate a data set and plots the results
#Known bugs: Program fails if there is only one corresponding yz data point for a unique x point

start_time = time.time()
inputFile = "JGV8-Torque.csv" #Input parameter for CSV file being used for data
pilotTorque = 41

#loads data from CSV file, column 0 is X data, 1 is Y data, 2 is Z data
with open(inputFile, newline='') as csvfile:
    reader = csv.reader(csvfile)
    #extracts first row of data which should be data column titles
    titles = next(reader)#reads column titles from first row
    data = np.array([[float(x) for x in row[:4]] for row in reader])#reads data from remaining rows

data[:,2]= data[:,2] - pilotTorque
uniqueX = np.sort(np.unique(data[:,0]))#list of unique X values in dataset
uniqueXCount = uniqueX.shape[0]#number of unique X values in dataset
tempY = np.sort(np.unique(data[:,1]))
yMin = tempY[0]#minimum Y value in dataset
yMax = tempY[-1]#maximum Y value in dataset

# Creates list for YZ splines, each entry is a function, Z(y) that returns a Z value given a y value for a unique x point.
# example: If uniqueX[1] = 2.5, Y=2 and Z=3, YZsplines[1](2) = 3
YZsplines = []

for i in range(uniqueXCount):
    tempArray = []
    for j in range (data.shape[0]):
        if data[j][0] == uniqueX[i]:
            tempArray.append(data[j,1:])
    tempArray  = np.array(sorted(tempArray, key=lambda x: x[0]))#ensures Y values are ordered as CubicSpline() will fail if first input isn't sequential
    spline = CubicSpline(np.transpose(tempArray[:,0]),np.transpose(tempArray[:,1]))#creates cubic spline to find Z as a function of Y for a unique X value
    YZsplines.append(spline)#add spline to array

constTorqueCurve = []
for i in range(uniqueXCount):
    zero = YZsplines[i].roots(discontinuity=False,extrapolate=None)
    k = 0
    while(zero[k] < yMin):
        k = k + 1
    constTorqueCurve.append([uniqueX[i],zero[k],0])

print(constTorqueCurve)

for i in range(uniqueXCount):
    tempArray = []
    for j in range (data.shape[0]):
        if data[j][0] == uniqueX[i]:
            tempArray.append([data[j,1],data[j,3]])
    tempArray  = np.array(sorted(tempArray, key=lambda x: x[0]))#ensures Y values are ordered as CubicSpline() will fail if first input isn't sequential
    spline = CubicSpline(np.transpose(tempArray[:,0]),np.transpose(tempArray[:,1]))#creates cubic spline to find Z as a function of Y for a unique X value
    constTorqueCurve[i][2] = spline(constTorqueCurve[i][1])

np.savetxt("constTorque.csv", constTorqueCurve, delimiter=",")