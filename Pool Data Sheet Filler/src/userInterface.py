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

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import PhotoImage
import src.JSON_Parsing as ParseJSON

def homeWindow():   
    #Tells the program wether to run the PDF Filler. Used to kill the program if the window is closed
    runPDFFiller = True

    #window root
    root = Tk()
    
    #get the config file for finding default settings
    config = ParseJSON.parseConfigFile("config/configuration.json")

    #window title
    root.title('PDF Filler Tool')

    #window size
    root.geometry("280x140")

    content = ttk.Frame(root)

    #window variables
    image = PhotoImage(file="config/Splash_Image.png")
    image_label = ttk.Label(content, image=image)
    select_PDF_label = ttk.Label(content, text= "Choose PDF to fill      ")
    promptForSavePathVar = BooleanVar(value=config["default settings"]["Prompt For Save Path"])

    def select_PDF_button_command():
        filepath = filedialog.askopenfilename(title="Select PDF file", filetypes= [('Portable Document Format','*.pdf')])
        #only change filepath if the filedialog returns a path (Will return nothing if window is cancelled or clsoed)
        if filepath:
            ParseJSON.changeFilepath("PDF Path",filepath)

    #TODO: #1 Sort out closing the file dialogue causing the output path to go blank
    def fill_PDF_button_command():
        # Change the configuration json to reflect the current state of the promt for save path checkbox
        # so it remembers if it was pressed or not when the program is run again
        ParseJSON.changeFilepath("Prompt For Save Path",promptForSavePathVar.get())
        # Opens file dialogue window if prompt for save path button is pressed
        if promptForSavePathVar.get():
            filepath = filedialog.asksaveasfilename(title="Save PDF as", defaultextension=".pdf", filetypes= [('Portable Document Format','*.pdf')])
            # return to PDF filler window if file dialogue box is clsoed.
            if not filepath:
                return
            ParseJSON.changeFilepath("Filled PDF Path",filepath)
        root.quit()
        root.destroy()

    # Used to stop the PDF Filer from running if the UI window is closed
    def windowClosed():
        nonlocal runPDFFiller
        runPDFFiller = False
        root.destroy()

    promptForSavePath = ttk.Checkbutton(content, text="Promt for save path", variable=promptForSavePathVar, onvalue=True)
    Fill_PDF_button = ttk.Button(content, text="Fill PDF", command= fill_PDF_button_command)
    select_PDF_button = ttk.Button(content, text="Choose File", command= select_PDF_button_command)

    content.grid(column=0, row=0)
    image_label.grid(column=0,row=0)
    select_PDF_label.grid(column=0, row=1)
    select_PDF_button.grid(column= 1, row= 1)
    Fill_PDF_button.grid(column=1, row=2)
    promptForSavePath.grid(column=1, row =3)

    root.protocol("WM_DELETE_WINDOW", windowClosed)
    
    root.mainloop()

    return runPDFFiller