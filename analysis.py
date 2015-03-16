import csv
import dateutil.parser as p
import numpy as np
import data_prep as dp
from sklearn import preprocessing
from sklearn import linear_model
from sklearn import preprocessing
from sklearn import linear_model
from sklearn import svm
from sklearn import neighbors
from sklearn.lda import LDA
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier

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
def sample_cut(years, data, percent, direction, shift_amt):
    targetVector = yearToTargetVector(years, shift_amt)    
    #tv = np.array([targetVector.tolist()])
    #temp = np.concatenate((tv.T, data), axis = 1)

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

def yearToTargetVector(years, shift_amt):
    tmp = np.zeros(total_yrs-shift_amt)
    for year in years:
        tmp[1+year-begin_yr] = 1
    return tmp

def yearsToTargetVector(years):
    tmp = []
    for i in range(total_yrs):
        if i+begin_yr in years:
            tmp.append([1])
        else:
            tmp.append([0])
    return tmp

def sample_random(data, percent, direction):
    #TODO:
    return 0

def train_model(train_matrix, target_vector, classifier):
    
    #Standardize features
    scaler = preprocessing.StandardScaler().fit(train_matrix)
    scaled_features = scaler.transform(train_matrix)

    #Fit logistic regression model
    classifier.fit(scaled_features,target_vector)
    


    return classifier

def test_model(classifier, test_matrix, target_vector):
    correct_count = 0

    #Standardize features
    scaler = preprocessing.StandardScaler().fit(test_matrix)
    scaled_features = scaler.transform(test_matrix)

    TP = 0
    FP = 0
    TN = 0
    FN = 0
    
    predicted_eruptions = classifier.predict(scaled_features)
    for i,guessed_eruption in enumerate(predicted_eruptions):
        #print eruption
        if guessed_eruption == 1:
            if target_vector[i] == 1:
                #print "\t"+str(True)+" "+str(classifier)[:15]
                TP += 1
            else:
                FP += 1
                #print False
    if TP + FP == 0 or TP == 0:
        #print "\tNONE\t"+str(classifier)[:10]        
        0
    elif float(TP)/(TP+FP) > 0.7:    
        print "\t"+ str(float(TP)/(TP+FP))+"\t"+str(classifier)[:10]
            

def shift(amount, data, years):
    new_data = data[amount:]
    new_years = []
    for year in years:
        if year+amount <= end_yr:
            new_years.append(year+amount)
    return new_data, new_years

				

def spray_n_pray(master_data, master_years):
    for i in range(10):
        print "Shifting by: "+str(i)
        data, years = shift(i, master_data, master_years)
    
    
        #print data[words.index('volcanos'), 1756-begin_yr]
        percentage  = 0.3
        while percentage <= 1.0:
            print "    Percentage "+str(percentage)
            train, train_target, test, test_target = sample_cut(years, data, percentage, True, i)
            
            classifiers = [linear_model.LogisticRegression(penalty='l2',dual=False), 
            linear_model.SGDClassifier(),
            svm.LinearSVC(),
            svm.SVC(kernel = 'rbf'),
            linear_model.Perceptron(penalty='l1'),
            linear_model.Perceptron(penalty='l2',n_iter = 25),
            neighbors.KNeighborsClassifier(),
            LDA(),
            tree.DecisionTreeClassifier(),
            RandomForestClassifier(n_estimators=10)]
                
            for classifier_choice in classifiers:
                #print classifier_choice
                classifier = train_model(train, train_target, classifier_choice)
                accuracy = test_model(classifier, test, test_target)
            percentage += 0.05

def specific(master_data, master_years):
    data, years = shift(6, master_data, master_years)
    train, train_target, test, test_target = sample_cut(years, data, 0.75, True, 1)
    classifier_choice = linear_model.SGDClassifier()
    classifier = train_model(train, train_target, classifier_choice)
    accuracy = test_model(classifier, test, test_target)
    
def specific2(master_data, master_years):
    data, years = shift(6, master_data, master_years)
    train, train_target, test, test_target = sample_cut(years, data, 0.5, True, 1)
    classifier_choice = linear_model.Perceptron(penalty='l1')
    classifier = train_model(train, train_target, classifier_choice)
    accuracy = test_model(classifier, test, test_target)

master_years = get_volcano_years()
master_data = import_data()
#specific(master_data, master_years)
#specific2(master_data, master_years)
spray_n_pray(master_data, master_years)