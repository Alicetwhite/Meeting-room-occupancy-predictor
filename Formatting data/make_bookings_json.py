#This script will format meeting room bookings into a json

import json
from dateutil.parser import parse
from datetime import *; from dateutil.relativedelta import *
import calendar
import operator 

# Checks to see if a parameter is a string or a float
def is_valid(str):
    if type(str) == float:
        return False

# Converts a float to a binary string
# This is needed as csv to json converted these strings as a float not a string
def float_to_binary_string(num):
    if num == 1.1111111111111111e+51:
        return '1111111111111111111111110000000000000000000000000000'
    elif num == 1e+51:
        return '1000000000000000000000000000000000000000000000000000'
    elif num == 1.111111111e+51:
        return '0100000000000000000000000000000000000000000000000000'
    else:
        return num

#Updates any incorrect floats to strings
with open("../jsons/room_bookings.json", 'r') as bookings:
    
    content = json.load(bookings)

    for booking in content:
        if is_valid(booking['Start Date']) == False:
            booking['Start Date'] = float_to_binary_string(booking['Start Date'])

#Writes correctly formatted bookings to room_bookings.json
with open("../jsons/room_bookings.json", "w") as outfile:
    outfile.write(json.dumps(content))

# Does this binary string have repeated bookings
def is_it_repeated(binary_bookings):
    bookings_list = list(binary_bookings)
    bookings_list.sort()
    if bookings_list[len(bookings_list)-2] == '1':
        return True    
    else:
        return False
        
#Write all bookings which are recurring to file repeated_bookings.json
with open("../jsons/room_bookings.json") as bookings:
    content = json.load(bookings)
    
    all_repeats = [] # List of all jsons which have recurring bookings

    with open("../jsons/repeated_bookings.json", 'w') as repeated:

        # Add every repeated booking to list
        for booking in content:
            if is_it_repeated(booking['Start Date']) == True:
                all_repeats.append(booking)
        
        #Write every booking which has repeated bookings to a file
        json.dump(all_repeats, repeated)     

#Duplicate jsons of repeated bookings with updated dates to new file duplicates_new.json
with open("../jsons/repeated_bookings.json") as bookings:
    content = json.load(bookings)

    new_json = []

    for i in range(len(content)):
        booking = content[i]
        
        booking_list = list(booking['Start Date']) # Converts binary repeated bookings string into list
        date = parse(booking['Scheduled Start Date'], dayfirst = True) #Convert string to date type

        first_week = False # Flag detecting whether it is the first booking
        second_week = False # Flag detecting whether reached second week
        current_week_number = 0 # Stores the current week number of the recurring booking

        # If there are repeated bookings find the corresponding date
        for i in range(len(booking_list)):
            if booking_list[i] == '1':
                #If it is the first date where meeting occurs set first week flag to week number
                if first_week == False:
                    first_week = True
                    current_week_number = i
                # If its a future booking work out the date
                else:
                    second_week = True
                    week_jump = i-current_week_number
                    current_week_number = i
                    date = date+relativedelta(weeks=+week_jump)
                
                #Create dictionary of new json with updated date
                if second_week == True:
                    new_dict = {"Name":booking['Name'], "Start Date":booking['Start Date'], "Scheduled Start Date":date.strftime('%d/%m/%Y'),"Day":booking['Day'], "Start time":booking['Start time'], "End time":booking['End time'], "Duration as duration":booking['Duration as duration'],"Locations":booking['Locations'], "Size of Locations":booking['Size of Locations']}
                    new_json.append(new_dict) #Add this to new json list

    # Write all new jsons to file
    with open("../jsons/duplicates_new.json", 'w') as outfile:
        json.dump(new_json,outfile)   

#Merging duplicates and non duplicate room bookings into new file final_room_bookings
with open("../jsons/duplicates_new.json") as duplicates:
    duplicates_content = json.load(duplicates) #content in duplicates
    
    with open("../jsons/room_bookings.json") as bookings:
        content2 = json.load(bookings) #content in non duplicates

        for duplicate in duplicates_content:
            content2.append(duplicate)

        # Put JSON in chronological order
        content2 = sorted( content2, key=lambda el: (parse(el['Scheduled Start Date'], dayfirst=True), el['Start time']), reverse=False )

        #print(parse(content2[0]['Scheduled Start Date']))

        #Writing all room bookings to file final_room_bookings
        with open("../jsons/final_room_bookings.json", 'w') as outfile:
            json.dump(content2, outfile)