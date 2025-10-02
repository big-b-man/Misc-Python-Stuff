# PDFFiller.py
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

# hours: sept 16: 2
# sept 17: 1
# sept 18: 2
# sept 26: 1
# sept 28: 8
# oct 1: 1.5

import pymupdf
import os
import json
import jsonschema
import copy
import src.fileIO as IO
from src.errorHandling import fatalError

# Load Configuration.json which contains default settings and fields in the PDF.
# Checks the JSON schema using checkConfigSchema()
def parseConfigFile(filepath):
    #load configuration file, throw error if not found
    try:
        with open(filepath, 'r') as FILE:
            data = json.load(FILE)
    except Exception as error:
        fatalError(1, 'Error reading config: ' + str(error))

    #Verifies that the Configuration.JSON file has the correct schema
    checkConfigSchema(data)

    return data

# Checks if the configuration file contains "default settings and fields"
# Checks schema of "default settings" using checkDefaultSetttings()"
# Checks schema of "fields" using checkFields()
def checkConfigSchema(data):
    schema = {
        "type": "object",
        "required": ["default settings", "fields"]
    }

    try:
        jsonschema.validate(instance=data, schema=schema)
        print("Configuration file contains default data and fields objects")
    except jsonschema.ValidationError as error:
        fatalError(2,error.message)
    checkDefaultSettings(data["default settings"])
    checkFields(data["fields"])

# checks if the default settings are formatted correctly
def checkDefaultSettings(data):
    schema = {
        "type": "object",
        "required": ["PDF Path",
                     "Filled PDF Path",
                     "Spreadsheet Path",
                     "Spreadsheet Sheet Name",
                     "font size",
                     "text x offset",
                     "text y offset",
                     "checkbox size",
                     "checkbox line width"],
        "properties": {
        "PDF Path": {"type": "string"},
        "Spreadsheet Path": {"type": "string"},
        "Filled PDF Path": {"type": "string"},
        "Spreadsheet Sheet Name": {"type": "string"},
        "font size": {"type": "number"},
        "text x offset": {"type": "number"},
        "text y offset": {"type": "number"},
        "checkbox size": {"type": "number"},
        "checkbox line width": {"type": "number"}
        }
    }

    try:
        jsonschema.validate(instance=data, schema=schema)
        print("default settings are valid")
    except jsonschema.ValidationError as e:
        fatalError(3,e.message)

# checks if inputed data fields are formatted correctly
def checkFields(data):
    #check schema to see if field is valid type
    for item in data:
        schema = {
            "type": "object",
            "required": ["type"],
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["multiChoiceCheckbox", "string"]    
                }
            }
        }
        
        try:
            jsonschema.validate(instance=item, schema=schema)
        except jsonschema.ValidationError as error:
            fatalError(4, 'The following document field: "' + str(item["name"]) \
                       + '" has an invalid field type. ' + str(error.message))
        
        #check if properties of fields are accurate based on type
        match item["type"]:
            case "string":
                validateString(item)
            case "multiChoiceCheckbox":
                validateMultiChoiceCheckbox(item)

# checks if string fields are formatted correctly
def validateString(data):
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
        fatalError(5, 'document field "'+ str(data["name"]) +'" has invalid schema: ' + str(e.message))

# checks if multi choice checkbox fields are formatted correctly
def validateMultiChoiceCheckbox(data):
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
            "coordinate units": {
                "type": "string",
                "enum": ["points", "inches", "mm"]
            }
        }
    }
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.ValidationError as e:
        fatalError(6, 'document field "'+ str(data["name"]) +'" has invalid schema: ' + str(e.message))

    #Used for tracking which option of the multiple choice checkbox we are currently validating

    for option in data["options"]:
        schema = {
        "type": "object",
        "required": ["option name",
            "document coordinates"],
        "properties": {
            "option name": {"type": "string"},
            "document coordinates": {
                "type": "array",
                "items": {"type": "number"},
                "minItems": 2,
                "maxItems": 2
                },
            }
        }
        try:
            jsonschema.validate(instance=option, schema=schema)
        except jsonschema.ValidationError as e:
            fatalError(7,'multi choice checkbox option in "' + str(data["name"]) + '" field has invalid schema: ' + str(e.message))

# Converts Excel index to python list of lists
def excelCelltoArrayIndex(cell, name):
    #Convert uppercase letter to its base-26 numerical equivalent (A=0, B=1, ... Z=25).
    #Only need to check 4 first characters as excel column indexes are no more than 3 characters
    #4th character check is to verify propper formatting
    if not cell.isalnum():
        fatalError(8, 'Cell reference for the following field is not alphaNumberic: "'+ str(name)+ '"')

    if cell.isdigit():
        fatalError(9, 'Cell reference for the following field only contains numbers: "'+ str(name)+ '"')

    if cell.isalpha():
        fatalError(10, 'Cell reference for the following field only contains Letters: "'+ str(name)+ '"')

    #array used to store excel cell coordinates converted to base 10
    coordinateArray = ['',0]
    
    counter = 0
    while not cell[counter].isnumeric():
        coordinateArray[1] += (ord(cell[counter].upper())-ord('A')+1)*pow(26,counter)
        counter += 1

    coordinateArray[1] += -1

    for i in range(counter,len(cell)):
        coordinateArray[0] += str(cell[i])
        if cell[i].isnumeric() == False:
            fatalError(11, "Cell reference for the following field is not formatted correctly: "+ str(name))
    
    coordinateArray[0] = int(coordinateArray[0])
    coordinateArray[0] += -1

    return coordinateArray

