#This script will create various graphs of the actual occupancy and predicted occupancy

import json
import matplotlib.pyplot as plt
import time
import pandas as pd
import joypy
import pickle
import numpy as np
from sklearn import neural_network
from sklearn.model_selection import train_test_split
from matplotlib import cm
from dateutil.parser import parse
import pickle

X = []
y = []
rooms = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
start_date = "10/09/2018"
start_time = "00:00"
end_date = "10/03/2019"
end_time = "23:45"
include_weekend = True
week_start_date = "10/09/2018"
week_end_date = "16/09/2018"
graph_hour_interval = 2

#Change file type depending on what features you want to visualise - also change features on line 130 to correspond to file, and train model with right data
with open("../XandY/stages_bookings_X.json") as f:
        content = json.load(f)
        X = content

with open("../XandY/stages_bookings_Y.json") as f:
    content = json.load(f)
    y = content

# generate timesteps between start and end time
def gen_times(startTime, edfnimeStep, interval_mins):
    times = []
    current_time = time.strptime(startTime, "%H:%M")
    time_str = time.strftime("%H:%M", current_time)
    times.append(time_str)

    #Work out number of minutes between start time and end time
    start_hour = startTime.split(":")[0]
    start_minutes = startTime.split(":")[1]
    start_minutes_from_midnight = (int(start_hour)*60)+(int(start_minutes))

    end_hour = edfnimeStep.split(':')[0]
    end_minutes = edfnimeStep.split(':')[1]
    end_minutes_from_midnight = (int(end_hour)*60)+int(end_minutes)+15

    minutes_between_timesteps = end_minutes_from_midnight - start_minutes_from_midnight

    #Work out the number of intervals between start time and end time
    no_intervals = int(((minutes_between_timesteps)/interval_mins) - 1)

    for i in range(no_intervals):
        #Increment time by specified interval
        updated_min = current_time.tm_min + interval_mins      
        updated_hour = current_time.tm_hour
        # Increment hour if needed
        if(updated_min >= 60):
            updated_hour = current_time.tm_hour + 1
            updated_min = updated_min - 60
        current_time = time.strptime(str(updated_hour)+":"+str(updated_min), "%H:%M")
        time_str = time.strftime("%H:%M", current_time)
        times.append(time_str)
    return times

#Create list of times between start date and end date
def gen_times_between_dates(start_date, start_time, end_date, end_time_step, interval_mins, include_weekend):

    times = [] #List to store times between start date and end date

    # Number of days between start and end date
    date_difference = (parse(end_date, dayfirst = True)-parse(start_date, dayfirst = True)).days+1

    #Populate times list with times between start date and end date
    for i in range(date_difference):
        times_list = gen_times(start_time, end_time,interval_mins)
        for j in times_list:
            times.append(j)

    #Delete weekends if neccessary
    if(include_weekend == False):

        #Work out index of first time on Saturday
        no_timesteps_in_day = int(len(times))/7
        index_first_time_saturday = int(no_timesteps_in_day*5)

        i = index_first_time_saturday

        #delete times at wekeend
        while i < len(times):
            del times[i]

    return times

#Convert sin and cos time to hour and minute
def convert_to_real_time(sin_time, cos_time):
    seconds_in_day = 24*60*60

    #If sin is negative return second value in cos wave
    if(sin_time < 0):
        time_in_mins = (24*60)-(((np.arccos(cos_time))/(2*np.pi))*(seconds_in_day))/60# Convert sin time to time in minutes
    else:
        time_in_mins = (((np.arccos(cos_time))/(2*np.pi))*(seconds_in_day))/60 # Convert cos time to time in minutes

    time_in_mins = str(time_in_mins).split('.')[0] #Turns time_in_mins into a string from a float 
    
    time = int(time_in_mins)/60 #Get time as hour.percentageMinute
    hour = str(time).split('.')[0] #Get hour
    minute = int(60*((int(str(time).split('.')[1]))/100)) #Get minute
    
    #Adjusts minutes and hour to be correct as calculation above doesn't work for the below cases
    if(minute == 3):
        minute = minute*10
    elif(minute == 5900000000000000 or minute == 589999999999999 or minute == 590000000000000):
        minute = 0
        hour = int(hour)+1
    elif(minute == 139999999999999 or minute == 140000000000000):
        minute = 15
    elif(minute == 289999999999999 or minute == 290000000000000):
        minute = 30
    elif(minute == 439999999999999 or minute == 440000000000000):
        minute = 45
    
    time = []
    time.append(hour)
    time.append(minute)

    return time

