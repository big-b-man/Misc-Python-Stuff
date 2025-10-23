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
        fatalError(14,"Unable to open excel file. Traceback has been written to log file")

# gets sheet name from an excel file
def getSheetNames(filePath):
    try:
        tempSheet = pd.ExcelFile(filePath)
        return tempSheet.sheet_names
    except Exception as error:
        with open('log.txt', 'w') as f:
            f.write(traceback.format_exc())
        fatalError(15,"Unable to open excel file. Traceback has been written to log file")