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

def homeWindow():   
    # Tells the program wether to run the PDF Filler. Used to kill the program if the window is closed
    runPDFFiller = True

    # window root
    root = tk.Tk()
    
    # get the config file for finding default settings
    config = ParseJSON.parseConfigFile("config/configuration.json")

    # window title
    root.title('PDF Filler Tool')

    # window size
    root.geometry("280x140")

    content = ttk.Frame(root)

    # window variables
    image = PhotoImage(file="config/Splash_Image.png")
    image_label = ttk.Label(content, image=image)
    PDF_save_path_label = ttk.Label(content,text= "PDF Save Path:")
    PDF_save_path_var = tk.StringVar(content, value=config["default settings"]["Filled PDF Path"])

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
        root.destroy()

    # Used to stop the PDF Filer from running if the UI window is closed
    def windowClosed():
        nonlocal runPDFFiller
        runPDFFiller = False
        root.destroy()

    def initSettingsWindow():
        settingsWindow(config)

    Fill_PDF_button = ttk.Button(content, text="Fill PDF", command= fill_PDF_button_command)
    select_PDF_button = ttk.Button(content, text="Choose File", command= select_PDF_button_command)
    close_button = ttk.Button(content, text="Close", command=windowClosed)
    PDF_path_box = ttk.Entry(content, textvariable=PDF_save_path_var)
    PDF_settings_button = ttk.Button(content, text="Settings", comman= initSettingsWindow)

    content.grid(column=0, row=0)
    image_label.grid(column=0, row=0, rowspan=2)
    Fill_PDF_button.grid(column=1, row=0)
    PDF_settings_button.grid(column= 1, row=1)
    PDF_save_path_label.grid(column=0, row=2)
    PDF_path_box.grid(column= 0, row=3, columnspan= 2, sticky= tk.EW)
    select_PDF_button.grid(column= 0, row= 4, sticky=tk.W)
    close_button.grid(column= 0, row=5, sticky=tk.W)
    
    root.protocol("WM_DELETE_WINDOW", windowClosed)
    
    root.mainloop()

    return runPDFFiller

def settingsWindow(config):
    # window root
    settings_root = tk.Tk()

    # window title
    settings_root.title('PDF Filler Tool')

    # window size
    settings_root.geometry("280x140")

    settings_content = ttk.Frame(settings_root)

    # Used to stop the PDF Filer from running if the UI window is closed
    def settingsWindowClosed():
        settings_root.destroy()

    settings_close_button = ttk.Button(settings_content, text="Close", command= settingsWindowClosed)

    settings_content.grid(column=0, row=0)
    settings_close_button.grid(column=0, row=0)

    settings_root.protocol("WM_DELETE_WINDOW", settingsWindowClosed)

    settings_root.mainloop()

    return