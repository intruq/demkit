import csv

def write_to_csv(data, file_name):
  
    # Ensure the file name ends with '.csv'
    if not file_name.endswith('.csv'):
        file_name += '.csv'
    
    # Writing data to a CSV file
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def printToConsole(msg):
    print(msg)