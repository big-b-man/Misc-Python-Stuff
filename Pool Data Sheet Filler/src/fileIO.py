# fileIO.py
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

import pandas as pd
from datetime import datetime
from src.errorHandling import fatalError
import traceback
import json
import src.JSON_Parsing as jsonParse

# contains functions for handling file I/O

# reads spreadsheet file and returns as list of lists containing the spreadsheet contents
def readExcel(filePath, **kwargs):
    try:
        tempSheet = pd.read_excel(filePath, **kwargs)
        tempSheet = tempSheet.fillna('')
        sheet = tempSheet.values.tolist()
        # pd.values.tolist() converts an excel date to a python date data type
        # convert back to string to avoid errors
        for row_index, row in enumerate(sheet):
            for col_index, cell in enumerate(row):
                if isinstance(cell, datetime):
                    sheet[row_index][col_index] = cell.strftime("%d-%m-%Y")
        return sheet
    except Exception as error:
        with open('log.txt', 'w') as f:
            f.write(traceback.format_exc())
        fatalError(16,"Unable to open excel file. Traceback has been written to log file")

# gets sheet name from an excel file
def getSheetNames(filePath):
    try:
        tempSheet = pd.ExcelFile(filePath)
        return tempSheet.sheet_names
    except Exception as error:
        with open('log.txt', 'w') as f:
            f.write(traceback.format_exc())
        fatalError(17,"Unable to open excel file. Traceback has been written to log file")

# converts excel column letter to number, returns number if successful, returns false is failed
def excelColumnToNumber(column):
    #Convert uppercase letter to its base-26 numerical equivalent (A=0, B=1, ... Z=25).
    #Only need to check 4 first characters as excel column indexes are no more than 3 characters
    #4th character check is to verify propper formatting

    #return false if input isn't letter
    if not column.isalpha():
        return False
    
    convertedNumber = 0 
    for i in range(len(column)):
        convertedNumber += (ord(column[i].upper())-ord('A')+1)*pow(26,i)

    return convertedNumber - 1

#converts and excel table to a python dictionary compatible with the fields object in the config
def excelTabletoListofLists(fieldMapingDict):
    excelFile = readExcel(fieldMapingDict["excel file"], sheet_name=fieldMapingDict["sheet name"], header=None)
    formattedExcel = []
    for row in excelFile:
        formattedExcel.append([row[fieldMapingDict["name"]],row[fieldMapingDict["type"]],
                               row[fieldMapingDict["multi choice options"]],row[fieldMapingDict["X insertion coordinate"]],
                               row[fieldMapingDict["Y insertion coordinate"]],row[fieldMapingDict["cell reference"]],
                               row[fieldMapingDict["document page"]],row[fieldMapingDict["coordinate units"]],
                               row[fieldMapingDict["override name"]],row[fieldMapingDict["override value"]]])
    return formattedExcel

# converts array of fields to dictionary of fields and stores to JSON file
def excelListofListstoDict(sortedArray):
    fields = []
    field = {}
    inputType = ''
    for row in sortedArray:
        # Checks if row has a name, which indicates if it is a new field
        if row[0]:
            # Make sure the field isn't empty before appending it to the array of fields
            if (field):
                if jsonParse.checkFieldsNoFail([field],True):
                    fields.append(field)
            # zeroes the field if a new field name is seen
            field = {}
            # checks if it is a valid PDF field option
            match row[1]:
                case "string":
                    inputType = "string"
                    field.update({"name": row[0], "type": row[1],"document coordinates":[row[3],row[4]],
                                  "cell reference": row[5], "document page": row[6], "coordinate units": row[7]})
                    #add override fields if overrides exist
                    if row[8]:
                                field.update({"overrides":{}})
                case "multiChoiceCheckbox":
                    inputType = "multiChoiceCheckbox"
                    field.update({"name": row[0], "type": row[1], "options": [],
                                  "document coordinates":[row[3],row[4]],
                                  "cell reference": row[5], "document page": row[6], "coordinate units": row[7]})
        # Checks if there are values in the field, and additional overrides to add
        if (row[8] and field):
            field["overrides"].update({row[8]: row[9]})
        if (inputType == "multiChoiceCheckbox" and row[2]):
            field["options"].append({"option name": row[2],"document coordinates":[row[3],row[4]]})
    
    return fields

# parses excel file to extract fields and stores them in the configuration.json object
def fieldsFromExcel(excelMapings,config):
    fieldMapingDict = {
        "name": "",
        "type" : "",
        "multi choice options" : "",
        "X insertion coordinate": "",
        "Y insertion coordinate": "",
        "cell reference": "",
        "document page": "",
        "coordinate units": "",
        "override name":"",
        "override value":"",
        "excel file": excelMapings["excel file"],
        "sheet name": excelMapings["sheet name"]
    }
    for key,value in excelMapings.items():
        # Don't convert letter to column if item is sheet name or excel file path
        if key in ("excel file", "sheet name"):
            continue
        fieldMapingDict[key]= excelColumnToNumber(value)
        if fieldMapingDict[key] is False:
            fatalError(18,"The following field is improperly formatted: " + str(key))

    sortedArray = excelTabletoListofLists(fieldMapingDict)
    fields = excelListofListstoDict(sortedArray)
    with open("config/Configuration.json",'w') as file:
        json.dump({"default settings":config["default settings"], "fields": fields}, file, indent=4)