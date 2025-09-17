# Pool Data Sheet Filler Tool
#
# Copyright (C) 2025 Bennett Steers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pymupdf
import pandas as pd
import os

#General Style Notes: 12 Point font, offset 6 point from base of cell

ExcelPath = "Pool-construction-permit-application-form.pdf"
FilledPDFPath = "Filled Data Sheet.pdf"

def safe_insert_text(page, position, value, **kwargs):
    # Handle NaN/NaT/missing values
    if pd.isna(value):
        value = ""
    else:
        value = str(value)
    print(value)
    page.insert_text(position, value, **kwargs)

def writedoc(doc, healthData):
    #Page 2
    #Application to
    
    #Health Authority Checkbox
    match(healthData.iloc[1,1]):
        case "Fraser":
            doc[1].draw_line([ 41, 149],[ 49, 158],color=(1,0,0),width=3)
        case "Interior": 
            doc[1].draw_line([162, 149],[170, 158],color=(1,0,0),width=3)
        case "Coastal":
            doc[1].draw_line([257, 149],[265, 158],color=(1,0,0),width=3)
        case "Island":
            doc[1].draw_line([369, 149],[377, 158],color=(1,0,0),width=3)
        case "Northern":
            doc[1].draw_line([482, 149],[490, 158],color=(1,0,0),width=3)
        case _:
            print("Page 2: No Health Authority Defined")

    #Pool Name, Date, and Address
    safe_insert_text(doc[1], [37,210], healthData.iloc[2,1], color=None, fontsize=12, overlay=True)
    safe_insert_text(doc[1], [412,210], healthData.iloc[2,3], color=None, fontsize=12, overlay=True)
    safe_insert_text(doc[1], [37,239], healthData.iloc[3,1], color=None, fontsize=12, overlay=True)

    #Owner Info
    safe_insert_text(doc[1], [37,289], healthData.iloc[5,1], color=None, fontsize=12, overlay=True)
    safe_insert_text(doc[1], [37,318], healthData.iloc[6,1], color=None, fontsize=12, overlay=True)
    safe_insert_text(doc[1], [37,345], healthData.iloc[7,1], color=None, fontsize=12, overlay=True)
    safe_insert_text(doc[1], [254,345], healthData.iloc[7,3], color=None, fontsize=12, overlay=True)    

    #Person Applying for Permit Info
    safe_insert_text(doc[1], [37,395], healthData.iloc[9,1], color=None, fontsize=12, overlay=True)
    safe_insert_text(doc[1], [37,422], healthData.iloc[10,1], color=None, fontsize=12, overlay=True)
    safe_insert_text(doc[1], [37,451], healthData.iloc[11,1], color=None, fontsize=12, overlay=True)
    safe_insert_text(doc[1], [254,451], healthData.iloc[11,3], color=None, fontsize=12, overlay=True)

    #Page 3:
    #General Information
    safe_insert_text(doc[2], [103,146], healthData.iloc[14,1], color=None, fontsize=12, overlay=True)
    safe_insert_text(doc[2], [103,172], healthData.iloc[15,1], color=None, fontsize=12, overlay=True)

    #Pool Type Checkbox
    match(healthData.iloc[16,1]):
        case "Public Pool":
            doc[2].draw_line([180, 186],[188, 195],color=(1,0,0),width=3)
        case "Commercial Pool": 
            doc[2].draw_line([282, 186],[290, 195],color=(1,0,0),width=3)
        case "Hot Tub":
            doc[2].draw_line([343, 186],[351, 195],color=(1,0,0),width=3)
        case "Spray Pool":
            doc[2].draw_line([414, 186],[422, 195],color=(1,0,0),width=3)
        case "Wading Pool":
            doc[2].draw_line([497, 186],[505, 195],color=(1,0,0),width=3)
        case _:
            print("Page 3: No Pool Type Defined")

    for page in doc:
        page.insert_text([0,12], "Hello World!", fontsize=12, color=None, overlay=True)

doc = pymupdf.open(ExcelPath)
excelData = pd.read_excel("Test Sheet.xlsx",sheet_name="Pool Data For Export", header=None)
print ("Excel Data read:\n",excelData)
writedoc(doc,excelData)
doc.save(FilledPDFPath)
doc.close()
os.startfile(FilledPDFPath)