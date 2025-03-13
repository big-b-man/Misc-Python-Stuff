import csv

#takes the openprop curves and parses them into code that can be copied into an onShape feature script

def LoadCSV(filePath):
    #parse hull profile and load into memory
    with open(filePath, 'r') as file:
        reader = csv.reader(file)
        # Insert First two columns into list
        data = [[float(x) for x in row[:3]] for row in reader]
    return data

code = str()
code = code + 'FeatureScript 2599;\n' + 'import(path : "onshape/std/common.fs", version : "2599.0");\n\n'
code = code + '//Name of feature so we can select it in the Part Studio\n' + 'annotation { "Feature Type Name" : "Prop Loft" }\n'
code = code + 'export const propLoft = defineFeature(function(context is Context, id is Id, definition is map)\n'
code = code + '    precondition{}\n' + '    {\n' + '        const offsets = [\n'

for i in range (19): #number of curves minus 1
    data = LoadCSV("SectionCurve" + str(i+1) + ".txt")
    code = code + '                        ' + str(data[0][2]) + ' * meter,\n'

#last code snipet doesn't have colon
data = LoadCSV("SectionCurve" + str(20) + ".txt")
code = code + '                        ' + str(data[0][2]) + ' * meter\n'
code = code + '                        ];\n\n'
code = code + '        const points = [[\n'

for i in range (19): #number of curves minus 1
    data = LoadCSV("SectionCurve" + str(i+1) + ".txt")
    code = code + '                        //Curve ' + str(i+1) +'\n'
    for j in range(len(data) - 1):
        code = code + '                        vector('
        code = code + str(data[j][0])+','+str(data[j][1]) + ') * meter,\n'
    code = code + '                        vector('
    code = code + str(data[len(data)-1][0])+','+str(data[len(data)-1][1]) + ') * meter\n'
    code = code + '                    ],[\n'

data = LoadCSV("SectionCurve" + str(20) + ".txt")
code = code + '                        //Curve ' + str(20) +'\n'
for j in range(len(data) - 1):
    code = code + '                        vector('
    code = code + str(data[j][0])+','+str(data[j][1]) + ') * meter,\n'
code = code + '                        vector('
code = code + str(data[len(data)-1][0])+','+str(data[len(data)-1][1]) + ') * meter\n'
code = code + '                    ]];\n'

with open("code.txt", 'w') as file:
    file.write(code)
