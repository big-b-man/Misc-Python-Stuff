import csv

#takes the openprop curves and parses them into code that can be copied into an onShape feature script

def LoadCSV(filePath):
    #parse hull profile and load into memory
    with open(filePath, 'r') as file:
        reader = csv.reader(file)
        # Insert First two columns into list
        data = [[float(x) for x in row[:3]] for row in reader]
    return data

file = open("code.txt", 'w')
file.close
    

with open("code.txt", 'a') as file:
    with open('preCode.txt', 'r') as preCode:
        file.write(preCode.read())

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
    with open('postCode.txt', 'r') as postCode:
        file.write(postCode.read())