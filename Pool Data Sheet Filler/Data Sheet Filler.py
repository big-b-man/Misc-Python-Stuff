import pymupdf
import pandas as pd

#General Style Notes: 12 Point font, offset 6 point from base of cell

def safe_insert_text(page, position, value, **kwargs):
    # Handle NaN/NaT/missing values
    if pd.isna(value):
        value = ""
    else:
        value = str(value)
    print(value)
    page.insert_text(position, value, **kwargs)

def writedoc(doc, healthData):
    #Page 2: Application to:
    
    #Health Authority Checkbox
    match(healthData.iloc[1,1]):
        case "Fraser":
            doc[1].draw_line([ 41.2, 149.2],[ 49.2, 157.9],color=(1,0,0),width=3)
        case "Interior": 
            doc[1].draw_line([161.7, 149.2],[169.7, 157.9],color=(1,0,0),width=3)
        case "Coastal":
            doc[1].draw_line([256.8, 149.2],[264.8, 157.9],color=(1,0,0),width=3)
        case "Island":
            doc[1].draw_line([369.3, 149.2],[377.3, 157.9],color=(1,0,0),width=3)
        case "Northern":
            doc[1].draw_line([481.9, 149.2],[489.9, 157.9],color=(1,0,0),width=3)
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

    for page in doc:
        page.insert_text([0,12], "Hello World!", fontsize=12, color=None, overlay=True)

doc = pymupdf.open("Pool-construction-permit-application-form.pdf")
excelData = pd.read_excel("Test Sheet.xlsx",sheet_name="Pool Data For Export", header=None)
print ("Excel Data read:\n",excelData)
writedoc(doc,excelData)
doc.save("Filled Data Sheet.pdf")
doc.close()