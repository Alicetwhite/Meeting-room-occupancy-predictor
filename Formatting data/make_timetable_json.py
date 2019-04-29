#This script will format timetable into a json

import json
import datetime
import calendar
import time

interval_mins = 15 #Interval between times in X matrix

#Format json to delete irrelevant columns and make each entry for a specific week
with open('../jsons/timetable.json') as f:
    content = json.load(f)

    #Delete irrelevant columns in json
    for i in range(len(content)):
        del content[i]['Module']
        del content[i]['Type']
        del content[i]['Activity Code']
        del content[i]['Activity Name']
        del content[i]['Room']
        del content[i]['Staff']
        content[i]['Date'] = "Not yet set"
    
    new_json = [] #List to store new json for entry for a specific week

    #----------Create json where each entry is for a specific week-------------
    for i in range(len(content)):
        
        weeks = [] #List to store individual week numbers where this lecture occurs
        current_week = content[i]['Weeks'] # Unformatted weeks from json
        split = current_week.split(',') #List which stores each week section
        
        for j in split:

            #----Create weeks list to store the week numbers which this lecture occurs----

            #If week section has multiple weeks in it
            if('-' in j):
                subsplit = j.split('-') #List to store start and end week
                difference = 0 #Difference between start and end week
                k = 0 #Counter for looping through subsplit

                #Find difference between the two weeks
                while (k<len(subsplit)):
                    if(k != len(subsplit)-1):
                        difference = int(subsplit[k+1]) - int(subsplit[k])
                        #Loop through difference and add each week to weeks list
                        for k in range(difference+1):
                            weeks.append(int(subsplit[0]) + int(k))
         
                    k = k + 1
                k=0 #Reset k
      
            #If it's a single week add it to weeks list
            else:
                weeks.append(int(j))
        
        # ----Create new entry in timetable for every week----
        for k in range(len(weeks)):
            new_dict = {"Day":content[i]['Day'], "Start Time":content[i]['Start Time'], "Duration":content[i]['Duration'],"Week":weeks[k],"Date":content[i]['Date'], "Stage":content[i]['Stage']}
            new_json.append(new_dict)
        
        # Write all new jsons to file
        with open("../jsons/timetable_week.json", 'w') as outfile:
            json.dump(new_json,outfile)

#Convert day string to number
def day_to_num(day):
    return {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6
    }.get(day, "Unknown")

#Converts week number to date at start of that week
def week_to_date(week):

    week_one = datetime.datetime.strptime("03/09/2018", "%d/%m/%Y")
    days_difference = (week-1)*7 #Number of days between week passed in and week one
    d = datetime.timedelta(days=days_difference) #Day difference in date format
    updated_date = week_one + d #New date 

    return updated_date

#Converts week and day to date
def week_day_to_date(day, week):
    
    start_date = week_to_date(week) 
    day_no = day_to_num(day)
    d = datetime.timedelta(days=day_no)
    updated_date = start_date + d

    return updated_date

def make_datetime(time, day, week):

    date = week_day_to_date(day, week) #Convert to date
    
    hour = int(time[:2])
    minute = int(time[3:])
    date = date.replace(hour=hour, minute=minute) #Set time 

    return date

#------Convert week number to date and set new json------
with open('../jsons/timetable_week.json') as f:
    content = json.load(f)

    #Set date for each entry in json
    for i in range(len(content)):
        date = make_datetime(content[i]['Start Time'], content[i]['Day'], content[i]['Week'])
        content[i]['Date'] = str(date)
    
        #Delete unnecessary columns
        del content[i]['Day']
        del content[i]['Week']

        #Set duration to integer
        content[i]['Duration'] = content[i]['Duration'][:1]

    #Output new json with correct date to file
    with open('../jsons/dt_week_timetable.json', 'w') as outfile:
        json.dump(content,outfile)

#--------Create new json where each lecture is every 15 mins-------
with open('../jsons/dt_week_timetable.json') as f:
    content = json.load(f)
    new_json = [] #List to store new json with intervals

    for i in range(len(content)):

        current = content[i] #Current lecture
        
        #Get date_time and number of intervals 
        date_time = datetime.datetime.strptime(current['Date'], "%Y-%m-%d %H:%M:%S")
        duration = int(current['Duration'])
        intervals = int(duration*60/interval_mins) #Number of intervals for this lecture

        #Update duration field of first lecture
        current['Duration'] = interval_mins
        
        new_json.append(current)

        #--------Create 15 minute intervals for each lecture-------

        start_min = date_time.minute #Start minute of interval before

        for j in range(intervals-1):
            #Increment time by specified interval
            updated_min = start_min + interval_mins     
            updated_hour = date_time.hour

            start_min = updated_min

            # Increment hour if needed
            if(updated_min >= 60):
                #If it is a new day reset to 00:00
                if(updated_hour >= 23):
                    updated_hour = 00
                    updated_min = 00
                else:
                    updated_hour = date_time.hour + 1
                    updated_min = updated_min - 60
                
                start_min = updated_min #Reset start_min if duration is more than one hour
                
            #Update time
            current_time = time.strptime(str(updated_hour)+":"+str(updated_min), "%H:%M")
            time_str = time.strftime("%H:%M", current_time)

            #Update date_time
            date_time = date_time.replace(hour=updated_hour, minute=updated_min)
            # date_time_str = date_time.strftime()

            #Create a new dictionary for this entry and add it to json list
            new_dict = {"Start Time":time_str, "Duration":interval_mins, "Date":str(date_time), "Stage":current['Stage']}
            new_json.append(new_dict)

    #Output new json with correct date to file
    with open('../jsons/final_timetable.json', 'w') as outfile:
        json.dump(new_json,outfile)
        

    

