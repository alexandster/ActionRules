import csv

reader = csv.reader(open("../Data/fragile_states.csv", 'rU'), dialect=csv.excel_tab)
print reader
for row in reader:
	print row
