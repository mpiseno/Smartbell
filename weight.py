#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
import io
import datetime
import numpy as np
import matplotlib.pyplot as plt

ser = serial.Serial()
ser.baudrate = 115200
ser.port = 'COM1'

ser.open()

fo = open('workoutData.txt', 'r+')
lines = fo.readlines()
curwgt = int(lines[0])
day = int(lines[1])


c = ''

workArray = np.array([])
dateArray = np.array([])

def lastWorkout(file):
    fileObject = open(file, "r")
    lines = fileObject.readlines()
    lastLine = lines[-1]
    fileObject.close()
    lastStats = lastLine.split(",")[1:]
    stats = []
    for i in lastStats:
        stats.append(int(i))
        
    repsCompleted = sum(stats[0:2])
    weight = stats[-1]
    return repsCompleted, weight

def makeNpArrays(file, workArray, dateArray):
    fo = open(file,"r")
    lines = fo.readlines()
    for line in lines[2:]:
        tempList = line.split(",")
        workNums = tempList[1:]
        dates = tempList[0]
        year = dates.split(" ")[0]
        month = dates.split(" ")[1]
        day = dates.split(" ")[2]
        tempdate = str(datetime.datetime(int(year), int(month), int(day)))
        date = tempdate.split(" ")[0]
        
        repList = []
        for i in workNums:
            repList.append(int(i))
        totalWork = sum(repList[0:2]) * repList[3]
        workArray = np.append(workArray, totalWork)
        
        dates = tempList[0]
        year = dates.split(" ")[0]
        month = dates.split(" ")[1]
        day = dates.split(" ")[2]
        tempdate = str(datetime.datetime(int(year), int(month), int(day)))
        date = tempdate.split(" ")[0]
        dateArray = np.append(dateArray, date)
    
    fo.close()    
    return workArray, dateArray

def graphWorkVsTime(workArray, dateArray):
    plt.plot(np.array(np.arange(len(dateArray))), workArray)
    plt.ylabel("Reps * Weight")
    plt.xlabel("Days since first workout")
    plt.title("Work Progression over time")
    plt.show()    


while(c != 'q'):
    c = raw_input("What would you like to do? (q for quit)(g for graph)(w for weight)")
    if c == 'w':
        print "Weight mode\n"
        first = int(ser.read(8))
        print first
        second = int(ser.read(8))
        third = int(ser.read(8))
        lines.append("2018 3 " + day + "," + first + "," + second + "," + third + "," + curwgt + "\n")
        workout = first + second + third
        if workout < 15 & completedReps >= 9:
            curwgt += 5
            print "good job! you increased in strength. next workout try " + curwgt
        elif workout < 24:
            curwgt -= 5
            print "bad job! you decreased in strength. next workout try " + curwgt
        else:
            print "good job! you completed your workout. next workout try " + curwgt
        lines[0] = str(curwgt)
        lines[1] = str(day+1)
        for i in lines[2:]:
            fo.write(i)
        
        
            
    elif c == 'g':
        print "Graph mode\n"
        workArray, dateArray = makeNpArrays(file, workArray, dateArray)
        graphWorkVsTime(workArray, dateArray)
    elif c == 'q':
        break
    else:
        continue

