# userInterface.py
#
# Copyright (C) 2025 Bennett Steers
#
# This file forms part of the PDF Filler Tool
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# This file contains functions used for controling the user interface. This file is called when

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import PhotoImage
import src.JSON_Parsing as ParseJSON
import os
import src.fileIO as fileIO

def userInterface():
    # states:
    # 0: Close program
    # 1: Run PDF Filler
    # 2: Home Window
    # 3: Settings Window
    state = 2
    while 1:
        match state:
            case 0:
                return False
            case 1:
                return True
            case 2:
                state = homeWindow()
            case 3:
                state = settingsWindow(ParseJSON.parseConfigFile("config/configuration.json"))

def homeWindow():
    #state variable
    state = 0
    
    # window root
    home_root = tk.Tk()
    
    # get the config file for finding default settings
    config = ParseJSON.parseConfigFile("config/configuration.json")

    # window title
    home_root.title('PDF Filler Tool')

    # window size
    #root.geometry("280x140")

    home_content = ttk.Frame(home_root)

    # window variables
    image = PhotoImage(file="config/Splash_Image.png")
    image_label = ttk.Label(home_content, image=image)
    PDF_save_path_label = ttk.Label(home_content,text= "PDF Save Path:")
    PDF_save_path_var = tk.StringVar(home_content, value=config["default settings"]["Filled PDF Path"])

    def select_PDF_button_command():
        filepath = filedialog.asksaveasfilename(title="Save PDF as", defaultextension=".pdf", filetypes= [('Portable Document Format','*.pdf')])
        # return to PDF filler window if file dialogue box is clsoed.
        if not filepath:
            return
        PDF_path_box.delete(0, tk.END)
        PDF_path_box.insert(0,filepath)

    def fill_PDF_button_command():
        # There is not error checking here, if the path is invalid then the program will do dumb shit
        ParseJSON.changeFilepath("Filled PDF Path",PDF_path_box.get())
        nonlocal state
        state = 1
        home_root.destroy()

    # Used to stop the PDF Filer from running if the UI window is closed
    def windowClosed():
        home_root.destroy()

    def initSettingsWindow():
        nonlocal state
        state = 3
        home_root.destroy()
        

    Fill_PDF_button = ttk.Button(home_content, text="Fill PDF", command= fill_PDF_button_command)
    select_PDF_button = ttk.Button(home_content, text="Choose File", command= select_PDF_button_command)
    close_button = ttk.Button(home_content, text="Close", command=windowClosed)
    PDF_path_box = ttk.Entry(home_content, textvariable=PDF_save_path_var)
    PDF_settings_button = ttk.Button(home_content, text="Settings", comman= initSettingsWindow)

    home_content.grid(column=0, row=0)
    image_label.grid(column=0, row=0, rowspan=2)
    Fill_PDF_button.grid(column=1, row=0)
    PDF_settings_button.grid(column= 1, row=1)
    PDF_save_path_label.grid(column=0, row=2)
    PDF_path_box.grid(column= 0, row=3, columnspan= 2, sticky= tk.EW)
    select_PDF_button.grid(column= 0, row= 4, sticky=tk.W)
    close_button.grid(column= 0, row=5, sticky=tk.W)
    
    home_root.protocol("WM_DELETE_WINDOW", windowClosed)
    
    home_root.resizable(width= False, height= False)
    home_root.mainloop()

    return state

def settingsWindow(config):
    excelMaping = ParseJSON.parseExcelMaping("config/excelMappings.json")
    
    if not excelMaping["Use Config Sheet Info"]:
        excelMaping["excel file"] = config["default settings"]["Spreadsheet Path"]
        excelMaping["sheet name"] = config["default settings"]["Spreadsheet Sheet Name"]
    
    print(excelMaping)
    # window root
    settings_root = tk.Tk()

    # window title
    settings_root.title('PDF Filler Tool')

    settings_content = ttk.Frame(settings_root)

    change_maping_label = ttk.Label(settings_content,text= "Change PDF Maping:")

    # Used to stop the PDF Filer from running if the UI window is closed
    def settingsWindowClosed():
        settings_root.destroy()

    def settingsSelectMapingFileFunction():
        filepath = filedialog.askopenfilename(title="Select Excel File", defaultextension=".xlsx", filetypes= [('Excel Spreadsheet','*.xlsx')])
        print(fileIO.getSheetNames(filepath))
        # return to PDF filler window if file dialogue box is clsoed.
        if not filepath:
            return

    settings_close_button = ttk.Button(settings_content, text="Close", command= settingsWindowClosed)
    settings_select_maping_file = ttk.Button(settings_content, text="Choose File",command=settingsSelectMapingFileFunction)

    settings_content.grid(column=0, row=0)
    settings_close_button.grid(column=0, row=0)
    settings_select_maping_file.grid(column=1, row=0)

    settings_root.protocol("WM_DELETE_WINDOW", settingsWindowClosed)

    settings_root.mainloop()

    return 2