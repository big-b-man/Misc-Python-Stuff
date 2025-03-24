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

# Description: Creates home window for program, returns name of the window we
# want to go to or termination code

import tkinter as tk
from tkinter import ttk
from .plot2DWindow import plotPoints2D
from .hullSplines import hullSpline
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def homeWindow(horizontalSpline: hullSpline, verticalSpline: hullSpline):
    # The main tkinter window 
    window = tk.Tk()
    frmMain = tk.Frame(window)
    
    # setting the title and  
    window.title('UVSRC Hull Designer')
    
    # setting the dimensions of
    # the main window 
    window.geometry("1000x800")
    
    #variable for storing sub menu which we will be going to
    nextWindow = "home"

    #functions for button functionality
    def constraintAction():
        window.quit()
        window.destroy()

    def plot2DAction():
        window.quit()
        window.destroy()


    def scaleAction():
        window.quit()
        window.destroy()


    def quitAction():
        window.quit()
        window.destroy()


    plotPoints = plotPoints2D(horizontalSpline,verticalSpline,1000,600)
    hullPreviewer = tk.Canvas(window, bg = 'white')
    hullPreviewer.config(width=1000,height=600)
    hullPreviewer.create_line(plotPoints.horizontalPoints, fill = 'black', width = 3, smooth= True)
    hullPreviewer.create_line(plotPoints.horizontalPointsNegative, fill = 'black', width = 3, smooth= True)
    hullPreviewer.create_line(plotPoints.verticalPoints, fill = 'black', width = 3, smooth= True)
    hullPreviewer.create_line(plotPoints.verticalPointsNegative, fill = 'black', width = 3, smooth= True)
    hullPreviewer.pack()

    #buttons to go to separate screens
    const_window_button=ttk.Button(window,text = 'Constraints', command = constraintAction)
    const_window_button.pack()
    plot2D_button=ttk.Button(window,text = 'Plot Hull 2D', command = plot2DAction)
    plot2D_button.pack()
    quit_button=ttk.Button(window,text = 'Quit', command = quitAction)
    quit_button.pack()
    scale_button=ttk.Button(window,text = 'Scale Hull', command = scaleAction)
    scale_button.pack()

    window.protocol("WM_DELETE_WINDOW", quitAction)  # To handle window close

    window.mainloop()
    
    return