# Create a list of the number of rooms which are predicted to be occupied at each time for a specified week
def gen_aggregated_predicted_occupancy(week_no, no_times_in_week):

    first_index = (week_no-1)*no_times_in_week #Index of 07:00 for Monday of week
    last_index =  ((week_no)*no_times_in_week) #Index of 19:45 for Sunday of week

    with open("../Model/df.pkl", 'rb') as f:
        df = pickle.load(f)

    predicted_occupancy = [] #Create list to store predicted values

    #Change features depending on file type and what you want to predict
    #Fill predicted list with predicted values
    for i in range(first_index, last_index):
        sin_time = X[i][0]
        cos_time = X[i][1]
        sin_day = X[i][2]
        cos_day = X[i][3]
        stage_1 = X[i][4]
        stage_2 = X[i][5]
        stage_3 = X[i][6]
        room_1 = X[i][7]
        room_2 = X[i][8]
        room_3 = X[i][9]
        room_4 = X[i][10]
        room_5 = X[i][11]
        room_6 = X[i][12]
        room_7 = X[i][13]
        room_8 = X[i][14]
        room_9 = X[i][15]
        room_10 = X[i][16]

        #, sin_day, cos_day,stage_1, stage_2, stage_3,room_1, room_2, room_3 , room_4, room_5, room_6 , room_7, room_8, room_9, room_10
        predicted = df.predict([[sin_time, cos_time, sin_day, cos_day,stage_1, stage_2, stage_3,room_1, room_2, room_3 , room_4, room_5, room_6 , room_7, room_8, room_9, room_10]]) 
        predicted = list(list(predicted)[0]) #Convert into a list

        predicted_occupancy.append(list(predicted))

    aggregated_predicted_occupancy = [] #List to store number of occupied rooms at each time step

    # Find number of occupied rooms at each timestep for specified week and add to aggregated_occupancy list
    for i in range(len(predicted_occupancy)):
        no_rooms_occupied = 0
        for j in range(len(y[0])):
            if(predicted_occupancy[i][j]==1):
                no_rooms_occupied +=1
        aggregated_predicted_occupancy.append(no_rooms_occupied)
    
    return aggregated_predicted_occupancy

#Create a list of actual aggregated occupancies for each time for specified week
def gen_aggregated_occupancy(week_no, no_times_in_week):

    first_index = (week_no-1)*no_times_in_week #Index of 00:00 for Monday of week
    last_index =  (week_no)*no_times_in_week #Index of 23:45 for Sunday of week

    aggregated_occupancy = [] #List to store number of occupied rooms at each time step

    #Find number of occupied rooms at each timestep for specified week and add to aggregated_occupancy list
    for i in range(first_index,last_index):
        no_rooms_occupied = 0
        for j in range(len(y[0])):
            if(y[i][j]==1):
                no_rooms_occupied +=1
        aggregated_occupancy.append(no_rooms_occupied)

    return aggregated_occupancy

#Creates a dataframe of columns containing aggregated number of predicted rooms predocted occupied vs rows of timesteps
def create_predicted_df():
    
    #Create list of all times in a week
    times = gen_times_between_dates(week_start_date,start_time,week_end_date,end_time, 15, include_weekend)
    no_times_in_week = len(times)

    #Create dictionary mapping week number to aggregated predicted occupancy
    map = {}

    for week_no in range(1,27):
        print(week_no)
        map['Week ' + str(week_no)] = gen_aggregated_predicted_occupancy(week_no, no_times_in_week) 
    
    df = pd.DataFrame(map,times) #Create pandas dataframe 

    return df

#Creates a dataframe of columns containing aggregated number of rooms occupied vs rows of timesteps
def create_actual_df():

    #Create lists of sin times in X and cos times in X
    sin_time = []
    cos_time = []
    for i in range(len(X)):
        sin_time.append(X[i][0])
        cos_time.append(X[i][1])
    
    #Create list of all times in a week
    times = gen_times_between_dates(week_start_date,start_time,week_end_date,end_time, 15, include_weekend)
    no_times_in_week = len(times)

    #Create dictionary mapping week number to aggregated occupancy
    dict = {}
    for week_no in range(1,27):
        print(week_no)
        dict['Week ' + str(week_no)] = gen_aggregated_occupancy(week_no, no_times_in_week)

    df = pd.DataFrame(dict,times) #Create pandas dataframe 

    return df

