#This script will create confusion matrix's for the actual data and predicted data

#-------------------Imports---------------------

import json
from datetime import time, tzinfo, timedelta
import time
from dateutil.parser import parse
import datetime
import numpy as np
import requests
import dateutil.parser
import dateutil.tz
from sklearn import neural_network
from sklearn.model_selection import train_test_split

rooms = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
X = []
y = []
booked_occupied = 0
booked_not_occupied = 0
not_booked_occupied = 0
not_booked_not_occupied = 0

#Set X list to content in json
with open('../XandY/just_time_X.json') as f:
    X = json.load(f)

#Set y list to content in json
with open('../XandY/just_time_Y.json') as f:
    y = json.load(f)


#----------- All rooms --------------

#For every timestep calculate variables
for j in range(len(X)):
    i=7
    #Loop through each room at current timestep
    while (i<len(X[j])):

        if(X[j][i] == 1):

            #If booked see if occupied
            if(y[j][i-7]==0):
                booked_not_occupied = booked_not_occupied +1
            else:
                booked_occupied = booked_occupied +1

        #If not booked see if occupied
        else:
            if(y[j][i-7]==0):
                not_booked_not_occupied = not_booked_not_occupied + 1
            else:
                not_booked_occupied = not_booked_occupied +1

        i = i+1

print(booked_occupied)
print(booked_not_occupied)

print(not_booked_occupied)
print(not_booked_not_occupied)

#Model
nn = neural_network.MLPClassifier((18, 18, 18, 18), activation='relu') #Creates neural network
xTrain, xTest, yTrain, yTest = train_test_split(X,y,test_size=0.5,shuffle=True) #Splits into training and test data
nn.fit(xTrain,yTrain)

#---------Calculate confusion matrix of model--------
y_true = yTest
y_pred = nn.predict(xTest)
y_predicted = [] #List to store predicted values

#Ensure each element is a list not a numpy array
for i in range(len(list(y_pred))):
    new = list(y_pred[i])
    y_predicted.append(new)

predicted_occupied_actual_occupied = 0
predicted_occupied_actual_unoccupied = 0
predicted_unoccupied_actual_occupied = 0
predicted_unoccupied_actual_unoccupied = 0


for i in range(len(y_predicted)):
    for j in range(len(y_predicted[0])):
        #If predicted and occupied
        if(y_predicted[i][j] == y_true[i][j] and y_predicted[i][j] == 1):
            predicted_occupied_actual_occupied += 1
        #If predicted and not occupied
        elif (y_predicted[i][j] != y_true[i][j] and y_predicted[i][j] == 1):
            predicted_occupied_actual_unoccupied += 1
        #If not predicted and occupied
        if(y_predicted[i][j] != y_true[i][j] and y_predicted[i][j] == 0):
            predicted_unoccupied_actual_occupied += 1
        #If not predicted and not occupied
        elif (y_predicted[i][j] == y_true[i][j] and y_predicted[i][j] == 0):
            predicted_unoccupied_actual_unoccupied += 1

print("Model:")
print('Predicted occupied actual occupied: ' , predicted_occupied_actual_occupied)
print('Predicted occupied actual unoccupied: ',predicted_occupied_actual_unoccupied)
print("Predicted unoccupied actual occupied: ", predicted_unoccupied_actual_occupied)
print("Predicted unoccupied actual unoccupied: ", predicted_unoccupied_actual_unoccupied)


#---------Calculate confusion matrix of model for each room--------


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


#Reset
predicted_occupied_actual_occupied = 0
predicted_occupied_actual_unoccupied = 0
predicted_unoccupied_actual_occupied = 0
predicted_unoccupied_actual_unoccupied = 0

rooms = ['1.025', '1.025A', '1.025B', '1.043', '2.060', '3.032', '4.036', '4.053', '5.009', '6.011']

#Train model
nn = neural_network.MLPClassifier((18, 18, 18, 18), activation='relu') #Creates neural network
xTrain, xTest, yTrain, yTest = train_test_split(X,y,test_size=0.5,shuffle=True) #Splits into training and test data
nn.fit(xTrain,yTrain)

y_true = yTest
y_pred = nn.predict(xTest)
y_predicted = [] #List to store predicted values

#Ensure each element is a list not a numpy array
for i in range(len(list(y_pred))):
    new = list(y_pred[i])
    y_predicted.append(new)


#----------- Individual rooms --------------

#For every room calculate the confusion matrix
for room_index in range(len(rooms)):
    room = rooms[room_index] #Corresponding room

    predicted_occupied_accuracies = []
    predicted_unoccupied_accuracies = []

    for run in range(10):

        for i in range(len(y_predicted)):
            predicted = y_predicted[i][room_index] #Stores predicted occupancy of room for current timestep
            actual = y_true[i][room_index] #Stores actual occupancy of room for current timestep

            #Update correct variable
            if(predicted == actual and predicted == 1):
                predicted_occupied_actual_occupied +=1
            elif(predicted != actual and predicted == 1):
                predicted_occupied_actual_unoccupied +=1
            elif(predicted == actual and predicted ==0):
                predicted_unoccupied_actual_unoccupied +=1
            elif(predicted != actual and predicted ==0):
                predicted_unoccupied_actual_occupied +=1
        
        
        accuracy_occupied = (predicted_occupied_actual_occupied / (predicted_occupied_actual_occupied + predicted_unoccupied_actual_occupied))*100
        accuracy_unoccupied = (predicted_unoccupied_actual_occupied / (predicted_unoccupied_actual_occupied + predicted_unoccupied_actual_unoccupied))*100
        predicted_occupied_accuracies.append(accuracy_occupied)
        predicted_unoccupied_accuracies.append(accuracy_unoccupied)

        #Reset
        predicted_occupied_actual_occupied = 0
        predicted_occupied_actual_unoccupied = 0
        predicted_unoccupied_actual_occupied = 0
        predicted_unoccupied_actual_unoccupied = 0

    # print(room)
    # print("Predicted occupied mean accuracy: ", mean(predicted_occupied_accuracies))
    # print("Predicted occupied variance: ", np.var(predicted_occupied_accuracies))
    # print("Predicted not occupied mean accuracy: ", mean(predicted_unoccupied_accuracies))
    # print("Predicted not occupied variance: ", np.var(predicted_unoccupied_accuracies))