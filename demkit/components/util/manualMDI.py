import csv
import shutil

path = "C:/Users/intruq/Desktop/Bachelorarbeit/DEMKit/workspace/example/data/"

def makeCSVs():
    joinCsv("CSV-House-1", ["SmartMeter-House-1", "Load-House-1", "WashingMachine-House-1", "Dishwasher-House-1", "ElectricVehicle-House-1", "Heatpump-House-1", "DomesticHotWaterControllerBoiler-House-1", "PV-House-1"])
    joinCsv("CSV-House-4", ["SmartMeter-House-4", "Load-House-4", "WashingMachine-House-4", "ElectricVehicle-House-4"])
    joinCsv("CSV-House-8", ["SmartMeter-House-8", "Load-House-8", "WashingMachine-House-8", "Dishwasher-House-8", "Battery-House-8", "Heatpump-House-8", "DomesticHotWaterControllerBoiler-House-8", "PV-House-8"])

    shortenCSV("CSV-House-1")
    shortenCSV("CSV-House-4")
    shortenCSV("CSV-House-8")
    feeder("")

    att_scenario_1()
    att_scenario_2()
    att_scenario_3()
    #att_scenario_4()

def att_scenario_1():
    shutil.copy(path + "CSV-House-1-short.csv", path + "att_scenario_1/CSV-House-1.csv")
    shutil.copy(path + "CSV-House-4-short.csv", path + "att_scenario_1/CSV-House-4.csv")
    shutil.copy(path + "CSV-House-8-short.csv", path + "att_scenario_1/CSV-House-8.csv")
    feeder("att_scenario_1/")

def att_scenario_2():
    as1_var_1()
    as1_var_2()
    as1_var_3()

def att_scenario_3():
    data1, data2 = readCsv("CSV-House-1-short"), readCsv("CSV-House-8-short")
    for i in range(1, len(data1)):
        if(i % 2 == 1):
            data1[i][1] = float(data1[i][1]) - float(data1[i][4])
            data2[i][1] = float(data2[i][1]) - float(data2[i][4])
            data1[i][4] = 0
            data2[i][4] = 0
        else:
            data1[i][4] = -11999
            data2[i][4] = -11999
            data1[i][1] = float(data1[i][1]) - 11999
            data2[i][1] = float(data2[i][1]) - 11999
    writeCsv("att_scenario_3/CSV-House-1", data1)
    writeCsv("att_scenario_3/CSV-House-8", data2)
    shutil.copy(path + "CSV-House-4-short.csv", path + "att_scenario_3/CSV-House-4.csv")
    feeder("att_scenario_3/")

def att_scenario_4():
    feeder("att_scenario_4/")

def as1_var_1():
    data = readCsv("CSV-House-8-short")
    for i in range(1, len(data)):
        data[i][5] = 13000 # Max capacity of power line: 12000W
        data[i][6] = 4000 # Max capacity of Medium ALPG battery: 4000Wh 
    writeCsv("att_scenario_2/var1/CSV-House-8", data)
    shutil.copy(path + "CSV-House-1-short.csv", path + "att_scenario_2/var1/CSV-House-1.csv")
    shutil.copy(path + "CSV-House-4-short.csv", path + "att_scenario_2/var1/CSV-House-4.csv")
    feeder("att_scenario_2/var1/")

def as1_var_2():
    data = readCsv("CSV-House-8-short")
    for i in range(1, len(data)):
        if(i % 2 == 1):
            data[i][6] = 5000 # Max capacity of Medium ALPG battery: 4000Wh 
        else:
            data[i][6] = -1
    writeCsv("att_scenario_2/var2/CSV-House-8", data)
    shutil.copy(path + "CSV-House-1-short.csv", path + "att_scenario_2/var2/CSV-House-1.csv")
    shutil.copy(path + "CSV-House-4-short.csv", path + "att_scenario_2/var2/CSV-House-4.csv")
    feeder("att_scenario_2/var2/")

def as1_var_3():
    data = readCsv("CSV-House-8-short")
    for i in range(1, len(data)):
        data[i][5] = (-1) * float(data[i][5])
    writeCsv("att_scenario_2/var3/CSV-House-8", data)
    shutil.copy(path + "CSV-House-1-short.csv", path + "att_scenario_2/var3/CSV-House-1.csv")
    shutil.copy(path + "CSV-House-4-short.csv", path + "att_scenario_2/var3/CSV-House-4.csv")
    feeder("att_scenario_2/var3/")

# Function collecting SmartMeter data and adding values to get combined input/output of all houses
def feeder(folder: str):
    data, sourceData = [["time", "W-power.real.c.ELECTRICITY"]], []
    for m in ["CSV-House-1", "CSV-House-4", "CSV-House-8"]:
        sourceData.append(readCsv(folder + m))
    try:
        maxTime = int(sourceData[0][-1][0])
    except IndexError:
        maxTime = 0
    if maxTime > 0:
        for i in range(1, (maxTime // 60) - 1):
            time = sourceData[0][i][0]
            sum_meters = 0
            for j in range(3):
                sum_meters += float(sourceData[j][i][1])
            data.append([time, sum_meters])
        writeCsv(folder + "CSV-Feeder", data)

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
    writeCsv("att_scenario_1/" + source + "-short", output)

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
    with open(path + fileName, mode='r', newline='') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            data.append(row)

    return data

# Input: List, Output: CSV
def writeCsv(fileName, data: list):
    if not fileName.endswith('.csv'):
        fileName += '.csv'
    
    # Writing data to a CSV file
    with open(path + fileName, mode='w', newline='') as file:
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