#Author- Bennett Steers
#Description- Makes a hull loft from 2 imported CSV files that describe the 2D hull curves
#imported curves must only contain the positive half of the y points for each profile
#if the x points are negative, the profile must be mirrored so that they are positive
#imported CSV's must be arranged with the X values going from lowest to highest value

import csv, math,tkinter as tk, numpy as np, matplotlib.pyplot as plt
from src.LoadAirfoil import LoadAirfoilPrompt, LoadAirfoilNoPrompt
from tkinter import filedialog
from scipy.interpolate import CubicSpline

def homeWindow():
    # The main tkinter window 
    window = tk.Tk()
    frmMain = tk.Frame(window)
    
    # setting the title and  
    window.title('Hull Designer Home Screen')
    
    # setting the dimensions of
    # the main window 
    window.geometry("500x500")
    
    #variable for storing sub menu which we will be going to
    nextWindow = "home"

    #functions for button functionality
    def constraintAction():
        nonlocal nextWindow 
        nextWindow = "constraint"
        window.destroy()

    def plot2DAction():
        nonlocal nextWindow 
        nextWindow = "plot2D"
        window.destroy()

    def quitAction():
        nonlocal nextWindow
        nextWindow = "quit"
        window.destroy()

    def scaleAction():
        nonlocal nextWindow
        nextWindow = "scale"
        window.destroy()

    def on_close():
        nonlocal nextWindow
        nextWindow = "quit"
        window.destroy()

    #buttons to go to separate screens
    const_window_button=tk.Button(window,text = 'Constraints', command = constraintAction)
    plot2D_button=tk.Button(window,text = 'Plot Hull 2D', command = plot2DAction)
    quit_button=tk.Button(window,text = 'Quit', command = quitAction)
    scale_button=tk.Button(window,text = 'Scale Hull', command = scaleAction)

    #setup window grid
    const_window_button.grid(row=0,column=0)
    plot2D_button.grid(row=0,column=1)
    scale_button.grid(row=0,column=2)
    quit_button.grid(row=0,column=3)
        
    #terminate the program if the user closes the main window
    window.protocol("WM_DELETE_WINDOW",on_close)
    
    window.mainloop()
    
    return nextWindow

def constraintsWindow(constraints):
    # The main tkinter window 
    window = tk.Tk()
    frmMain = tk.Frame(window)
    
    # setting the title and
    window.title('Add constraint points') 
    
    # setting the dimensions of  
    # the main window 
    window.geometry("500x500")

    # variable for storing entry data
    point_var = tk.StringVar()
    const_name_var = tk.StringVar()

    #return empty dictionary if window is closed
    def on_close():
        window.destroy()
        return {}

    window.protocol("WM_DELETE_WINDOW",on_close)

    def current_constraints():
        if bool(constraints) == False:
            tk.messagebox.showinfo("Current Constraints","No constraints defined")
        else:
            tk.messagebox.showinfo("Current Constraints",constraints)

    def new_constraints():
        points = str(point_var.get())
        names = str(const_name_var.get())
        points = points.split(';')
        names = names.split(';')
        if len(points) != len(names):
            tk.messagebox.showerror("Error","Number of constraint points does not match \nnumber of constraint names")
            return {}
        #adding some dummy coordinates as the error checking requires a list of lists, and it will only recieve
        #a single level list if there is only one coordinate entered
        points.append('0,0,0')
        for i in range(len(points)):
            points[i] = points[i].split(',')
            if len(points[i]) != 3:
                tk.messagebox.showerror("Error","Improper Coordinates in constraint " + str(i+1))
                return {}
            try:
                points[i] = [float(item) for item in points[i]]
            except:    
                tk.messagebox.showerror("Error","Coordinates in constraint " + str(i+1) + "\nCould not be converted to a float")
                return {}
        #remove dummy entry
        points.pop()
        if len(names) != len(set(names)):
            tk.messagebox.showerror("Error","New constraints contain duplicate names")
            return{}
        constraints = {}
        for i in range(len(names)):
            constraints[names[i]] = points[i]
        return constraints
    
    # point constraint Label
    point_constraint_label = tk.Label(window, text = 'constraint points (x,y,z)', font=(10))

    # point constraint entry box
    point_constraint_entry = tk.Entry(window,textvariable = point_var, font=(10))

    # constraint name label
    constraint_name_label = tk.Label(window, text = 'constraint name', font=(10))

    # constraint name entry box
    constraint_name_entry = tk.Entry(window,textvariable = const_name_var, font=(10))

    #add points button
    add_constraints_button=tk.Button(window,text = 'Add Constraints', command = new_constraints)

    #view current constraints button
    view_constraints_button=tk.Button(window,text = 'View Constraints', command = current_constraints)

    # adding elements to window grid
    point_constraint_label.grid(row=0,column=0)
    point_constraint_entry.grid(row=0,column=1)
    constraint_name_label.grid(row=1,column=0)
    constraint_name_entry.grid(row=1,column=1)
    add_constraints_button.grid(row=2,column=0)
    view_constraints_button.grid(row=3,column=0)

    #display window in loop until closed
    window.mainloop()

