# This script will format the X and Y lists
# X list: [sin time, cos time, sin day, cos day, stage 1, stage 2, stage 3, room 1, room 2, room 3, room 4, room 5, room 6, room 7, room 8, room 9, room 10]
# Y list: [room 1 occupied?, room 2 occupied?, room 3 occupied?, room 4 occupied?, room 5 occupied?, room 6 occupied?, room 7 occupied?, room 8 occupied?, room 9 occupied?, room 10 occupied?]

#-------------------Imports---------------------

import json
from datetime import time, tzinfo, timedelta
import time
from time import mktime
from dateutil.parser import parse
import datetime
import numpy as np
import pandas as pd
import requests
import dateutil.parser
import dateutil.tz

#----------------Global variables---------------

start_date = "10/09/2018"
end_date = "10/03/2019"
date = "Not yet set"
rooms = [] #Stores unique meeting rooms
interval_mins = 15 #Interval between times in X matrix
intervals_in_day = int(((24*60)/interval_mins))
seconds_in_day = 24*60*60 

#--------------Helper functions---------------

#Function to flip a bit
def flip_bit(value):
    if(value==1):
        return 0
    else:
        return 1

#-------Find unique number of rooms and add to rooms array------
with open("../jsons/final_room_bookings.json") as bookings:
    
    content = json.load(bookings)

    date = parse(start_date, dayfirst = True)
    
    i = 0

    split = [] #Array to store individual meeting rooms

    for j in range(len(content)):

        #If more than one room split into each room
        if(',' in content[j]['Locations']):
            split = content[j]['Locations'].split(",")    
        else:
            split = [content[j]['Locations']]

        # Add each unique room to rooms array
        for k in range(len(split)):
            if((split[k].split(' ')[0])[4:] not in rooms):
                rooms.append((split[k].split(' ')[0])[4:])
        
        split = []
            
rooms.sort()

#Delete 2.022 and 4.005 from rooms list as their bookings are after March
i = 0
while (i < len(rooms)):
    if(rooms[i] == '2' or rooms[i] == '4'):
        del(rooms[i])
    i = i+1

# Number of days between start and end date
date_difference = (parse(end_date, dayfirst = True)-parse(start_date, dayfirst = True)).days
no_samples = (date_difference+1)*intervals_in_day 

#Initialise 2d X array for x and y
X = [[0 for x in range(len(rooms)+10)] for y in range(no_samples)]
Y = [[0 for x in range(len(rooms)+1)] for y in range(no_samples)]

#Set time for first array
X[0][2] = "00:00" 
X[0][3] = np.sin(2*np.pi*0/seconds_in_day)
X[0][4] = np.cos(2*np.pi*0/seconds_in_day)

#--------------Populate X array with correct time---------------

current_time = time.strptime("00:00", "%H:%M")

for i in range(no_samples-1):

    #Increment time by specified interval
    updated_min = current_time.tm_min + interval_mins      
    updated_hour = current_time.tm_hour
    # Increment hour if needed
    if(updated_min >= 60):
        #If it is a new day reset to 00:00
        if(updated_hour >= 23):
            updated_hour = 00
            updated_min = 00
        else:
            updated_hour = current_time.tm_hour + 1
            updated_min = updated_min - 60
    
    #Update time
    current_time = time.strptime(str(updated_hour)+":"+str(updated_min), "%H:%M")
    time_str = time.strftime("%H:%M", current_time)
    
    X[i+1][2] = time_str

    #-------Calculate sin and cos time------

    time_in_secs = updated_hour*3600 + updated_min*60 #Time in seconds since midnight
    sin_time = np.sin(2*np.pi*time_in_secs/seconds_in_day) #Time in sin
    cos_time = np.cos(2*np.pi*time_in_secs/seconds_in_day) #Time in cos

    #Update features in X
    X[i+1][3] = sin_time
    X[i+1][4] = cos_time

#-------Populate X array with correct date and day------
for i in range(date_difference + 1):

    #Get day of current date
    day_num = date.weekday() # Parse date string to a date and get corresponding weekday as a number
    print(day_num)

    #-------Calculate sin and cos day------
    sin_day = np.sin((day_num/7 * (2*np.pi))) #Day in sin equivalent
    cos_day = np.cos((day_num/7 * (2*np.pi))) #Day in cos equivalent

    for j in range(intervals_in_day*i, (intervals_in_day*i)+intervals_in_day):
        X[j][0] = date.strftime("%d/%m/%Y")
        X[j][1] = day_num
        X[j][5] = sin_day
        X[j][6] = cos_day
        
    date += datetime.timedelta(days=1)

