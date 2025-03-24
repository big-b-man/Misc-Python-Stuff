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

# Description: #Contains the functions used to load airfoils store in a CSV 
# file into memory

import typing, tkinter as tk, csv, numpy as np
from tkinter import filedialog

#Loads the airfoils from a hardcoded file path
def loadAirfoilNoPrompt(filePath):
    #parse hull profile and load into memory
    with open(filePath, 'r') as file:
        reader = csv.reader(file)
        # Insert First two columns into list
        data = [[float(x) for x in row[:2]] for row in reader]
    
    #Data preprocessing: Remove negative y values
    data = [item for item in data if item[1] >= 0]

    #Data preprocessing: Sort list by ascending x values
    #x values need to be ascending to avoid cubic spline interpolation errors
    data = sorted(data, key=lambda x: x[0])

    #convert to numpy arrays, delete repeat values
    data = np.unique(np.array(data), axis=0)
    
    return data

# prompts the user for a file using the tkinter file dialog box, then passes
# that file path to LoadAirfoilNoPrompt()
def loadAirfoilPrompt(curveName):
    return loadAirfoilNoPrompt(tk.filedialog.askopenfilename(title= "Select" + curveName + "Profile", filetypes=[('Comma Separated Values', '*.csv')]))