# -*- coding: utf-8 -*-

import cv2
import time
import imutils
import _csv as csv
import datetime
import os
#print(cv2.__version__)



def csvConvertRaw(data):
    with open('C:/Users/DRizvi/Desktop/Vehicle Detection/vehicle_detection_haarcascades-master/Video_Data.csv', 'ab') as vidprocess:
        process = csv.writer(vidprocess, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for item in data:
            process.writerow(item)
    vidprocess.close()

def cleanList(raw_data):
    output = []
    for row in raw_data:
        column = 0
        new_row = []
        while column < len(row):
            if row[column] != '*':
                new_row.append(row[column])
            column += 1
        output.append(new_row)

    return output

def makeList(file):
    with open(file, 'rb') as input:
        read = csv.reader(input)
        output = []

        for row in read:
            output.append(row)

    input.close()
    return output

def AddSpaces(List):
    numRows = len(List)
    numColumns = len(List[numRows-1])

    row = 0

    while (row < numRows):
        while(len(List[row]) < numColumns):
            List[row].append('')
        row += 1

    return List
    

def DeleteColumns(CarList):
    numRows = len(CarList)
    numColumns = len(CarList[0])
    row = 0
    column = 2

    row1 = 0
    framesPresent = 0

    while(column < numColumns):
        while(row < numRows):
            if((CarList[row][column] != '') and (CarList[row][column] != ' ') and (CarList[row][column] != '-')):
                framesPresent += 1
            row += 1
        if(framesPresent < 5):
            while(row1 < numRows):
                CarList[row1][column] = '*'
                CarList[row1][column+1] = '*'
                row1 += 1
            row1 = 0
        row = 0
        framesPresent = 0
        column += 2

    return CarList


def remakeCSV():
    L1 = makeList('C:/Users/DRizvi/Desktop/Vehicle Detection/vehicle_detection_haarcascades-master/Video_Data_export.csv')
    L2 = AddSpaces(L1)
    L3 = DeleteColumns(L2)
    L4 = cleanList(L3)
    csvConvertRaw(L4)
    os.remove('C:/Users/DRizvi/Desktop/Vehicle Detection/vehicle_detection_haarcascades-master/Video_Data_export.csv')

            

cv2.destroyAllWindows()
