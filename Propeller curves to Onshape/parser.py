import csv, ezdxf

def LoadCSV(filePath):
    #parse hull profile and load into memory
    with open(filePath, 'r') as file:
        reader = csv.reader(file)
        # Insert First two columns into list
        data = [[float(x) for x in row[:3]] for row in reader]
    return data

for i in range (20):
    data = LoadCSV("SectionCurve" + str(i+1) + ".txt")
    print(str(i+1) + ": " + str(data[0][2]))
    doc = ezdxf.new()
    for j in range(len(data)):
        data[j][2] = 0
    msp = doc.modelspace()
    spline = msp.add_spline(data)
    doc.saveas(str(i+1) + ".dxf")