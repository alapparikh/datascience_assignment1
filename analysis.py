import csv
import dateutil.parser as p
import numpy as np
import data_prep as dp
from sklearn import preprocessing
from sklearn import linear_model

begin_yr = 1751
end_yr = 2008
total_yrs = 1+ end_yr - begin_yr
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
    
    
#data: Rows(features) Columns (years)
#Percent (ratio of sampling between Train and Test
#Direction (boolean): True: Train data cut from ealier, False: Train data cut from later in history
#Years: 
def sample_cut(years, data, percent, direction):
    targetVector = yearToTargetVector(years)
    
    #tmp = np.append(targetVector, 
    cut = int(percent*data.shape[0])
    
    if direction:
        train = data[:cut]
        train_target = targetVector[:cut]
        test = data[cut:]
        test_target = targetVector[cut:]        

    else:
        train = data[cut:]
        train_target = targetVector[cut:]
        test = data[:cut]
        test_target = targetVector[:cut]   
    return train, train_target, test, test_target

def yearToTargetVector(years):
    tmp = np.zeros(total_yrs)
    for year in years:
        tmp[1+year-begin_yr] = 1
    return tmp

def sample_random(data, percent, direction):
    cut = int(percent*data.shape[0])
    if (direction):
        train = data[:cut]
        test = data[cut:]
    else:
        train = data[cut:]
        test = data[:cut]
    return train, test

def train_model(train_matrix, target_vector):
    
    #Standardize features
    scaler = preprocessing.StandardScaler().fit(train_matrix)
    scaled_features = scaler.transform(train_matrix)

    #Fit logistic regression model
    classifier = linear_model.LogisticRegression(penalty='l2',dual=False)
    classifier.fit(scaled_features,target_vector)

    return classifier

def test_model(classifier, test_matrix, target_vector):
    correct_count = 0

    #Standardize features
    scaler = preprocessing.StandardScaler().fit(test_matrix)
    scaled_features = scaler.transform(test_matrix)

    predicted_eruptions = classifier.predict(scaled_features)
    for i,eruption in enumerate(predicted_eruptions):
        print eruption
        if eruption == 1:
            if target_vector[i] == 1:
                print True
            else:
                print False

		
years = get_volcano_years()
print years
data = import_data()

#print data[words.index('volcanos'), 1756-begin_yr]
train, train_target, test, test_target = sample_cut(years, data, 0.8, True)
classifier = train_model(train, train_target)
accuracy = test_model(classifier, test, test_target)
