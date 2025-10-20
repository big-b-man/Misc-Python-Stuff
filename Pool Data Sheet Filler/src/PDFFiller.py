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

# hours: 
# sept 16: 2
# sept 17: 1
# sept 18: 2
# sept 26: 1
# sept 28: 8
# oct 1: 1.5
# oct 3: 2

import pymupdf
import os
import src.fileIO as IO
from src.errorHandling import *
from src.JSON_Parsing import *
from src.writeDoc import *
import traceback

#main run context
def run():
    configuration = parseConfigFile("config/Configuration.json")
    PDFPath = configuration["default settings"]["PDF Path"]
    FilledPDFPath = configuration["default settings"]["Filled PDF Path"]
    SpreadsheetPath= configuration["default settings"]["Spreadsheet Path"]
    SpreadsheetSheetName = configuration["default settings"]["Spreadsheet Sheet Name"]
    # Throws error if PDF can't be opened
    try:
        doc = pymupdf.open(PDFPath)
    except Exception as error:
        with open('log.txt', 'w') as f:
            f.write(traceback.format_exc())
        fatalError(12,"Unable to open Source PDF file. Traceback has been written to log file")

    excelData = IO.readExcel(SpreadsheetPath, sheet_name=SpreadsheetSheetName, header=None)
    writedoc(doc, excelData, configuration)
    #Throws error if PDF can't be written
    try:
        doc.save(FilledPDFPath)
    except:
        with open('log.txt', 'w') as f:
            f.write(traceback.format_exc())
        fatalError(13,"Unable to save new PDF file. Traceback has been written to log file")
    doc.close()
    os.startfile(FilledPDFPath)