#Reset date
date = parse(start_date, dayfirst = True)


#-------Populate X array with correct bookings------
with open("../jsons/final_room_bookings.json") as bookings:
    content = json.load(bookings)

    for i in range(date_difference+1):
        filtered = list(filter(lambda booking: booking['Scheduled Start Date'] == date.strftime("%d/%m/%Y"), content)) #Returns bookings just on specified date
        
        #Check if there is a booking at each time interval in a day
        for j in range(intervals_in_day*i, (intervals_in_day*i)+intervals_in_day):
            time = X[j][2]
            for k in range(len(filtered)):
                if( time >= filtered[k]['Start time'] and time < filtered[k]['End time']):
                    room = filtered[k]['Locations']
                    
                    #Split each room up into an array (handles multiple roooms)
                    if(',' in room):
                        split = room.split(",")    
                    else:
                        split = [room]

                    # Shorten string to room recognised by API
                    for x in range(len(split)):
                        if(split[x] not in rooms):
                            split[x] = (split[x].split(' ')[0][4:])

                    # Add a 1 to indicate booking at correct index in X
                    for k in range(len(split)):
                        index = rooms.index(split[k])
                        X[j][index+10] = 1 #Creates 7 slots before for sin and cos time and day, and timetable *3

                split = [] #Reset

            #-------Update datetime object to include time and be in iso format------
                
            # Get current hour and minute
            hour = int(time[:2])
            minute = int(time[3:])

            #Update date with correct time
            date = date.replace(hour=hour,minute=minute)
            

            X[j][0] = date.isoformat() #Update date to be in iso format
            # del X[j][2] # Delete time in list
            # del X[j][1] # Delete day in list
                
        date += datetime.timedelta(days=1)

#-------------------Filter X array to term/ holiday dates---------------

#Index's of start and end dates for term and holiday
semester_one_start = 0
semester_one_end = (96*7*14)+(96*3)+95
semester_two_start = (96*7*21)-96
semester_two_end = len(X)-1
christmas_start = (96*7*14)+(96*3)+96
christmas_end = (96*7*17)+95
exam_start = (96*7*17)+96
exam_end = (96*7*21)-97

#Function to filter X to between a start and end date
def make_X(start, end):

    new_X = []

    for i in range(start, end+1):
        new_X.append(X[i])
    
    return new_X

#Index in X where want to start and end
start_date_index = semester_one_start
end_date_index = semester_two_end

#Set start date and end date of X to strings
start_date = X[start_date_index][0][:10]
end_date = X[end_date_index][0][:10]
start_date = start_date[8:10] + "/" + start_date[5:7] + "/" + start_date[:4] #Format string to be recognised by no_samples code
end_date = end_date[8:10] + "/" + end_date[5:7] + "/" + end_date[:4] #Format string to be recognised by no_samples code

#Make X
X = make_X(start_date_index, end_date_index) 

# Set no_samples to correct size
date_difference = (parse(end_date, dayfirst = True)-parse(start_date, dayfirst = True)).days
no_samples = (date_difference+1)*intervals_in_day 

#--------------Return a dictionary of timestamp lecture pairs for specific stage-------------
def create_map_lecture(stage):

    #Create hashmap for current stage
    map = [[0 for x in range(2)] for y in range(no_samples)]

    #Populate map with correct timestamp
    for i in range(len(X)):
        map[i][0] = datetime.datetime.strptime(X[i][0], "%Y-%m-%dT%H:%M:%S")
    
    #Populate map with whether a lecture is on or not
    with open('../jsons/final_timetable.json') as f:
        content = json.load(f)
        filtered = list(filter(lambda lecture: lecture['Stage'] == stage, content)) #Returns all lectures for a specific stage

        for i in range(len(filtered)):
            current = filtered[i] #Current lecture
            timetable_date = datetime.datetime.strptime(current['Date'], "%Y-%m-%d %H:%M:%S") #Convert date to datetime object for comaprison

            #Look for the equivilant date time in map and set it to 1
            for j in range(len(map)):
                if (map[j][0] == timetable_date ):
                    map[j][1] = 1
    
    dictionary = {str(m[0]): m[1] for m in map} #Create a dictionary from the map
        
    # with open("test_map.txt", 'w') as outfile:
    #     outfile.write(str(map))
    
    return dictionary