#-----------------Plot number of rooms occupied vs time --------------------

#A function to plot predicted number of occupied rooms for each time in a week
def predicted_agg_occupancy_vs_time():

    df = create_predicted_df()

    #Plot graph
    df = df.agg("mean",axis="columns")
    ax = df.plot(kind="area", color= "#FF7F0E")

    #Plot x axis ticks
    times = gen_times_between_dates(week_start_date, start_time,week_end_date, end_time, 15, include_weekend)
    no_times_in_week = len(times)

    ticks = []
    xLocations = []
    for i in range(no_times_in_week):
        if i % (graph_hour_interval*12) == 0:
            ticks.append(times[i])
            xLocations.append(i)    

    plt.xticks(xLocations, ticks)

    plt.xticks(rotation = 70)
    plt.grid(axis='x')

    # Set x and y labels
    ax.set_xlabel('Time')
    ax.set_ylabel('Average number of rooms predicted occupied')

    #Set ticks
    yTicks = [1,2,3,4,5,6,7,8,9,10]
    plt.yticks(yTicks)

    plt.show()

#A function to plot actual number of occupied rooms for each time in a week
def actual_agg_occupancy_vs_time():
    
    df = create_actual_df()
    print(df)

    #Create list of all times in a week
    times = gen_times_between_dates(week_start_date,start_time,week_end_date,end_time, 15, include_weekend)

    #Plot graph
    df = df.agg("mean",axis="columns")
    ax = df.plot(kind="area")

    print(df)

    #Plot x axis ticks
    no_times_in_week = len(times)

    ticks = []
    xLocations = []
    for i in range(no_times_in_week):
        if i% (graph_hour_interval*12) == 0:
            ticks.append(times[i])
            xLocations.append(i)    

    plt.xticks(xLocations, ticks)

    plt.xticks(rotation = 70)
    plt.grid(axis='x')

    # Set x and y labels
    ax.set_xlabel('Time')
    ax.set_ylabel('Average number of rooms occupied')

    #Set ticks
    yTicks = [1,2,3,4,5,6,7,8,9,10]
    plt.yticks(yTicks)

    #Set ticks
    yTicks = [1,2,3,4,5,6,7,8,9,10]
    plt.yticks(yTicks)

    plt.show()

#------------Just bookings - number of rooms occupied vs predicted occupied -----------------

#Returns number of rooms booked in a list
def number_rooms_booked(element_list):

    number_rooms_booked  = 0

    for element in element_list:
        if(element == 1):
            number_rooms_booked +=1
    
    return number_rooms_booked


#Generates average number of rooms model will predict to be occupied
def gen_avg_predicted_occupancy(no_rooms_booked):
    
    with open("../Model/df.pkl", 'rb') as f:
        df = pickle.load(f)

    scores = 0
    total = 0

    for i in range(len(X)):
        if(number_rooms_booked(X[i]) == no_rooms_booked):
            predicted_list = df.predict([X[i]])[0]
            
            #Loop through predicted list to calculate how many rooms it predicted to be occupied
            no_predicted_rooms = 0
            for j in range(len(predicted_list)):
                if(predicted_list[j] == 1):
                    no_predicted_rooms += 1

            scores += no_predicted_rooms
            total += 1
    
    return(scores/total)

#Generates average number of rooms actually occupied
def generate_actual_occupancy(no_rooms_booked):

    scores = 0
    total = 0

    for i in range(len(X)):
        if(number_rooms_booked(X[i]) == no_rooms_booked):
            actual_occupied_list = y[i]

            #Loop through actual occupied list to calculate how many rooms are actually occupied
            no_occupied_rooms = 0
            for j in range(len(actual_occupied_list)):
                if(actual_occupied_list[j] == 1):
                    no_occupied_rooms += 1
            
            scores += no_occupied_rooms
            total += 1
    
    return(scores/total)


