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

#main run context
def run():
    configuration = parseConfigFile("config/Configuration.json")
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