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

def homeWindow(horizontalSpline: hullSpline, verticalSpline: hullSpline):
    # The main tkinter window
    window = tk.Tk()
    # setting the title
    window.title('UVSRC Hull Designer')
    # setting the dimensions of the main window
    window.geometry("1000x800")
    #frame for submarine plots
    plotterFrame = ttk.Frame(window)
    optionsFrame = ttk.Frame(window)
    constraintFrame =ttk.Frame(optionsFrame)
    scaleFrame = ttk.Frame(optionsFrame)
    analysisFrame = ttk.Frame(optionsFrame)

    plotPoints = plotPoints2D(horizontalSpline,verticalSpline,1000,400)
    hullPreviewer = tk.Canvas(plotterFrame, bg = 'white')
    hullPreviewer.config(width=1000,height=400)
    def setupPlot():
        hullPreviewer.create_line((50,30,50,250,480,250), fill = 'grey', width= 2)
        hullPreviewer.create_line((540,30,540,250,970,250), fill = 'grey', width= 2)
    
    setupPlot()
    hullPreviewer.create_line(plotPoints.horizontalPoints, fill = 'black', width = 3, smooth= True)
    hullPreviewer.create_line(plotPoints.verticalPoints, fill = 'black', width = 3, smooth= True)
    hullPreviewer.pack()
    plotterFrame.pack()

    #functions for button functionality
    def constraintAction():
        print("TODO: Add action")

    def scaleAction():
        print("TODO: Add action")

    def quitAction():
        window.quit()
        window.destroy()

    #buttons to go to separate screens
    const_window_button=ttk.Button(optionsFrame,text = 'Constraints', command = constraintAction)
    scale_button=ttk.Button(optionsFrame,text = 'Scale Hull', command = scaleAction)
    quit_button=ttk.Button(optionsFrame,text = 'Quit', command = quitAction)
    
    const_window_button.pack()
    scale_button.pack()
    quit_button.pack()
    optionsFrame.pack()

    window.protocol("WM_DELETE_WINDOW", quitAction)  # To handle window close

    window.mainloop()
    
    return