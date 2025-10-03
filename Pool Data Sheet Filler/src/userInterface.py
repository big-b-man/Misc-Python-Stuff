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
from src.JSON_Parsing import *

def homeWindow():   
    #window root
    root = Tk()
    
    config = parseConfigFile("configuration.json")

    promptForSavePathVar = BooleanVar(value=config["default settings"]["Prompt For Save Path"])

    def select_PDF_button_command():
        filepath = filedialog.askopenfilename(title="Select PDF file", filetypes= [('Portable Document Format','*.pdf')])
        changeDefaultSetting("PDF Path",filepath)

    def fill_PDF_button_command():
        changeDefaultSetting("Prompt For Save Path",promptForSavePathVar.get())
        if promptForSavePathVar.get():
            filepath = filedialog.asksaveasfilename(title="Save PDF as", defaultextension=".pdf", filetypes= [('Portable Document Format','*.pdf')])
            changeDefaultSetting("Filled PDF Path",filepath)
        root.quit()
        root.destroy()

    #window title
    root.title('PDF Filler Tool')

    #window size
    root.geometry("256x512")

    content = ttk.Frame(root)
    select_PDF_label = ttk.Label(content, text= "Choose PDF to fill      ")
    select_PDF_button = ttk.Button(content, text="Choose File", command= select_PDF_button_command)

    promptForSavePath = ttk.Checkbutton(content, text="Promt for save path", variable=promptForSavePathVar, onvalue=True)

    Fill_PDF_button = ttk.Button(content, text="Fill PDF", command= fill_PDF_button_command)

    content.grid(column=0, row=0)
    select_PDF_label.grid(column=0, row=0)
    select_PDF_button.grid(column= 1, row= 0)
    Fill_PDF_button.grid(column=1, row=1)
    promptForSavePath.grid(column=1, row =2)
    root.mainloop()