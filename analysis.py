import csv
import dateutil.parser as p
import numpy as np
import data_prep as dp
from sklearn import preprocessing

from sklearn import linear_model

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
    data = np.zeros((total_yrs, word_count))
    with open('word_data.csv', 'rb') as fp:
        reader = csv.reader(fp, delimiter='\t')
        for row in reader:
            #print row
            data[int(row[1])-begin_yr, words.index(row[0])] = row[2]
    return data
    
    
#data: Rows(years) Columns (features)
#Percent (ratio of sampling between Train and Test
#Direction (boolean): True: Train data cut from ealier, False: Train data cut from later in history
def sample_cut(data, percent, direction):
   cut = int(percent*data.shape[0])
    if (direction):
        train = data[:cut]
        test = data[cut:]
    else:
        train = data[cut:]
        test = data[:cut]
    return train, test


def sample_random(data, percent, direction):
    cut = int(percent*data.shape[0])
    if (direction):
        train = data[:cut]
        test = data[cut:]
    else:
        train = data[cut:]
        test = data[:cut]
    return train, test


		
years = get_volcano_years()
print years
data = import_data()

#print data[words.index('volcanos'), 1756-begin_yr]
train, test = sample_cut(data, 0.1, True)