def plot2D(vertScale, horScale, HorizontalMax,VerticalMax,YXspline,YZspline,constraints):
    # make data
    yHor = np.linspace(0,int(HorizontalMax*100))/100
    yVert = np.linspace(0,int(VerticalMax*100))/100
    x = YXspline(yHor)
    z = YZspline(yVert)
    lengthMax = max(HorizontalMax,VerticalMax)
    heightMax = max(YZspline(vertScale),YXspline(horScale))
    aspect = (1)

    # plot
    fig, (ax1, ax2) = plt.subplots(2,1)
    ax1.plot(yHor,x, 'c')
    ax1.plot(yHor,-x, 'c')
    ax1.set_title("Horizontal Hull Profile")
    ax1.set_aspect(aspect)
    ax1.set_xlim([0,lengthMax])
    ax1.set_ylim([-heightMax,heightMax])

    ax2.plot(yVert,z, "c")
    ax2.plot(yVert,-z, "c")
    ax2.set_title("Vertical Hull Profile")
    ax2.set_aspect(aspect)
    ax2.set_xlim([0,lengthMax])
    ax2.set_ylim([-heightMax,heightMax])

    ax1.set(xlabel="y",ylabel="x")
    ax2.set(xlabel="y",ylabel="z")
    plt.show()

def scalePlot(horizontalXScale, horizontalYScale, verticalXScale, verticalYScale):
    # The main tkinter window 
    window = tk.Tk()
    frmMain = tk.Frame(window)
    
    # setting the title and  
    window.title('Add constraint points') 
    
    # setting the dimensions of  
    # the main window 
    window.geometry("500x500")

    # variable for storing entry data
    hor_x_var = tk.StringVar()
    hor_y_var = tk.StringVar()
    vert_x_var = tk.StringVar()
    vert_y_var = tk.StringVar()

    # hor X scale Label
    hor_x_label = tk.Label(window, text = 'Horizontal Profile X Scale', font=(10))

    # hor X scale entry box
    hor_x_entry = tk.Entry(window,textvariable = hor_x_var, font=(10))
    hor_x_entry.insert(0,str(horizontalXScale))

    # hor Y scale Label
    hor_y_label = tk.Label(window, text = 'Horizontal Profile Y Scale', font=(10))

    # hor X scale entry box
    hor_y_entry = tk.Entry(window,textvariable = hor_y_var, font=(10))
    hor_y_entry.insert(0,str(horizontalYScale))

    # vert X scale Label
    vert_x_label = tk.Label(window, text = 'Vertical Profile X Scale', font=(10))

    # vert X scale entry box
    vert_x_entry = tk.Entry(window,textvariable = vert_x_var, font=(10))
    vert_x_entry.insert(0,str(verticalXScale))

    # vert Y scale Label
    vert_y_label = tk.Label(window, text = 'Vertical Profile Y Scale', font=(10))

    # vert X scale entry box
    vert_y_entry = tk.Entry(window,textvariable = vert_y_var, font=(10))
    vert_y_entry.insert(0,str(verticalYScale))

    #add set scale button
    set_button=tk.Button(window,text = 'Set Scale', command = window.destroy)

    # adding elements to window grid
    hor_x_label.grid(row=0,column=0)
    hor_x_entry.grid(row=0,column=1)
    hor_y_label.grid(row=1,column=0)
    hor_y_entry.grid(row=1,column=1)
    vert_x_label.grid(row=2,column=0)
    vert_x_entry.grid(row=2,column=1)
    vert_y_label.grid(row=3,column=0)
    vert_y_entry.grid(row=3,column=1)
    set_button.grid(row=4,column=1)

    #display window in loop until closed
    window.mainloop()
    horizontalXScale = float(hor_x_var.get())
    horizontalYScale = float(hor_y_var.get())
    verticalXScale = float(vert_x_var.get())
    verticalYScale = float(vert_y_var.get())
    
    return horizontalXScale, horizontalYScale, verticalXScale, verticalYScale

