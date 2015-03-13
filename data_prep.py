import re, string
import csv

#Relevant Google ngram files
files = ['googlebooks-eng-all-1gram-20120701-v', 'googlebooks-eng-all-1gram-20120701-i', 'googlebooks-eng-all-1gram-20120701-e', 
		'googlebooks-eng-all-1gram-20120701-l', 'googlebooks-eng-all-1gram-20120701-m', 'googlebooks-eng-all-2gram-20120701-vo']

#Words to be used as features
feature_words = ['volcano', 'volcanos', 'eruption', 'lava', 'molten', 'igneous', 'volcanic activity', 'volcanic eruption']

#Dictionary containing total count of words in each year
count_dict = {}

#Only import words after this year
begin_year = 1750

#Populate count dictionary
def get_total_count():
	
	with open('googlebooks-eng-all-totalcounts-20120701.txt', 'rU') as fp:

		for line in fp:
			rows = line.split('\t')

		for row in rows:
			values = row.split(',')
			
			if int(values[0]) > begin_year:
				count_dict[values[0]] = int(values[1])

	fp.close()

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
					if int(values[1]) > begin_year:
						relevant_data.append(values)

			print len(relevant_data)

		write_to_csv (relevant_data)

		fp.close()

#Write relevant data to CSV file
def write_to_csv(data):
	with open('word_data.csv', 'a') as fp:

		a = csv.writer(fp, delimiter='\t')

		for row in data:
			#Divide specific word count by total word count for that year to normalize it
			normalized_count = float(row[2])/count_dict[row[1]]
			a.writerow([row[0], row[1], normalized_count])

	fp.close()

if __name__ == '__main__':
	get_total_count()
	parse_data()