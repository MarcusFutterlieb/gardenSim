# -*- coding: utf-8 -*-

"""
Created on Mon Jul 15
@author: Marcus Futterlieb

"""

import sched, time, random, math, csv, pandas
#import for plot
import matplotlib
import matplotlib.pyplot as plt

#setup variables###############################################################
###############################################################################
s                                       = sched.scheduler(time.time, time.sleep)
sleepTime                               = 0.0001;
environmenStopCondition                 = 1000;
schedCounter                            = 1;
batteryLevel                            = 100;
moistureLevel                           = 100;
averageTemperature                      = 15;
maxSolarPowerForBatteryGeneration       = 20;

#create storage file
with open('log.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['schedCounter','days', 'partialDays', 'batteryLevel', 'averageTemperature', 'moistureLevel' ])

 

 

#function definitions##########################################################
###############################################################################
def sigmoid(x):
    return 1 / (1 + math.e ** -x)

def environModel(sc,schedCounter,batteryLevel,moistureLevel,averageTemperature,maxSolarPowerForBatteryGeneration):
    #set days and hours
    (days,partialDays) = divmod(schedCounter, 24);
    #set approximate temperature (assuming daytime from 10-20 and night from 21-9)
    if (partialDays>10) and (partialDays<20):
        #print("day time")
        averageTemperature = (averageTemperature + random.randint(22,35))*0.5;
        #set solar power generation
        batteryLevel += random.randint(10,maxSolarPowerForBatteryGeneration);
    else:
        #print("night time")   
        averageTemperature = (averageTemperature + random.randint(10,18))*0.5;
    #set moisture level depending on temperature
    if moistureLevel>0:
        moistureLevel -= sigmoid(averageTemperature-15);
    else:
        moistureLevel = 0.0;
    #set battery level
    batteryLevel -= 3; #passive consumption of the raspoberry pi
    if (batteryLevel<0) or (batteryLevel>100):
        if batteryLevel<0:
            batteryLevel = 0;
            print("shut down Raspberry Pi due to low battery");
        if batteryLevel>100:
            batteryLevel=100;

    print ("the environment after",days, "day and ",(partialDays), "hours is now being simulasted ...");
    print ("battery level is ", batteryLevel);
    #print ("it is ", averageTemperature,"degrees");
    #print ("moisture level ", moistureLevel);
    #print ("the sigmoid(temperature) is",sigmoid(averageTemperature-15));

   
    #Raspberry Pi functions
    if moistureLevel<30:
        moistureLevel += 30;
        batteryLevel -= 10; # battery usage of the pump
        print("pump being used")
    else:
        moistureLevel = moistureLevel;

       

    toStore = [schedCounter,days, partialDays, batteryLevel, averageTemperature, moistureLevel ];
    #storing information
    with open('log.csv','a') as csvfile:
        wr = csv.writer(csvfile, dialect='excel')
        wr.writerow(toStore)
        #csvfile.write(",".join(toStore));

    schedCounter+=1;
    #stop condition test
    if (schedCounter<environmenStopCondition) and (batteryLevel>5):
        s.enter(sleepTime, 1, environModel, (sc,schedCounter,batteryLevel,moistureLevel,averageTemperature,maxSolarPowerForBatteryGeneration));
    else:
        print('Environment: End of simulation');

   
        

#main function#################################################################
###############################################################################
s.enter(sleepTime, 1, environModel, (s,schedCounter,batteryLevel,moistureLevel,averageTemperature,maxSolarPowerForBatteryGeneration));
s.run();

#analysis #####################################################################
###############################################################################

logData = pandas.read_csv('log.csv');
timeColumn = logData['schedCounter'];

batteryLevelColumn = logData['batteryLevel'];
fig, ax = plt.subplots()
ax.plot(timeColumn, batteryLevelColumn)
ax.set(xlabel='time (h)', ylabel='charge (%)',
       title='Battery level over time')
ax.grid()
fig.savefig("batteryLvl.png")
plt.show()



moistureLevelColumn = logData['moistureLevel'];
fig, ax = plt.subplots()
ax.plot(timeColumn, moistureLevelColumn)
ax.set(xlabel='time (h)', ylabel='moisture (%)',
       title='Moisture level over time')
ax.grid()
fig.savefig("moistureLvl.png")
plt.show()



temperatureColumn = logData['averageTemperature'];
fig, ax = plt.subplots()
ax.plot(timeColumn, temperatureColumn)
ax.set(xlabel='time (h)', ylabel='temperature (°C)',
       title='Average temperature over time')
ax.grid()
fig.savefig("temperatureLvl.png")
plt.show()
