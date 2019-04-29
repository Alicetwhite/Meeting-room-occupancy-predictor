#This script will format the X and Y lists to contain only certain features

import json
import datetime

X = []
Y = []

#Load X and Y in
with open("../XandY/raw_X.json") as f:
    X = json.load(f)
    

with open("../XandY/raw_Y.json") as f:
    Y = json.load(f)

#------ Functions to customise X array depending on what features are wanted---------

#Function to restrict the times to between 7am-8pm (hours where rooms are occupied) and only weekdays
def condense_time(condense):

    if(condense == False):

        #Remove timestamps from y array
        for i in range(len(X)):
            del Y[i][0]

        #Remove timestamps, day and time from X array
        for i in range(len(X)):
            for j in range(3):
                del X[i][0]         

    #Remove all time stamps between 8.15pm-6.45am and Saturday and Sunday
    else:
        i = 0
        while i < len(X):
            timestamp = datetime.datetime.strptime(X[i][0], "%Y-%m-%dT%H:%M:%S") #Convert string to datetime object
            hour = timestamp.hour
            day = X[i][1]

            #If timestamps are before 7 am or after 8pm, or a saturday or sunday -  delete them from X list
            if(hour<7 or hour > 19 or day == 5 or day == 6):
                del X[i]
                del Y[i]
            else:
                i = i + 1

        condense_time(False) #Delete irrelavnt info from X and Y lists

#Just time
def make_just_time_lists():

    condense_time(condense_time_bool)

    #Remove everything from X list except time
    for i in range(len(X)):
        for j in range(15):
            del X[i][2]

    # Write X
    with open("../XandY/just_time_X.json", 'w') as outfile:
        json.dump(X,outfile) 

    # Write Y
    with open("../XandY/just_time_Y.json", 'w') as outfile:
        json.dump(Y,outfile) 

#Time and day
def make_time_day_lists():

    condense_time(condense_time_bool)

    #Remove meeting room bookings and semesters from X array
    for i in range(len(X)):
        for j in range(13):
            del X[i][4]

    # Write X
    with open("../XandY/time_day_X.json", 'w') as outfile:
        json.dump(X,outfile) 

    # Write Y
    with open("../XandY/time_day_Y.json", 'w') as outfile:
        json.dump(Y,outfile) 


#Time, day, stages
def make_time_day_stages_lists():

    condense_time(condense_time_bool)

    #Remove meeting room bookings from X array 
    for i in range(len(X)):     
        for j in range(10):
            del X[i][7]

    # Write X
    with open("../XandY/stages_X.json", 'w') as outfile:
        json.dump(X,outfile) 

    # Write Y
    with open("../XandY/stages_Y.json", 'w') as outfile:
        json.dump(Y,outfile) 

#Time, day, bookings
def make_time_day_bookings_lists():

    condense_time(condense_time_bool)

    #Remove stages from X
    for i in range(len(X)):      
        for k in range(3):
            del X[i][4]

    # Write X
    with open("../XandY/bookings_X.json", 'w') as outfile:
        json.dump(X,outfile) 

    # Write Y
    with open("../XandY/bookings_Y.json", 'w') as outfile:
        json.dump(Y,outfile) 

#Time, day, semesters, bookings
def make_time_day_stages_bookings_lists():

    condense_time(condense_time_bool)

    # Write X
    with open("../XandY/stages_bookings_X.json", 'w') as outfile:
        json.dump(X,outfile) 

    # Write Y
    with open("../XandY/stages_bookings_Y.json", 'w') as outfile:
        json.dump(Y,outfile) 

#Bookings
def make_just_bookings_lists():

    condense_time(condense_time_bool)

    #Remove time, day and stages from X
    for i in range(len(X)):      
        for k in range(7):
            del X[i][0]

    # Write X
    with open("../XandY/just_bookings_X.json", 'w') as outfile:
        json.dump(X,outfile) 

    # Write Y
    with open("../XandY/just_bookings_Y.json", 'w') as outfile:
        json.dump(Y,outfile)

#Stages
def make_just_timetable_lists():

    condense_time(condense_time_bool)

    #Remove meeting room bookings from X array
    for i in range(len(X)):     
        for j in range(10):
            del X[i][7]
    
    #Remove time and day from X array
    for i in range(len(X)):      
        for k in range(4):
            del X[i][0]

    # Write X
    with open("../XandY/just_timetable_X.json", 'w') as outfile:
        json.dump(X,outfile) 

    # Write Y
    with open("../XandY/just_timetable_Y.json", 'w') as outfile:
        json.dump(Y,outfile)  

#Day
def make_just_day_lists():

    condense_time(condense_time_bool)

    #Remove meeting room bookings and stages from X array
    for i in range(len(X)):     
        for j in range(10):
            del X[i][4]
    
    #Remove time from X array
    for i in range(len(X)):      
        for k in range(2):
            del X[i][0]

    # Write X
    with open("../XandY/just_day_X.json", 'w') as outfile:
        json.dump(X,outfile) 

    # Write Y
    with open("../XandY/just_day_Y.json", 'w') as outfile:
        json.dump(Y,outfile) 

condense_time_bool = False #Set whether to condense the times or not

make_time_day_stages_bookings_lists()