#------------Populate X list with whether or not there is a lecture on------------

#Create maps for the different stages
stage_1 = create_map_lecture(1)
stage_2 = create_map_lecture(2)
stage_3 = create_map_lecture(3)

#Insert into X whether or not there is a lecture for each year group
for i in range(len(X)):
    X_date_time = X[i][0].replace('T',' ') #Ensures formatting is the same so can compare
    X[i][7] = stage_1[X_date_time] 
    X[i][8] = stage_2[X_date_time]
    X[i][9] = stage_3[X_date_time]

#--------------Return a dictionary of timestamp occupancy pairs for specific room-------------
def create_map(room):

    room = str(room)

    #Create hashmap for current room
    map = [[0 for x in range(2)] for y in range(no_samples)]
    for i in range(len(X)):
        map[i][0] = datetime.datetime.strptime(X[i][0], "%Y-%m-%dT%H:%M:%S")

    with open('../occupancy_sensors/' + room + '.json') as f:
        content = json.load(f)
        data = content['historic']['values']

        date = datetime.datetime.strptime("2000-01-01", "%Y-%m-%d")
        wanted_date = datetime.datetime.strptime("2018-09-04", "%Y-%m-%d")

        i=len(data) -1 #Index of last element in historic data

        #Loop through json until find index of 04/09/18 (start date)
        while(date < wanted_date):

            date_time = data[i]['time']     
            date_str = date_time[:10]
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d")

            i= i -1

        i = i+1 # Reset i which was deduced by 1 before while loop caught condition

        #Loop through dates we care about and set occupancy in hashmap for corresponding time
        while(i>=0):
            #Previous date time (occupancy detected before)
            previous_date_time = data[i+1]['time']
            p_date_str = previous_date_time[:19]
            p_date_str = p_date_str.replace('T', '')
            p_date_time = datetime.datetime.strptime(p_date_str, "%Y-%m-%d%H:%M:%S")

            #Current date time (occupancy detected now)
            date_time = data[i]['time']
            date_str = date_time[:19]
            date_str = date_str.replace('T', '')
            date_time = datetime.datetime.strptime(date_str, "%Y-%m-%d%H:%M:%S")
            occupancy = data[i]['value']
            occupancy = flip_bit(occupancy) #Occupancy before current sensor change

            ##Populate hashmap with corresponding occupancy

            for j in range(len(map)):
                
                # Populate hashmap with occupancy for times between previous datetime and current
                if (map[j][0] <= date_time and map[j][0] > p_date_time ):
                    map[j][1] = occupancy
            
            i=i-1

        dictionary = {m[0]: m[1:] for m in map} #Create a dictionary from the map
        
    return dictionary


#--------------Create dictionary mapping rooms to dictionary of timestamp to occupancy-------------

dictionary = {} # Stores key value pairs mapping room to dictionary of timestamp to occupancy 

#Populate dictionary
for room in rooms:
    room = room.replace('.','') #Format room so it is recognised by create_map function
    print(room)
    dictionary[room] = create_map(room) #Set room to key and dictionary returned from create_map to value

#Populate y array with correct timestamps
for i in range(len(X)):
    Y[i][0] = X[i][0]

#------------------------Fill y array with occupancy of each room at each timestamp------------------------
for i in range(len(X)):
    date_time = Y[i][0] #Datetime of current entry in x
    date_time = datetime.datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S") #Converted to datetime object
    for j in range(len(rooms)):

        occupied = dictionary[rooms[j].replace('.','')][date_time][0] #Query hashmap for occupancy of room at given datetime
        Y[i][j+1] = occupied #Fill y array with occupancy of correct room

# Write X to file
with open("../XandY/raw_X.json", 'w') as outfile:
    json.dump(X,outfile) 

# Write Y to file
with open("../XandY/raw_Y.json", 'w') as outfile:
    json.dump(Y,outfile)

