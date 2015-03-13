import csv

with open('test.csv', 'rb') as fp:
	reader = csv.reader(fp, delimiter='\t')
	for row in reader:
		print row