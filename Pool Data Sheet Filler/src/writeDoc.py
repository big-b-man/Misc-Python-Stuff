# writeDoc.py
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

# Contains functions for writing fields to the PDF file from excel sheet

from src.errorHandling import fatalError
import copy

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
    if field["document page"] > len(doc):
       return
    if field["document page"] <= 0:
        return
    else:
        return field["document page"]-1

# writes a multi choice checkbox field to the PDF
def writeMultiChoiceCheckBox(doc, excelData, defaultSettings, field):
    
    valueCords = selectMultiChoiceCheckBox(doc,excelData,field)
    
    #TODO: #2 Make this print to the log file since console is disabled
    #TODO: #3 Throw a warning once the program has finished if certain fields produced errors
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