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

PDFPath = "Pool-construction-permit-application-form.pdf"
FilledPDFPath = "Filled Data Sheet.pdf"

# Load Configuration.json which contains default settings and fields in the PDF.
# Checks the JSON schema using checkConfigSchema()
def parseConfigFile(filepath):
    #load configuration file, throw error if not found
    try:
        with open(filepath, 'r') as FILE:
            data = json.load(FILE)
    except Exception as e:
        messagebox.showwarning("Error", "Error code 1: Error reading config: {str(e)}")
        sys.exit()

    #Verifies that the Configuration.JSON file has the correct schema
    checkConfigSchema(data)

    return data

#Checks if the configuration file contains "default settings and fields"
#Checks schema of "default settings" using checkDefaultSetttings()"
#Checks schema of "fields" using checkFields()
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

#checks if the default settings are formatted correctly
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

#checks if multi choice checkbox fields are formatted correctly
def validateMultiChoiceCheckbox(data, num):
    schema = {
        "type": "object",
        "required": ["name",
            "type",
            "options",
            "cell reference",
            "document page",
            "coordinate units"],
        "properties": {
        "name": {"type": "string"},
        "options": {"type": "array"},
        "document page": {"type": "number"},
        "document coordinates": {
            "type": "array",
            "items": {"type": "number"},
            "minItems": 2,
            "maxItems": 2
            }
        }
    }
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.ValidationError as e:
        messagebox.showwarning("Error", "Error code 6: document field "+ str(num) +" has invalid schema: " + str(e.message) + "\n")
        sys.exit()

    #Used for tracking which option of the multiple choice checkbox we are currently validating
    optionNum = 1

    for option in data["options"]:
        schema = {
        "type": "object",
        "required": ["option name",
            "document coordinates"],
        "properties": {
        "option name": {"type": "string"},
        "coordinate units": {
            "type": "string",
            "enum": ["points", "inches", "mm"]
            }
        }
        }
    try:
        jsonschema.validate(instance=option, schema=schema)
        optionNum += 1
    except jsonschema.ValidationError as e:
        messagebox.showwarning("Error", "Error code 7: multi choice checkbox option "+ str(optionNum) +" has invalid schema: " + str(e.message) + "\n")
        sys.exit()

#Converts Excel index to python list of lists
def excelCelltoArrayIndex(cell, name):
    #Convert uppercase letter to its base-26 numerical equivalent (A=0, B=1, ... Z=25).
    #Only need to check 4 first characters as excel column indexes are no more than 3 characters
    #4th character check is to verify propper formatting
    if cell.isalnum() == False:
        messagebox.showwarning("Error", "Error code 8: Cell reference for the following field is not alphaNumberic: "+ str(name))
        sys.exit()

    #array used to store excel cell coordinates converted to base 10
    coordinateArray = ['',0]
    
    counter = 0
    while cell[counter].isnumeric() == False:
        coordinateArray[1] += (ord(cell[counter].upper())-ord('A')+1)*pow(26,counter)
        counter += 1

    coordinateArray[1] += -1

    for i in range(counter,len(cell)):
        coordinateArray[0] += str(cell[i])
        if cell[i].isnumeric() == False:
            messagebox.showwarning("Error", "Error code 9: Cell reference for the following field is not formatted correctly: "+ str(name))
            sys.exit()
    
    coordinateArray[0] = int(coordinateArray[0])
    coordinateArray[0] += -1

    return coordinateArray

#writes a multi choice checkbox field to the PDF
def selectMultiChoiceCheckBox(doc,excelData,field):
    cell = excelCelltoArrayIndex(field["cell reference"],field["name"])
    value = ""
    valueCords = [0,0]
    caseMatchFlag = 0
    for item in field["options"]:
        if excelData[cell[0]][cell[1]] == item["option name"]:
            value = item["option name"]
            valueCords = item["document coordinates"]
            caseMatchFlag = 1
            break
        if caseMatchFlag == 1:
            return value, valueCords
        else:
            return 0

def writeMultiChoiceCheckBox(doc, excelData, defaultSettings, field):
    value,valueCords = 0,0
    try:
        value,valueCords = selectMultiChoiceCheckBox(doc,excelData,field)
    except:
        print("Warning: the following field's text in the excel file does not match " \
        "the available options in the configuration file: "+str(field["name"])+"\n" \
        "available options:")
        for i in field["options"]:
            print(str(i["option name"]))
    

def safe_insert_text(page, position, value, **kwargs):
    # Handle NaN/NaT/missing values
    if pd.isna(value):
        value = ""
    else:
        value = str(value)
    print(value)
    page.insert_text(position, value, **kwargs)

def readExcel(filePath, **kwargs):
    tempSheet = pd.read_excel(filePath, **kwargs)
    sheet = tempSheet.values.tolist()
    return sheet

def writedoc(doc, excelData, configuration):
    for field in configuration["fields"]:
        match field["type"]:
           case "multiChoiceCheckbox":
                writeMultiChoiceCheckBox(doc, excelData, configuration["default settings"], field)                

configuration = parseConfigFile("Configuration.json")

doc = pymupdf.open(PDFPath)
excelData = readExcel("Test Sheet.xlsx",sheet_name="Pool Data For Export", header=None)
writedoc(doc, excelData, configuration)
doc.save(FilledPDFPath)
doc.close()
#os.startfile(FilledPDFPath)