import re, string
import csv

def parse_data():
	with open('googlebooks-eng-all-1gram-20120701-v', 'rU') as f:

		#reader = csv.reader(f)
		count = 0
		#header = f.readline()

		for row in f:	
			values = row.split('\t')
			count += 1;

			if values[0] == 'volcano':
				

		print count

			#if count == 10:
			#	break

if __name__ == '__main__':
	parse_data()