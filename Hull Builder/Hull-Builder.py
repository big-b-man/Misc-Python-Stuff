#UVSRC Hull Designer Tool

#Copyright (c) 2025 Bennett Steers

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

# Description- Makes a hull loft from 2 imported CSV files that describe the 2D hull curves

import tkinter as tk, numpy as np, matplotlib.pyplot as plt, os
from src.loadAirfoil import loadAirfoilPrompt, loadAirfoilNoPrompt
from src.hullSplines import hullSpline
from src.window import homeWindow
from scipy.interpolate import CubicSpline

#XYdata = loadAirfoilPrompt("Horizontal")
XYdata = loadAirfoilNoPrompt("C:/Users/benne/OneDrive/Documents/GitHub/Misc-Python-Stuff/Hull Builder/naca16021.csv")
#XZdata = loadAirfoilPrompt("Vertical")
XZdata = loadAirfoilNoPrompt("C:/Users/benne/OneDrive/Documents/GitHub/Misc-Python-Stuff/Hull Builder/ys900.csv")

#create a cubic spline from both the imported CSV files
horizontalSpline = hullSpline(XYdata)
verticalSpline = hullSpline(XZdata)

homeWindow(horizontalSpline, verticalSpline)