import typing, tkinter as tk, csv, numpy as np

def LoadAirfoilNoPrompt(filePath):
    #parse hull profile and load into memory
    with open(filePath, 'r') as file:
        reader = csv.reader(file)
        # Insert First two columns into list
        data = [[float(x) for x in row[:2]] for row in reader]
    
    #Data preprocessing: Remove negative y values
    data = [item for item in data if item[1] >= 0]

    #Data preprocessing: Sort list by ascending x values
    data = sorted(data, key=lambda x: x[0])

    #convert to numpy arrays, delete repeat values
    data = np.unique(np.array(data), axis=0)
    
    return data

def LoadAirfoilPrompt(curveName):
    return LoadAirfoilNoPrompt(tk.filedialog.askopenfilename(title= "Select" + curveName + "Profile", filetypes=[('Comma Separated Values', '*.csv')]))