def getMax(x,dx,lenMax):
    root = dx.roots()
    i = 0
    goodRoot = False
    while(goodRoot == False):
        if root[i] > 0 and root[i] < lenMax:
            root = root[i]
            goodRoot = True
        else:
            i += 1
    return float(root)

#YXdata = LoadAirfoilPrompt("Horizontal")
YXdata = LoadAirfoilNoPrompt("C:/Users/benne/OneDrive/Documents/GitHub/Misc-Python-Stuff/Hull Builder/naca16021.csv")
#YZdata = LoadAirfoilPrompt("Vertical")
YZdata = LoadAirfoilNoPrompt("C:/Users/benne/OneDrive/Documents/GitHub/Misc-Python-Stuff/Hull Builder/ys900.csv")

#create a cubic spline from both the imported CSV files
horizontalSpline = CubicSpline(YXdata[:,0],YXdata[:,1])
verticalSpline = CubicSpline(YZdata[:,0],YZdata[:,1])

#calculate the derivative splines
vertPrime = verticalSpline.derivative()
horPrime = horizontalSpline.derivative()

quit = False
windowType = "home"
#hortScale and VertScale are used to scale the graph in the vertical and horizontal direction
#equal to half the height and width of the boat (distance from neural axis to top of spline)
vertScale = getMax(verticalSpline,vertPrime,YZdata[-1,0])
horScale = getMax(horizontalSpline,horPrime,YXdata[-1,0])

horizontalYScale = 1
horizontalXScale = 1
verticalYScale = 1
verticalXScale = 1

constraints = {}
while(quit == False):
    match windowType:
        case "home":
            windowType = homeWindow()
        
        case "constraint":
            tempDic = constraintsWindow(constraints)
            if len(tempDic|constraints) != (len(tempDic)+len(constraints)):
                result = tk.messagebox.askquestion("Duplicate names detected","Constraints cannot have duplicate names."
                "\ndo you wish to overwrite the old constraint?")
                if result == 'yes':
                    constraints = constraints|tempDic
            else:
                constraints = constraints|tempDic
            windowType = "home"
        
        case "plot2D":
            plot2D(vertScale, horScale, YXdata[-1,0]*horizontalXScale, YZdata[-1,0]*verticalXScale, horizontalSpline, verticalSpline,constraints)
            windowType = "home"
        
        case "quit":
            quit = True
        
        case "scale":
            horizontalXScale, horizontalYScale, verticalXScale, verticalYScale = scalePlot(horizontalXScale, horizontalYScale, verticalXScale, verticalYScale)
            windowType = "home"
            #redefine the cubic splines using the scale factors
            YXtemp = YXdata.copy()
            YXtemp[:,0] = YXtemp[:,0]*horizontalXScale
            YXtemp[:,1] = YXtemp[:,1]*horizontalYScale
            YZtemp = YZdata.copy()
            YZtemp[:,0] = YZtemp[:,0]*verticalXScale
            YZtemp[:,1] = YZtemp[:,1]*verticalYScale
            horizontalSpline = CubicSpline((YXtemp[:,0]),(YXtemp[:,1]))
            verticalSpline = CubicSpline((YZtemp[:,0]),(YZtemp[:,1]))
            vertPrime = verticalSpline.derivative()
            horPrime = horizontalSpline.derivative()
            vertScale = getMax(verticalSpline,vertPrime,YZtemp[-1,0])
            horScale = getMax(horizontalSpline,horPrime,YXtemp[-1,0])