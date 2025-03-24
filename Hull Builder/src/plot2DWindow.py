#UVSRC Hull Designer Tool

#Copyright (c) 2025 Bennett Steers

# This file is part of the UVSRC Hull Designer Tool

# The UVSRC Hull Designer Tool is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by 
# the Free Software Foundation, either version 3 of the License, or 
# (at your option) any later version.

# The UVSRC Hull Designer Tool is is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General 
# Public License for more details.

# You should have received a copy of the GNU General Public License along with
# The UVSRC Hull Designer Tool. If not, see <https://www.gnu.org/licenses/>.

# Description: class used to build and modify hull splines

import numpy as np, math
from .hullSplines import hullSpline

class plotPoints2D:
    def __init__(self, horizontalSpline: hullSpline, verticalSpline: hullSpline,canvasWidth: int, canvasHeight: int):
        self.xMin = min(horizontalSpline.xMin, verticalSpline.xMin)
        self.xMax = max(horizontalSpline.xMax, verticalSpline.xMax)
        self.horizontalPoints = []
        self.verticalPoints = []

        self.xScale = canvasWidth/(self.xMax-self.xMin)
        self.yScale = canvasHeight/horizontalSpline.maxHeight/4
        self.zScale = canvasHeight/verticalSpline.maxHeight/4

        self.scale = min(self.xScale,self.yScale,self.zScale)*0.9
        rightOffset = (canvasWidth-(self.xMax-self.xMin)*self.scale)/2
        for i in range (horizontalSpline.count):
            self.horizontalPoints.append(round(horizontalSpline.data[i][0]*self.scale+rightOffset))
            self.horizontalPoints.append(round(horizontalSpline.data[i][1]*self.scale+canvasHeight/4))
            
        for i in range (verticalSpline.count):    
            self.verticalPoints.append(round(verticalSpline.data[i][0]*self.scale+rightOffset))
            self.verticalPoints.append(round(verticalSpline.data[i][1]*self.scale+canvasHeight*3/4))