#A function to plot number of rooms predicted occupied vs average occupancy
def number_rooms_books_vs_predicted_average_occupancy():

    rooms = [1,2,3,4,5,6,7,8,9,10]
    average_no_rooms_predicted_occupied = []
    average_no_rooms_actually_occupied = []

    #Populate list with correct averages for number of rooms occupied for each number of booked rooms
    for room in rooms:
        actual_occupancy = generate_actual_occupancy(room)
        average_no_rooms_actually_occupied.append(actual_occupancy)

    #Populate list with correct predictions for each number of booked rooms
    for room in rooms:
        prediction = gen_avg_predicted_occupancy(room)
        average_no_rooms_predicted_occupied.append(prediction)
    
    #Create dataframe mapping number of booked rooms to predicted average number of rooms occuppied
    df = pd.DataFrame({'Actually occupied' : average_no_rooms_actually_occupied, 'Predicted occupied' : average_no_rooms_predicted_occupied},rooms) #Create pandas dataframe 
    
    #Plot graph
    ax = df.plot(kind='bar')

    # Set x and y labels
    ax.set_xlabel('Number of rooms booked')
    ax.set_ylabel('Average number of rooms occupied')

    #Set ticks
    yTicks = [1,2,3,4,5,6,7,8,9,10]
    plt.yticks(yTicks)

    plt.show()


#------------Just timetable - number of rooms occupied vs predicted occupied -----------------

#Generates average number of rooms actually occupied
def gen_actual_occupancy_stages(stage):

    if(stage == "No lectures"):
        no_stages_have_lectures = True
    else:
        stage_index = stage - 1 #Index of stage in each X element
        no_stages_have_lectures = False

    scores = 0
    total = 0
    if(no_stages_have_lectures == False):
        for i in range(len(X)):
            if((X[i][stage_index]) == 1):

                actual_occupied_list = y[i]

                #Loop through actual occupied list to calculate how many rooms are actually occupied
                no_occupied_rooms = 0
                for j in range(len(actual_occupied_list)):
                    if(actual_occupied_list[j] == 1):
                        no_occupied_rooms += 1
                
                scores += no_occupied_rooms
                total += 1
    #If no stages have any lectures
    else:
        for i in range(len(X)):
            if((X[i][0]) == 0 and (X[i][1]) == 0 and (X[i][2]) == 0):
                actual_occupied_list = y[i]

                #Loop through actual occupied list to calculate how many rooms are actually occupied
                no_occupied_rooms = 0
                for j in range(len(actual_occupied_list)):
                    if(actual_occupied_list[j] == 1):
                        no_occupied_rooms += 1
                
                scores += no_occupied_rooms
                total += 1
    
    return(scores/total)

#Generates average number of rooms predicted occupied
def gen_avg_predicted_occupancy_stages(stage):

    if(stage == "No lectures"):
        no_stages_have_lectures = True
    else:
        stage_index = stage - 1 #Index of stage in each X element
        no_stages_have_lectures = False

    with open("../Model/df.pkl", 'rb') as f:
        df = pickle.load(f)

    scores = 0
    total = 0

    if(no_stages_have_lectures == False):
        for i in range(len(X)):
            if(X[i][stage_index] == 1):

                predicted_list = df.predict([X[i]])[0]
                
                #Loop through predicted list to calculate how many rooms it predicted to be occupied
                no_predicted_rooms = 0
                for j in range(len(predicted_list)):
                    if(predicted_list[j] == 1):
                        no_predicted_rooms += 1

                scores += no_predicted_rooms
                total += 1
    #If no stages have any lectures
    else:
        for i in range(len(X)):
            if((X[i][0]) == 0 and (X[i][1]) == 0 and (X[i][2]) == 0):

                predicted_list = df.predict([X[i]])[0]
                
                #Loop through predicted list to calculate how many rooms it predicted to be occupied
                no_predicted_rooms = 0
                for j in range(len(predicted_list)):
                    if(predicted_list[j] == 1):
                        no_predicted_rooms += 1

                scores += no_predicted_rooms
                total += 1

    
    return(scores/total)

