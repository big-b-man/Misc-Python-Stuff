import numpy as np, matplotlib.pyplot as plt
from .hullSplines import hullSpline

class plotPoints2D:
    def __init__(self, horizontalSpline: hullSpline, verticalSpline: hullSpline,canvasWidth: int, canvasHeight: int):
        self.xMin = min(horizontalSpline.xMin, verticalSpline.xMin)
        self.xMax = max(horizontalSpline.xMax, verticalSpline.xMax)
        self.x = np.linspace(self.xMin, self.xMax, 25)
        self.y = horizontalSpline.spline(self.x)
        self.z = verticalSpline.spline(self.x)
        self.horizontalPoints = []
        self.verticalPoints = []
        self.horizontalPointsNegative = []
        self.verticalPointsNegative = []

        self.xScale = canvasWidth/(self.xMax-self.xMin)
        self.yScale = canvasHeight/horizontalSpline.maxHeight/2
        self.zScale = canvasHeight/verticalSpline.maxHeight/2

        self.scale = min(self.xScale,self.yScale,self.zScale)
        

        for i in range (len(self.x)):
            self.horizontalPoints.append(float(self.x[i])*self.scale)
            self.horizontalPoints.append(float(self.y[i])*self.scale+canvasHeight/4)
            self.horizontalPointsNegative.append(float(self.x[i])*self.scale)
            self.horizontalPointsNegative.append(float(-self.y[i])*self.scale+canvasHeight/4)
            self.verticalPoints.append(float(self.x[i])*self.scale)
            self.verticalPoints.append(float(self.z[i])*self.scale+canvasHeight*3/4)
            self.verticalPointsNegative.append(float(self.x[i])*self.scale)
            self.verticalPointsNegative.append(float(-self.z[i])*self.scale+canvasHeight*3/4)