# JSON_Parsing.py
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

# Contains functions for parsing JSON file containing settings and PDF fields

# TODO: Insert a function to parse the config file while only checking the default settings object so it can be imported if fields are screwed up

import jsonschema
import json
from src.errorHandling import fatalError
from src.errorHandling import nonFatalError

configSchema = {
    "type": "object",
    "required": ["default settings", "fields"]
}

defaultSettingsSchema = {
    "type": "object",
    "required": ["PDF Path",
                 "Filled PDF Path",
                 "Prompt For Save Path",
                 "Spreadsheet Path",
                 "Spreadsheet Sheet Name",
                 "font size",
                 "text x offset",
                 "text y offset",
                 "checkbox size",
                 "checkbox line width"],
    "properties": {
    "PDF Path": {"type": "string"},
    "Prompt For Save Path": {"type": "boolean"},
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

fieldsSchema = {
    "type": "object",
    "required": ["type"],
    "properties": {
        "type": {
            "type": "string",
            "enum": ["multiChoiceCheckbox", "string"]    
        }
    }
}

multiChoiceSchema = {
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

multiChoiceOptionschema = {
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

stringSchema = {
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
    try:
        jsonschema.validate(instance=data, schema=configSchema)
    except jsonschema.ValidationError as error:
        fatalError(2,error.message)
    checkDefaultSettings(data["default settings"])
    checkFields(data["fields"])

# checks if the default settings are formatted correctly
def checkDefaultSettings(data):
    try:
        jsonschema.validate(instance=data, schema=defaultSettingsSchema)
    except jsonschema.ValidationError as e:
        fatalError(3,e.message)

# checks if the data fields are formatted correctly
def checkFields(data):
    #check schema to see if field is valid type
    for item in data:        
        try:
            jsonschema.validate(instance=item, schema=fieldsSchema)
        except jsonschema.ValidationError as error:
            fatalError(4, 'The following document field: "' + str(item["name"]) \
                       + '" has an invalid field type. ' + str(error.message))
        
        #check if properties of fields are accurate based on type
        match item["type"]:
            case "string":
                validateString(item)
            case "multiChoiceCheckbox":
                validateMultiChoiceCheckbox(item)

# checks if multi choice checkbox field items are formatted correctly
def validateMultiChoiceCheckbox(data):
    try:
        jsonschema.validate(instance=data, schema=multiChoiceSchema)
    except jsonschema.ValidationError as e:
        fatalError(6, 'document field "'+ str(data["name"]) +'" has invalid schema: ' + str(e.message))

    for option in data["options"]:
        try:
            jsonschema.validate(instance=option, schema=multiChoiceOptionschema)
        except jsonschema.ValidationError as e:
            fatalError(7,'multi choice checkbox option in "' + str(data["name"]) + '" field has invalid schema: ' + str(e.message))

# checks if string fields are formatted correctly
def validateString(data):
    try:
        jsonschema.validate(instance=data, schema=stringSchema)
    except jsonschema.ValidationError as e:
        fatalError(5, 'document field "'+ str(data["name"]) +'" has invalid schema: ' + str(e.message))

# changes a default setting in the coniguration file and re-saves the file
def changeFilepath(setting,filepath):
    config = parseConfigFile("config/Configuration.JSON")
    config["default settings"][setting] = filepath
    with open('config/Configuration.json', 'w') as json_file:
        json.dump(config, json_file, indent=4)

# pulls the JSON file defining the excel maping for translating an excel sheet to the configuration JSON
def parseExcelMaping(filepath):
    #load configuration file, throw error if not found
    try:
        with open(filepath, 'r') as FILE:
            data = json.load(FILE)
    except Exception as error:
        fatalError(14, 'Error reading Excel maping file: ' + str(error))

    #Verifies that the Configuration.JSON file has the correct schema
    checkExcelMapingSchema(data)

    return data

# checks if the excel maping file has all required fields
def checkExcelMapingSchema(data):
    schema = {
        "type": "object",
        "required": ["name" ,
                     "type",
                     "multi choice options",
                     "X insertion coordinate",
                     "Y insertion coordinate",
                     "cell reference",
                     "document page",
                     "coordinate units",
                     "excel file",
                     "sheet name"
                    ],
        "properties": {
            "name": {"type": "string"},
            "type": {"type": "string"},
            "multi choice options": {"type": "string"},
            "X insertion coordinate" : {"type": "string"},
            "Y insertion coordinate": {"type": "string"},
            "cell reference": {"type": "string"},
            "document page": {"type": "string"},
            "coordinate units": {"type": "string"},
            "excel file": {"type": "string"},
            "sheet name": {"type": "string"}
        }
    }

    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.ValidationError as e:
        fatalError(15,e.message)

# changes fields object in JSON using values from Excel Sheet
def changeFields(excelSheet):
    PDFConfig = parseConfigFile("config/Configuration.json")
    excelConfig = parseExcelMaping("config/excelMappings.json")

# same as parseConfigFile but doesn't end the program if the schema is bad
def parseConfigFileNoFail(filepath):
    #load configuration file, throw error if not found
    try:
        with open(filepath, 'r') as FILE:
            data = json.load(FILE)
    except Exception as error:
        fatalError(1, 'Error reading config: ' + str(error))

    #Verifies that the Configuration.JSON file has the correct schema
    checkConfigSchemaNoFail(data)

    return data

# same as CheckConfigSchema but doesn't end the program if the schema is bad
def checkConfigSchemaNoFail(data):
    try:
        jsonschema.validate(instance=data, schema=configSchema)
    except jsonschema.ValidationError as error:
        nonFatalError("Warning: the following piece of configuration.json is invalid and will " \
        "cause the PDF Filler to fail: " + str(error.message))
    checkDefaultSettingsNoFail(data["default settings"])
    checkFieldsNoFail(data["fields"], False)

# same as checkDefaultSettings but doesn't end the program if the schema is bad
def checkDefaultSettingsNoFail(data):
    try:
        jsonschema.validate(instance=data, schema=defaultSettingsSchema)
    except jsonschema.ValidationError as e:
        nonFatalError("Warning: the following piece of configuration.json is invalid and will " \
        "cause the PDF Filler to fail: " + str(e.message))

# same as checkFields but doesn't end the program if the schema is bad
def checkFieldsNoFail(data, supressWarnings):
    #check schema to see if field is valid type
    for item in data:        
        try:
            jsonschema.validate(instance=item, schema=fieldsSchema)
        except jsonschema.ValidationError as error:
            print("bad " + str(item["name"]))
            if not supressWarnings:
                nonFatalError('The document field: "' + str(item["name"]) \
                        + '" has an invalid field type and will cause'
                        ' the PDF filler to fail: ' + str(error.message))
            else:
                return False
        
        #check if properties of fields are accurate based on type
        match item["type"]:
            case "string":
                if not validateStringNoFail(item, supressWarnings):
                    return False
            case "multiChoiceCheckbox":
                if not validateMultiChoiceCheckboxNoFail(item, supressWarnings):
                    return False
        
    return True

# same as validateMultiChoiceCheckbox but doesn't end the program if the schema is bad
def validateMultiChoiceCheckboxNoFail(data, supressWarnings):
    try:
        jsonschema.validate(instance=data, schema=multiChoiceSchema)
    except jsonschema.ValidationError as e:
        if not supressWarnings:
            nonFatalError('The document field "'+ str(data["name"]) +'" has invalid '
            'schema and will cause the PDF Filler to fail: ' + str(e.message))
        else:
            return False

    for option in data["options"]:
        try:
            jsonschema.validate(instance=option, schema=multiChoiceOptionschema)
        except jsonschema.ValidationError as e:
            if not supressWarnings:
                nonFatalError('Multi choice checkbox option in "' + str(data["name"]) + '" field has invalid '
                            'schema and will cause the PDF Filler to fail: ' + str(e.message))
            else:
                return False
    return True

# same as validatString but doesn't end the program if the schema is bad
def validateStringNoFail(data, supressWarnings):
    try:
        jsonschema.validate(instance=data, schema=stringSchema)
    except jsonschema.ValidationError as e:
        if not supressWarnings:
            nonFatalError('Document field "'+ str(data["name"]) +'" has invalid schema: ' + str(e.message))
        else:
            return False
    return True