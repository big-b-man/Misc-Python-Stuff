import pandas as pd
from datetime import datetime

# reads spreadsheet file and returns as list of lists
def readExcel(filePath, **kwargs):
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