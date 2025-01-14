import csv

def makeCSVs():
    joinCsv("CSV-Load-House1", ["Load-House-0", "Load-House-1"])
    joinCsv("CSV-EV", ["ElectricVehicle-House-0", "ElectricVehicle-House-1"])
    joinCsv("CSV-EV-Load-House", ["ElectricVehicle-House-0", "Load-House-0"])
    joinCsv("CSV-House-0", ["DomesticHotWater-House-0", "ElectricVehicle-House-0", "GasBoiler-House-0", "Load-House-0", "SmartGasMeter-House-0", "SmartMeter-House-0", "WashingMachine-House-0", "Zone-House-0"])
    joinCsv("CSV-House-8", ["Load-House-8", "Battery-House-8", "DishWasher-House-8", "DomesticHotWater-House-8", "DomesticHotWaterControllerBoiler-House-8", "HeatPump-House-8", "PV-House-8", "SmartGasMeter-House-8", "SmartMeter-House-8", "WashingMachine-House-8", "Zone-House-8"])
    joinCsv("CSV-House-8-Electric", ["SmartMeter-House-8", "Battery-House-8", "DishWasher-House-8", "HeatPump-House-8", "Load-House-8", "PV-House-8", "WashingMachine-House-8"])

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