# checks if a field in the JSON has overrides to the default settings 
# returns a dictionary with the new settings
def checkForOverides(defaultSettings, field):
    if "overrides" in field:
        overrides = field["overrides"]
        #Need to make a deepcopy of the element otherwise it overwrites the default values dictionary
        newSettings = copy.deepcopy(defaultSettings)
        for item in overrides:
            if item in defaultSettings:
                newSettings[item] = overrides[item]
            else:
                print('Warning: the following override in the "' + str(field["name"]) +\
                      '" field is invalid and will be ignored.\n' + '"' + str(item) + '"')
        return newSettings
    else:
        return defaultSettings

# converts units defined in the JSON file to points
def convertUnits(units,item):
    match(units):
        case "points":
            return item
        case "inches":
            return [item[0]*72,item[1]*72]
        case "mm":
            return [item[0]/25.4*72,item[1]/25.4*72]
        # Don't need to handle default case because we verified the 
        # Schema to be one of those three options

# determines the coordinates for drawing a checkbox from a multi-choice
# checkbox list in the JSON file
def selectMultiChoiceCheckBox(doc,excelData,field):
    cell = excelCelltoArrayIndex(field["cell reference"],field["name"])
    for item in field["options"]:
        if excelData[cell[0]][cell[1]] == item["option name"]:
            return convertUnits(field["coordinate units"],item["document coordinates"])
    #return nothing if excel field does not match any options in JSON
    return

#checks if the field being inserted is on a valid document page
def checkIfPageExists(doc,field):
    if field["document page"] >= len(doc):
       return
    if field["document page"] <= 0:
        return
    else:
        return field["document page"]-1

# writes a multi choice checkbox field to the PDF
def writeMultiChoiceCheckBox(doc, excelData, defaultSettings, field):
    
    valueCords = selectMultiChoiceCheckBox(doc,excelData,field)
    
    if not isinstance(valueCords, list):
        print("Warning: the following field's text in the excel file does not match " \
        "the available options in configuration.JSON: "+str(field["name"])+"\n" \
        "available options:")
        for i in field["options"]:
            print(str(i["option name"]))
        return
    
    docPage = checkIfPageExists(doc, field)
    
    if not isinstance(docPage, int):
        print('Warning: The following field in configuration.JSON: "'+ str(field["name"]) +\
              '" is configured to print on an invalid page in the document. This entry will be ignored.')
        return
    
    newSettings = checkForOverides(defaultSettings,field)
    
    topRightCorner = [valueCords[0],valueCords[1]-newSettings["checkbox size"]]
    bottomLeftCorner = [valueCords[0]+newSettings["checkbox size"],valueCords[1]]
    
    doc[docPage].draw_line(topRightCorner,bottomLeftCorner,color=(1,0,0),width=newSettings["checkbox line width"])

# writes a string field to the PDF
def writeString(doc, excelData, defaultSettings, field):
    cell = excelCelltoArrayIndex(field["cell reference"],field["name"])
    text = excelData[cell[0]][cell[1]]

    docPage = checkIfPageExists(doc, field)
    
    if not isinstance(docPage, int):
        print('Warning: The following field in configuration.JSON: "'+ str(field["name"]) +\
              '" is configured to print on an invalid page in the document. This entry will be ignored.')
        return
    
    newSettings = checkForOverides(defaultSettings,field)
    
    textCoordinates = convertUnits(field["coordinate units"],field["document coordinates"])
    textLocation = [textCoordinates[0] + newSettings["text x offset"] \
                    ,textCoordinates[1] - newSettings["text y offset"]]

    doc[docPage].insert_text(textLocation, str(text), color=None, fontsize=newSettings["font size"], overlay=True)

def writedoc(doc, excelData, configuration):
    for field in configuration["fields"]:
        match field["type"]:
            case "multiChoiceCheckbox":
                writeMultiChoiceCheckBox(doc, excelData, configuration["default settings"], field)
            case "string":
                writeString(doc, excelData, configuration["default settings"], field)

def run():
    configuration = parseConfigFile("Configuration.json")

    #with open('config1.json', 'w') as json_file:
    #    json.dump(configuration, json_file, indent=4)

    PDFPath = configuration["default settings"]["PDF Path"]
    FilledPDFPath = configuration["default settings"]["Filled PDF Path"]
    SpreadsheetPath= configuration["default settings"]["Spreadsheet Path"]
    SpreadsheetSheetName = configuration["default settings"]["Spreadsheet Sheet Name"]
    doc = pymupdf.open(PDFPath)
    excelData = IO.readExcel(SpreadsheetPath, sheet_name=SpreadsheetSheetName, header=None)
    writedoc(doc, excelData, configuration)
    doc.save(FilledPDFPath)
    doc.close()
    os.startfile(FilledPDFPath)