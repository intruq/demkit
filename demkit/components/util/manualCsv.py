import csv

def makeCSVs():
    joinCsv("CSV-House-8", ["SmartMeter-House-8", "Battery-House-8", "DishWasher-House-8", "DomesticHotWater-House-8", "DomesticHotWaterControllerBoiler-House-8", "Load-House-8", "HeatPump-House-8", "PV-House-8", "SmartGasMeter-House-8", "WashingMachine-House-8", "Zone-House-8"])
    joinCsv("CSV-Smart-Meters", ["SmartMeter-House-0", "SmartMeter-House-1", "SmartMeter-House-2", "SmartMeter-House-3", "SmartMeter-House-4", "SmartMeter-House-5", "SmartMeter-House-6", "SmartMeter-House-7", "SmartMeter-House-8", "SmartMeter-House-9"]) #S2 & S6

    shortenCSV("CSV-House-8")
    shortenCSV("CSV-Smart-Meters")

    modifierS1(True)
    modifierS1(False)
    modifierS2()
    modifierS3(True)
    modifierS3(False)
    modifierS4()
    modifierS5()
    modifierS6()

def modifierS1(option: bool):
    data = readCsv("CSV-House-8-short")

    if(option): # Smart Meter Value incorrect
        for i in range(1, len(data)):
            data[i][1] = float(data[i][1]) + 100
        writeCsv("CSV-MOD-S1-1", data) 
    else: # Device Values incorrect
        for i in range(1, len(data)):
            data[i][4] = float(data[i][4]) + 100
            data[i][7] = float(data[i][7]) + 100
            data[i][8] = float(data[i][8]) + 100
        writeCsv("CSV-MOD-S1-2", data)

def modifierS2():
    data = readCsv("CSV-Smart-Meters-short")
    for i in range(1, len(data)):
            data[i][i % 10] = 12001
    writeCsv("CSV-MOD-S2", data)

def modifierS3(option: bool):
    data = readCsv("CSV-House-8-short")

    if(option): # Battery soc over/under 100%/0% (12000 Wh Capacity)
        for i in range(1, len(data)):
            if(i % 2 == 1):
                data[i][3] = 12001
            else:
                data[i][3] = -1
        writeCsv("CSV-MOD-S3-1", data) 
    else: # Battery Charging while full/discharging while empty
        for i in range(1, len(data)):
            if(i % 2 == 1):
                data[i][3] = 12000 #soc
                data[i][2] = 100 #current
            else:
                data[i][3] = 0 #soc
                data[i][2] = -100 #current
        writeCsv("CSV-MOD-S3-2", data) 

def modifierS4():
    data = readCsv("CSV-House-8-short")
    for i in range(1, len(data)):
            data[i][4] = -1
    writeCsv("CSV-MOD-S4", data)

def modifierS5():
    data = readCsv("CSV-House-8-short")
    for i in range(1, len(data)):
            if(i % 2 == 1):
                data[i][2] = 3800
            else:
                data[i][2] = -3800
    writeCsv("CSV-MOD-S5", data)

def modifierS6():
    data = readCsv("CSV-Smart-Meters-short")
    for i in range(1, len(data)):
            if i % 3 == 0:
                var = 0
            elif i % 3 == 1:
                var = 5000
            else:
                var = 10000
            data[i][1] = var
    writeCsv("CSV-MOD-S6", data)

def modifierS7():
    True

# Removes all columns not needed in the IDS for clarity
def shortenCSV(source: str):
    sourceData = readCsv(source)
    headerIndices = [0]
    columnCount = len(sourceData[0])

    for i in range(columnCount):
        header = sourceData[0][i]
        if ("power.real.c.ELECTRICITY" in header) or ("energy.soc" in header):
            headerIndices.append(i)

    output = [[val for j, val in enumerate(row) if j in headerIndices] for row in sourceData]
    writeCsv(source + "-short", output)

# Joins CSVs from the fileNameList
def joinCsv(fileName, fileNameList: list):
    joinedData, sourceData, columnDepth, header = [], [], [], ["time"]

    #Load all needed CSVs into one list
    for source in fileNameList:
        sourceData.append(readCsv(source))

    columnDepth = calcListColumnDepth(sourceData)

    maxTime = 0
    for i in range(len(sourceData)):
        try:
            value = sourceData[i][-1][0]
        except IndexError:
            value = 0
        if maxTime < int(value):
            maxTime = int(value)

    if maxTime > 0:
        # Create header
        for i in range(len(fileNameList)):
            for j in range(1, columnDepth[i]):
                header.append(fileNameList[i] + ": " + sourceData[i][0][j])
        joinedData.append(header)

        #Extracts data from CSVs row by row and adds them to output file
        for i in range(1, (maxTime // 60) - 1):
            #reinitialize row
            time = sourceData[0][i][0]
            row = [time]
            for j in range(len(sourceData)):
                try:
                    for k in range(1, columnDepth[j]):
                        row.append(sourceData[j][i][k])
                except IndexError:
                    row.append(0)
            joinedData.append(row)

        writeCsv(fileName, joinedData)

#Calculates how many measurements each input-CSV contains
def calcListColumnDepth(data: list):
    output = []

    for i in range(len(data)):
        try:
            output.insert(i, len(data[i][0]))
        except IndexError:
            output.insert(i, 0)
    return output

# Input: CSV, Output: List
def readCsv(fileName):
    data = []

    if not fileName.endswith('.csv'):
        fileName += '.csv'

    # Reading data from a CSV file
    with open("C:/Users/intruq/Desktop/Bachelorarbeit/DEMKit/workspace/example/data/" + fileName, mode='r', newline='') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            data.append(row)

    return data

# Input: List, Output: CSV
def writeCsv(fileName, data: list):
    if not fileName.endswith('.csv'):
        fileName += '.csv'
    
    # Writing data to a CSV file
    with open("C:/Users/intruq/Desktop/Bachelorarbeit/DEMKit/workspace/example/data/" + fileName, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(data)

def devLogCsv(fileName, data: list):
    if len(data) > 0:
        measurementCount = int(len(data) / 10080) #10080 is number of entries for one measurement type

        dataSorted, header = [], []

        #Header
        header.append("time")
        for i in range(measurementCount):
            header.append(data[i][2])
        dataSorted.append(header)

        #Values
        for i in range(10079):
            row = [data[i * measurementCount][0]]
            for j in range(measurementCount):
                row.append(data[(i * measurementCount) + j][3])
            dataSorted.append(row)

        writeCsv(fileName, dataSorted)

makeCSVs()