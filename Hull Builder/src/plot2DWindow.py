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

        #determine how much the hulls should be scale to fit the plots
        self.xScale = 430/(self.xMax-self.xMin)# current plot area is 420 pixels wide, hence the 420 number
        self.yScale = 220/(horizontalSpline.maxHeight*2) # current plot area is 220 pixels tall, hence the 220 number
        self.zScale = 220/(verticalSpline.maxHeight*2) # current plot area is 220 pixels tall, hence the 220 number

        self.scale = min(self.xScale,self.yScale,self.zScale)# determine which of the 3 scalling factors is the
                                                             # limiting scale factor
        for i in range (horizontalSpline.count):
            self.horizontalPoints.append(round(horizontalSpline.data[i][0]*self.scale + 50))
            self.horizontalPoints.append(round(horizontalSpline.data[i][1]*self.scale + 140))
            
        for i in range (verticalSpline.count):    
            self.verticalPoints.append(round(verticalSpline.data[i][0]*self.scale + 540))
            self.verticalPoints.append(round(verticalSpline.data[i][1]*self.scale + 140))