import re, string
import csv

files = ['googlebooks-eng-all-1gram-20120701-v', 'googlebooks-eng-all-1gram-20120701-i', 'googlebooks-eng-all-1gram-20120701-e', 
		'googlebooks-eng-all-1gram-20120701-l', 'googlebooks-eng-all-1gram-20120701-m', 'googlebooks-eng-all-2gram-20120701-vo']

def parse_data():
	relevant_data = []

	with open('googlebooks-eng-all-2gram-20120701-vo', 'rU') as f:

		#reader = csv.reader(f)
		count = 0

		for row in f:	
			values = row.split('\t')
			count += 1;

			if values[0] == 'volcanic ':
				relevant_data.append(values)

		print len(relevant_data)

	write_to_csv (relevant_data)

def write_to_csv(data):
	with open('test.csv', 'a') as fp:
		a = csv.writer(fp, delimiter='\t')
		for row in data:
			a.writerow(row)

if __name__ == '__main__':
	parse_data()