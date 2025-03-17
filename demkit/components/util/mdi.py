import csv

def writeCsv(fileName, data: list):
    if not fileName.endswith('.csv'):
        fileName += '.csv'
    
    # Writing data to a CSV file
    with open("./data/" + fileName, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(data)

def storeMeterData(fileName, data: list):
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