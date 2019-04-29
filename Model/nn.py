#This script creates a decision tree model, dumps it to a pkl object file, and and obtains its accuracy

from sklearn import neural_network
from sklearn.model_selection import train_test_split, cross_val_score, TimeSeriesSplit, cross_validate
from sklearn.feature_selection import VarianceThreshold
from sklearn.metrics import confusion_matrix
import json
import pickle
import numpy as np
from numpy import array
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import metrics as ms
from datetime import time, tzinfo, timedelta
import time
from dateutil.parser import parse
import datetime

#27 weeks in X

X = []
y = []

#Change file type depending on what features you want to train model on
with open("../XandY/stages_bookings_X.json") as f:
    content = json.load(f)
    X = content

with open("../XandY/stages_bookings_Y.json") as f:
    content = json.load(f)
    y = content

def random_split():
    
    #Train model
    nn = neural_network.MLPClassifier((18,18,18,18), activation='relu') #Creates neural network
    xTrain, xTest, yTrain, yTest = train_test_split(X,y,test_size=0.5,shuffle=True) #Splits into training and test data
    nn.fit(xTrain,yTrain)

    #---------Calculate accuracy of model--------
    predictions = nn.predict(xTest)
    all_elements = len(predictions)*len(predictions[0]) #All elements in predictions
    score = 0

    #If a the prediction matches ground truth add 1 to the score
    for i in range(len(predictions)):
        prediction = predictions[i]
        truth = yTest[i]
        for j in range(len(prediction)):
            if prediction[j] == truth[j]:
                score += 1
    
    # Save model to file
    with open("../Model/nn.pkl", "wb") as f:
        pickle.dump(nn, f)

    return (score/all_elements)*100



def timeseries_split():

    all_scores = {'Train average accuracy' : 'Undefined', 'Train error rate': 'Undefined', 'Test average accuracy' : 'Undefined', 'Test error rate':'Undefined'}

    scores = []

    tscv = TimeSeriesSplit(n_splits=26)

    train_score = 0
    test_score = 0 
    occupied_accuracy = 0
    no_occupied_ground_truths = 0
    unoccupied_accuracy = 0
    no_unoccupied_ground_truths = 0

    counter = 1
    all_elements = 0

    for train_index, test_index in tscv.split(X):

        print(counter)
        counter= counter+1

        X_train = []
        X_test = []
        y_train = []
        y_test = []

        train_index = list(train_index)
        test_index = list(test_index)

        for j in range(len(train_index)):
            X_train.append(X[j])
            y_train.append(y[j])
        for j in range(len(test_index)):
            X_test.append(X[j])
            y_test.append(y[j])
        
        nn = neural_network.MLPClassifier((18, 18, 18, 18), activation='relu') #Creates neural network
        nn.fit(X_train,y_train)
        predictions_train = nn.predict(X_train)
        all_elements_train = len(predictions_train)*len(predictions_train[0])
        predictions_test = nn.predict(X_test)
        all_elements_test = len(predictions_test)*len(predictions_test[0]) #All elements in predictions
        
        #If a the prediction matches ground truth add 1 to the score
        for i in range(len(predictions_train)):
            prediction = predictions_train[i]
            truth = y_train[i]
            for j in range(len(prediction)):
                if prediction[j] == truth[j]:
                    train_score += 1
    

        #If a the prediction matches ground truth add 1 to the score
        for i in range(len(predictions_test)):
            prediction = predictions_test[i]
            truth = y_test[i]
            for j in range(len(prediction)):
    
                #Add to number of ground truths
                if(truth[j] == 1):
                    no_occupied_ground_truths +=1
                elif(truth[j] == 0):
                    no_unoccupied_ground_truths +=1

                #Add to score
                if prediction[j] == truth[j]:
                    test_score += 1
                    #Add to occupied accuracy
                    if(truth[j] == 1):
                        occupied_accuracy += 1
                    #Add to unoccupied accuracy
                    if(truth[j] == 0):
                        unoccupied_accuracy += 1
    
    # Save model to file
    with open("../Model/nn.pkl", "wb") as f:
        pickle.dump(nn, f)

    all_scores['Test average accuracy'] = ((test_score/26)/all_elements_test)*100
    all_scores['Train average accuracy'] = ((train_score/26)/all_elements_train)*100
    all_scores['Test error rate'] = 100-(((test_score/26)/all_elements_test)*100)
    all_scores['Train error rate'] = 100- (((train_score/26)/all_elements_train)*100)

    occupied_score = (occupied_accuracy/no_occupied_ground_truths)*100
    unoccupied_score = (unoccupied_accuracy/no_unoccupied_ground_truths)*100

    return unoccupied_score
 
print(timeseries_split())