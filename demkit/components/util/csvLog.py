import csv

def openCsv(file_name):
    if not file_name.endswith('.csv'):
        file_name += '.csv'
    

    file = open("./data/" + file_name, mode='w+', newline='')
    file.close()
    #print("CSV: File Truncated")

def logCsv(file_name, data):
    if not file_name.endswith('.csv'):
        file_name += '.csv'

    # Writing data to a CSV file
    with open("./data/" + file_name, mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(data)

