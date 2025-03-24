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

# class containing spline info from imported spline
class hullSpline:
    def __init__(self, data: np.ndarray):
        # copies data into object
        self.data = data
        #initialize spline
        self.xMax, self.xMin = np.max(self.data[:,0]), np.min(self.data[:,0])
        self.maxHeight = np.max(self.data[:,1])
        self.count = len(data)

    #scales inputted splines
    def scale(self, scale: float | list | int, axis: str= "all"):
        match axis:
            case "all":
                if not isinstance(scale, list):
                    raise TypeError("scale value is not a list")
                if len(scale) != 2:
                    raise NameError("Invalid number of arguments in scale list")
                self.data[:,0] = self.data[:,0] * scale[0]
                self.data[:,1] = self.data[:,1] * scale[1]
                self.xMax = self.xMax * scale[0]
                self.xMin = self.xMin * scale[0]
                self.maxHeight = self.maxHeight *scale[1]
            case "horizontal":
                if not isinstance(scale, (int, float)):
                    raise TypeError("scale value is not a float or int")
                self.data[:,0] = self.data[:,0] * scale
                self.xMax = self.xMax * scale
                self.xMin = self.xMin * scale
            case "vertical":
                if not isinstance(scale, (int, float)):
                    raise TypeError("scale value is not a float or int")
                self.data[:,1] = self.data[:,1] * scale
                self.maxHeight = self.maxHeight *scale
            case default:
                raise NameError("Invalid axis name")