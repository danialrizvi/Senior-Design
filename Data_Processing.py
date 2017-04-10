# After mission is complete, take CSV file generated from video data and generate readable metrics in new CSV file

import _csv as csv
import math
import datetime
import numpy as np

# altitude = vehicle.LocationGlobalRelative[2]
altitude = 100
FOV_x = altitude * np.tan(np.deg2rad(94.4/2)) * 2
FOV_y = altitude * np.tan(np.deg2rad(55.0/2)) * 2
pixel_width = 800
pixel_height = 450
ft_per_pixel_x = FOV_x / pixel_width
ft_per_pixel_y = FOV_y / pixel_height
mi_per_ft = 1.0 / 5280.0
hr_per_sec = 3600

current_time = datetime.datetime.now()

def dataExport(file):
    with open(file, 'rb') as columns:
        read = csv.reader(columns)
        position_list = []
        prev_row = []
        current_row = []
        vehicle_number = 1

        # Add code for first frame of data
        first_row = filter(None, read.next())
        num_cars = (len(first_row) - 2) / 2
        for k in range(0, num_cars):
            position_list.append([vehicle_number, first_row[1], first_row[vehicle_number*2], first_row[vehicle_number*2+1]])
            vehicle_number += 1
        prev_row = first_row

        # CSV files force uniform length
        # If second row has 4 columns and the first row only has 2
        # Then the file will automatically add two empty strings to the first row
        # Filter function used to prevent this

        # Code for subsequent frames
        for row in read:
            current_row = filter(None, row)
            if len(current_row) > len(prev_row): # If the length of the row has increased a new car has been added
                iterations = (len(current_row) - len(prev_row)) / 2 # Find out how many new cars have been added
                for j in range(0, iterations):
                    # Add vehicle number, timestamp, x coord, and y coord to a list
                    position_list.append([vehicle_number, row[1], row[vehicle_number*2], row[vehicle_number*2+1]])
                    vehicle_number += 1
            # Check if there are any new dashes in the row
            k = 0
            while k <= len(current_row)/2 - 2:
                if(current_row[2+k*2]) == '-' and prev_row[2+k*2] != '-': # If this is first "-" in column, car has left
                    # For each new dash, append the corresponding time stamp to the position list
                    position_list[k].append(prev_row[1])
                    position_list[k].append(prev_row[2+k*2])
                    position_list[k].append(prev_row[3+k*2])
                    # Calculate velocity and add it
                    position_list[k].append(velocity_calc(position_list[k]))
                    # Print row to show data in real time
                    #print position_list[k]
                k += 1
            prev_row = current_row

    columns.close()
    return position_list

def velocity_calc(pos_data):
    # Constants for unit conversion
    global ft_per_pixel_x
    global ft_per_pixel_y
    global mi_per_ft
    global hr_per_sec
    
    x_dist = abs(int(pos_data[5]) - int(pos_data[2])) * ft_per_pixel_x
    y_dist = abs(int(pos_data[6]) - int(pos_data[3])) * ft_per_pixel_y
    #x_dist = abs(x_dist)
    #y_dist = abs(y_dist)
    total_dist = math.sqrt(x_dist*x_dist + y_dist*y_dist)
    # Get velocity in ft/sec
    velocity = total_dist / (float(pos_data[4]) - float(pos_data[1]))

    # Unit conversions
    velocity = velocity * mi_per_ft
    velocity = velocity * hr_per_sec

    return round(velocity, 1)


# Write function for converting list of lists into CSV file
def csvConvert(data):
    with open('C:/Users/DRizvi/Desktop/Vehicle Detection/vehicle_detection_haarcascades-master/Velocity_Data.csv', 'ab') as vidprocess:
        process = csv.writer(vidprocess, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        process.writerow(['Mission Start Time:', current_time])
        process.writerow(['Car Number', 'Entry Time Offset', 'Entry X Position', 'Entry Y Position', 'Exit Time Offst', 'Exit X Position', 'Exit Y Position', 'Average Velocity'])
        for item in data:
            process.writerow(item)
    vidprocess.close()

def DataProcessing():
    test_file = 'C:/Users/DRizvi/Desktop/Vehicle Detection/vehicle_detection_haarcascades-master/Video_Data.csv'
    test = dataExport(test_file)
    csvConvert(test)
