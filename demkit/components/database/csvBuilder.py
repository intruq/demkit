import csv

def write_csv(data):
    with open('data.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')
        csv_writer.writerow([data])

data3 = "data3"
data4 = "data4"
write_csv(data3)
write_csv(data4)