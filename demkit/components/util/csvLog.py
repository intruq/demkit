import csv

def log(fileName, data, header):
    if not fileName.endswith('.csv'):
        fileName += '.csv'
    
    # Writing data to a CSV file
    with open("./data/" + fileName, mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=';', fieldnames=header)
        writer.writerows(data)

def logCsv(fileName, data):
    measurementCount = data.count / 10080 #10080 is number of entries for one measurement type
    print(measurementCount)

    header = []
    header[0] = "time"
    for i in range(measurementCount):
        header[i + 1] = data[i][3]
        
    dataSorted = []

    for i in range(10080):
        for j in range(measurementCount):
            dataSorted[i + 1][j + 1] = data[(i * measurementCount) + 1][4]

    log(fileName, dataSorted, header)