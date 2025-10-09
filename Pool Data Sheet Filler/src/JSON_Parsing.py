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

import jsonschema
import json
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

    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.ValidationError as e:
        fatalError(3,e.message)

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

# changes a default setting in the coniguration file and re-saves the file
def changeFilepath(setting,filepath):
    config = parseConfigFile("Configuration.JSON")
    config["default settings"][setting] = filepath
    with open('Configuration.json', 'w') as json_file:
        json.dump(config, json_file, indent=4)