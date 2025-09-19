# Pool Data Sheet Filler Tool
#
# Copyright (C) 2025 Bennett Steers
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

import pymupdf
import pandas as pd
import os
import sys
import json
from tkinter import messagebox
import jsonschema

#General Style Notes: 12 Point font, offset 6 point from base of cell

ExcelPath = "Pool-construction-permit-application-form.pdf"
FilledPDFPath = "Filled Data Sheet.pdf"

#Load JSON, Check if
def parseConfigFile(filepath):
    #load configuration file, throw error if not found
    try:
        with open(filepath, 'r') as FILE:
            data = json.load(FILE)
    except Exception as e:
        messagebox.showwarning("Error", "Error code 1: Error reading config: {str(e)}")
        sys.exit()
    
    return data

#Checks if the configuration file contains "default settings and fields"
def checkConfigSchema(data):
    schema = {
        "type": "object",
        "required": ["default settings", "fields"]
    }

    try:
        jsonschema.validate(instance=data, schema=schema)
        print("Configuration file contains default data and fields objects")
    except jsonschema.ValidationError as e:
        messagebox.showwarning("Error", "Error code 2: " + str(e.message) + "\n")
        sys.exit()
    checkDefaultSettings(data["default settings"])
    checkFields(data["fields"])

#checks if the default settings are formatte correctly
def checkDefaultSettings(data):
    schema = {
        "type": "object",
        "required": ["font size",
                     "text x offset",
                     "text y offset",
                     "checkbox size"],
        "properties": {
        "font size": {"type": "number"},
        "text x offset": {"type": "number"},
        "text y offset": {"type": "number"},
        "checkbox size": {"type": "number"}
        }
    }

    try:
        jsonschema.validate(instance=data, schema=schema)
        print("default settings are valid")
    except jsonschema.ValidationError as e:
        messagebox.showwarning("Error", "Error code 3: " + str(e.message) + "\n")
        sys.exit()

#checks if inputed data fields are formatted correctly
def checkFields(data):
    i = 1
    for item in data:
        match item["type"]:
            case "string":
                validateString(item,i)
                i += 1
            case "multiChoiceCheckbox":
                validateMultiChoiceCheckbox(item,i)
                i += 1
            case _:
                messagebox.showwarning("Error", "Error code 4: document field "+ str(i) + " is an invalid entry type")
                sys.exit()

#checks if string fields are formatted correctly
def validateString(data, num):
    schema = {
        "type": "object",
        "required": ["name",
            "type",
            "cell reference",
            "document page",
            "document coordinates",
            "coordinate units"],
        "properties": {
        "name": {"type": "string"},
        "cell reference": {"type": "string"},
        "document page": {"type": "number"},
        "document coordinates": {
            "type": "array",
            "items": {"type": "number"},
            "minItems": 2,
            "maxItems": 2
        },
        "coordinate units": {
            "type": "string",
            "enum": ["points", "inches", "mm"]
            }
        }
    }
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.ValidationError as e:
        messagebox.showwarning("Error", "Error code 5: document field "+ str(num) +" has invalid schema: " + str(e.message) + "\n")
        sys.exit()

def validateMultiChoiceCheckbox(data, num):
    schema = {
        "type": "object",
        "required": ["name",
            "type",
            "options",
            "document coordinates",
            "cell reference",
            "document page",
            "coordinate units"],
        "properties": {
        "name": {"type": "string"},
        "options": {"type": "array"},
        "document coordinates": {"type": "array"},
        "document page": {"type": "number"},
        "coordinate units": {
            "type": "string",
            "enum": ["points", "inches", "mm"]
            }
        }
    }
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.ValidationError as e:
        messagebox.showwarning("Error", "Error code 6: document field "+ str(num) +" has invalid schema: " + str(e.message) + "\n")
        sys.exit()
    if(len(data["document coordinates"])==len(data["options"])):
        print("yes")
    else:
        #
        #
        #PICK UP HERE AND WRITE ERROR CODE AND VERIFY ALL STRINGS IN OPTIONS AND ALL NUMBERS IN COORDINATES
        #
        #
        print("no")

def safe_insert_text(page, position, value, **kwargs):
    # Handle NaN/NaT/missing values
    if pd.isna(value):
        value = ""
    else:
        value = str(value)
    print(value)
    page.insert_text(position, value, **kwargs)

def writedoc(doc, healthData):
    print("test")

configuration = parseConfigFile("Configuration.json")
checkConfigSchema(configuration)
doc = pymupdf.open(ExcelPath)
excelData = pd.read_excel("Test Sheet.xlsx",sheet_name="Pool Data For Export", header=None)
print ("Excel Data read:\n",excelData)
writedoc(doc,excelData)
doc.save(FilledPDFPath)
doc.close()
os.startfile(FilledPDFPath)