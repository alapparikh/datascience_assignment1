import csv
import dateutil.parser as p
import numpy as np
import data_prep as dp

begin_yr = 1750
end_yr = 2008
words = dp.feature_words

def get_volcano_years():
    years = []
    with open('volcano_data_raw.txt', 'rb') as fp:
        reader = csv.reader(fp, delimiter='\t')
        for row in reader:
            years.append(p.parse(row[3]).year)
            #print p.parse(row[3]).year
    return years

        
def import_data():
    total_yrs = 1+ end_yr - begin_yr
    word_count = len(words)
    data = np.zeros((word_count, total_yrs))
    with open('word_data.csv', 'rb') as fp:
        reader = csv.reader(fp, delimiter='\t')
        for row in reader:
            #print row
            data[words.index(row[0]), int(row[1])-begin_yr] = row[2]
    return data
    

		
years = get_volcano_years()
print years

data = import_data()

#print data[words.index('volcanos'), 1756-begin_yr]

