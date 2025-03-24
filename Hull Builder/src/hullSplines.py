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

import numpy as np
from scipy.interpolate import CubicSpline

# class containing spline info from imported spline
class hullSpline:
    def __splineRebuild(self, data):
        # gets min and max x points of data
        xMax, xMin = np.max(data[:,0]), np.min(data[:,0])
        # creates a cubic spline from the data
        spline = CubicSpline(data[:,0],data[:,1])

        #calculates the derivative of the spline to get the max height
        dx = spline.derivative()
        # if cubic spline has several roots, finds root with bounds of 
        # xMin and xMax
        for root in dx.roots():
            if xMin <= root and root <= xMax:
                heightMaxLocation = root
                break
        maxHeight = spline(heightMaxLocation)
        return (xMax, xMin, spline, maxHeight)
    
    def __init__(self, data: np.ndarray):
        # copies data into object
        self.data = data
        #initialize spline
        self.xMax, self.xMin, self.spline, self.maxHeight = self.__splineRebuild(self.data)

    #scales inputted splines
    def scale(self, scale: float | list, axis: str= "all"):
        match axis:
            case "all":
                if type(scale) != list:
                    raise TypeError("scale value is not a list")
                if len(scale) != 2:
                    raise NameError("Invalid number of arguments in scale list")
                self.data[:,0] = self.data[:,0] * scale[0]
                self.data[:,1] = self.data[:,1] * scale[1]
                self.xMax, self.xMin, self.spline, self.maxHeight = self.__splineRebuild(self.data)
            case "horizontal":
                if type(scale) != float:
                    raise TypeError("scale value is not a float")
                self.data[:,0] = self.data[:,0] * scale
                self.xMax, self.xMin, self.spline, self.maxHeight = self.__splineRebuild(self.data)
            case "vertical":
                if type(scale) != float:
                    raise TypeError("scale value is not a float")
                self.data[:,1] = self.data[:,1] * scale
                self.xMax, self.xMin, self.spline, self.maxHeight = self.__splineRebuild(self.data)
            case default:
                raise NameError("Invalid axis name")