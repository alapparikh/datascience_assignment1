import re, string
import csv

#Relevant Google ngram files
files = ['googlebooks-eng-all-1gram-20120701-v', 'googlebooks-eng-all-1gram-20120701-i', 'googlebooks-eng-all-1gram-20120701-e', 
		'googlebooks-eng-all-1gram-20120701-l', 'googlebooks-eng-all-1gram-20120701-m', 'googlebooks-eng-all-2gram-20120701-vo']

#Words to be used as features
feature_words = ['volcano', 'volcanos', 'eruption', 'lava', 'molten', 'igneous', 'volcanic activity', 'volcanic eruption']

#Get relevant data from each ngram file
def parse_data():

	for f in files:
		relevant_data = []

		with open(f, 'rU') as fp:
			count = 0

			for row in fp:	
				values = row.split('\t')
				count += 1;

				if values[0] in feature_words:
					if int(values[1]) > 1750:
						relevant_data.append(values)

			print len(relevant_data)

		write_to_csv (relevant_data)

def write_to_csv(data):
	with open('word_data.csv', 'a') as fp:
		a = csv.writer(fp, delimiter='\t')
		for row in data:
			a.writerow([row[0], row[1], row[2]])

if __name__ == '__main__':
	parse_data()