#Function to plot average number of rooms actually and predicted occupied vs whether or not each stage has a lecture/practical on
def timetable_vs_no_rooms_occupied():

    stages = ["No lectures", 1,2,3]
    average_no_rooms_predicted_occupied = []
    average_no_rooms_actually_occupied = []

    #Populate list with correct averages for number of rooms occupied for stage
    for stage in stages:
        actual_occupancy = gen_actual_occupancy_stages(stage)
        average_no_rooms_actually_occupied.append(actual_occupancy)

    #Populate list with correct predictions for each stage 
    for stage in stages:
        prediction = gen_avg_predicted_occupancy_stages(stage)
        average_no_rooms_predicted_occupied.append(prediction)


    #Create df
    df = pd.DataFrame({'Actually occupied' : average_no_rooms_actually_occupied,'Predicted occupied' : average_no_rooms_predicted_occupied}, stages)
  
    #Plot graph
    ax = df.plot(kind='bar')

    # Set x and y labels
    ax.set_xlabel('Stages')
    ax.set_ylabel('Average number of rooms occupied')

    #Set ticks
    yTicks = [1,2,3,4,5,6,7,8,9,10]
    plt.yticks(yTicks)
    plt.xticks(rotation = 0)

    plt.show()

#------------Just day - number of rooms occupied vs predicted occupied -----------------

#Converts a day number to its equivalent sin value
def convert_to_sin_day(day_num):

    day_num = day_num - 1 #Format day num to be correct for equations
    sin_day = np.sin((day_num/7 * (2*np.pi))) #Day in sin equivalent
    return sin_day

#Converts a day number to its equivalent cos value
def convert_to_cos_day(day_num):

    day_num = day_num - 1 #Format day num to be correct for equations
    cos_day = np.cos((day_num/7 * (2*np.pi))) #Day in sin equivalent
    return cos_day

#Returns average number of rooms actually occupied for given day
def gen_avg_actual_occupancy_days(day_num):

    sin_day = convert_to_sin_day(day_num)
    cos_day = convert_to_cos_day(day_num)

    scores = 0
    total = 0

    for i in range(len(X)):
        if(X[i][0] == sin_day and X[i][1] == cos_day):
            actual_occupied_list = y[i]

            #Loop through actual occupied list to calculate how many rooms are actually occupied
            no_occupied_rooms = 0
            for j in range(len(actual_occupied_list)):
                if(actual_occupied_list[j] == 1):
                    no_occupied_rooms += 1
            
            scores += no_occupied_rooms
            total += 1
    
    return(scores/total)

#Generates average number of rooms predicted occupied
def gen_avg_predicted_occupancy_days(day_num):

    with open("../Model/df.pkl", 'rb') as f:
        df = pickle.load(f)
    
    sin_day = convert_to_sin_day(day_num)
    cos_day = convert_to_cos_day(day_num)

    scores = 0
    total = 0

    for i in range(len(X)):
        if(X[i][0] == sin_day and X[i][1] == cos_day):

            predicted_list = df.predict([X[i]])[0]
            
            #Loop through predicted list to calculate how many rooms it predicted to be occupied
            no_predicted_rooms = 0
            for j in range(len(predicted_list)):
                if(predicted_list[j] == 1):
                    no_predicted_rooms += 1

            scores += no_predicted_rooms
            total += 1
    
    return(scores/total)

#Plots a graph of days vs average number of rooms occupied
def days_vs_no_rooms_occupied():

    day_nums = [1,2,3,4,5]
    average_no_rooms_predicted_occupied = []
    average_no_rooms_actually_occupied = []

    #Populate list with correct averages for number of rooms occupied for stage
    for day_num in day_nums:
        actual_occupancy = gen_avg_actual_occupancy_days(day_num)
        average_no_rooms_actually_occupied.append(actual_occupancy)

    #Populate list with correct predictions for each stage 
    for day_num in day_nums:
        prediction = gen_avg_predicted_occupancy_days(day_num)
        average_no_rooms_predicted_occupied.append(prediction)

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    #Create df
    df = pd.DataFrame({'Actually occupied' : average_no_rooms_actually_occupied,'Predicted occupied' : average_no_rooms_predicted_occupied}, days)
  
    #Plot graph
    ax = df.plot(kind='bar')

    # Set x and y labels
    ax.set_xlabel('Days')
    ax.set_ylabel('Average number of rooms occupied')

    #Set ticks
    yTicks = [1,2,3,4,5,6,7,8,9,10]
    plt.yticks(yTicks)
    plt.xticks(rotation = 0)

    plt.show()


actual_agg_occupancy_vs_time()