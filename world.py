# -*- coding: utf-8 -*-

"""
Created on Mon Jul 15 2019
@author: Marcus Futterlieb

"""

import random, math, csv
#import for plot
from log import csv_plotter;
from init import initializer;
from pi import piFunctions;
#setup variables###############################################################
###############################################################################
[s,sleepTime,environmenStopCondition,schedCounter,batteryLevel,moistureLevel,
 averageTemperature,maxSolarPowerForBatteryGeneration, enableGraphics] = initializer();

 

#function definitions##########################################################
###############################################################################
def sigmoid(x):
    return 1 / (1 + math.e ** -x)

def world(sc,schedCounter,batteryLevel,moistureLevel,averageTemperature,
                 maxSolarPowerForBatteryGeneration):
    #set days and hours
    dayTime = False;
    (days,partialDays) = divmod(schedCounter, 24);
    #set approximate temperature (assuming daytime from 10-20 and night from 21-9)
    if (partialDays>10) and (partialDays<20):
        #print("day time")
        dayTime = True;
        averageTemperature = (averageTemperature + random.randint(22,35))*0.5;
        #set solar power generation
        batteryLevel += random.randint(10,maxSolarPowerForBatteryGeneration);
    else:
        #print("night time")   
        dayTime = False;
        averageTemperature = (averageTemperature + random.randint(10,18))*0.5;
    if batteryLevel > 100:
        batteryLevel = 100;
    #set moisture level depending on temperature
    if moistureLevel>0:
        moistureLevel -= sigmoid(averageTemperature-15);
    else:
        moistureLevel = 0.0;
    #set battery level
    batteryLevel -= 3; #passive consumption of the raspoberry pi
    #interfacing with the pi
    [pumpActivation,shutdown] = piFunctions(dayTime,batteryLevel,moistureLevel);
    

   
    #Raspberry Pi functions
    if pumpActivation>0:
        print("environment: pump activated");
        moistureLevel += random.randint(1,pumpActivation);
        batteryLevel -= sigmoid((pumpActivation/20)-2)*30;
        #division by 20 because that is the lowest pumpActivation
        #-2 to get the sigmoid to something like 0.25
        #*30 to have the result at 25 (~) if the pump is activated at full pumpActivation
        
        

       

    toStore = [schedCounter,days, partialDays, batteryLevel, averageTemperature,
               moistureLevel ];
    #storing information
    with open('log.csv','a') as csvfile:
        wr = csv.writer(csvfile, dialect='excel')
        wr.writerow(toStore)
        #csvfile.write(",".join(toStore));

    #print ("day : ",days, "hours : ",(partialDays));
    print ("day : ",days)
    print ("battery level is ", batteryLevel);
    #print ("it is ", averageTemperature,"degrees");
    #print ("moisture level ", moistureLevel);
    #print ("the sigmoid(temperature) is",sigmoid(averageTemperature-15));
    schedCounter+=1;
    #stop condition test
    if (schedCounter<environmenStopCondition) and (batteryLevel>5) and (shutdown==False):
        s.enter(sleepTime, 1, world, (sc,schedCounter,batteryLevel,
                                             moistureLevel,averageTemperature,
                                             maxSolarPowerForBatteryGeneration));
    else:
        print('Environment: End of simulation');

   
        

#main function#################################################################
###############################################################################
s.enter(sleepTime, 1, world, (s,schedCounter,batteryLevel,moistureLevel,
                                     averageTemperature,
                                     maxSolarPowerForBatteryGeneration));
s.run();

#analysis #####################################################################
###############################################################################
csv_plotter();
