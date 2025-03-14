import csv

#takes the openprop curves and parses them into code that can be copied into an onShape feature script

def LoadCSV(filePath):
    #parse hull profile and load into memory
    with open(filePath, 'r') as file:
        reader = csv.reader(file)
        # Insert First two columns into list
        data = [[float(x) for x in row[:3]] for row in reader]
    return data

with open("code.txt", 'w') as file:
    file.write('FeatureScript 2599;\n' + 'import(path : "onshape/std/common.fs", version : "2599.0");\n\n')

with open("code.txt", 'a') as file:
    file.write('//Name of feature so we can select it in the Part Studio\n')
    file.write('annotation { "Feature Type Name" : "Prop Loft" }\n')
    file.write('export const propLoft = defineFeature(function(context is Context, id is Id, definition is map)\n')
    file.write('    precondition{}\n')
    file.write('    {\n')
    file.write('        const offsets = [\n')
    code = str()

    for i in range (19): #number of curves minus 1
        data = LoadCSV("SectionCurve" + str(i+1) + ".txt")
        file.write('                        ' + str(data[0][2]) + ' * meter,\n')

    #last code snipet doesn't have colon
    data = LoadCSV("SectionCurve" + str(20) + ".txt")
    file.write('                        ' + str(data[0][2]) + ' * meter\n')
    file.write('                        ];\n\n')
    file.write('        const points = [[\n')

    for i in range (19): #number of curves minus 1
        data = LoadCSV("SectionCurve" + str(i+1) + ".txt")
        file.write('                        //Curve ' + str(i+1) +'\n')
        for j in range(len(data) - 1):
            file.write('                        vector(')
            file.write(str(data[j][0])+','+str(data[j][1]) + ') * meter,\n')
        #last code snipet doesn't have colon
        file.write('                        vector(')
        file.write(str(data[len(data)-1][0])+','+str(data[len(data)-1][1]) + ') * meter\n')
        file.write('                    ],[\n')
    
    #last code snipet doesn't have colon
    data = LoadCSV("SectionCurve" + str(20) + ".txt")
    file.write('                        //Curve ' + str(20) +'\n')
    for j in range(len(data) - 1):
        file.write('                        vector(')
        file.write(str(data[j][0])+','+str(data[j][1]) + ') * meter,\n')
    file.write('                        vector(')
    file.write(str(data[len(data)-1][0])+','+str(data[len(data)-1][1]) + ') * meter\n')
    file.write('                    ]];\n\n')
    file.write('        //create sketch planes from imported data\n')
    file.write('        var sketchId = id + "sketch";\n')
    file.write('        for (var i = 0; i < 20; i += 1)\n')
    file.write('        {\n')
    file.write('            //define plane offset\n')
    file.write('            var offsetDistance = offsets[i];\n')
    file.write('            sketchId = sketchId + i;\n')
    file.write('            // Define the offset plane (offset along Z-axis)\n')
    file.write('            const offsetPlane = plane(vector(0*inch, 0*inch, offsetDistance), vector(0, 0, 1)*inch);\n')
    file.write('            var sketch1 = newSketchOnPlane(context, sketchId, { "sketchPlane" : offsetPlane });\n')
    file.write('            //sketch some stuff here\n')
    file.write('            \n')
    file.write('            skFitSpline(sketch1, "spline1", {\n')
    file.write('                    "points" : points[i]\n')
    file.write('            });\n')
    file.write('        \n')
    file.write('            // Finalize the sketch\n')
    file.write('            skSolve(sketch1);\n')
    file.write('        }\n')
    file.write('    });\n')