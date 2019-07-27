# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 2019

@author: Marcus Futterlieb
"""

import sched,time,csv;

def initializer():
    s                                       = sched.scheduler(time.time, time.sleep)
    sleepTime                               = 0.0001;
    environmenStopCondition                 = 1000;
    schedCounter                            = 1;
    batteryLevel                            = 100;
    moistureLevel                           = 100;
    averageTemperature                      = 15;
    maxSolarPowerForBatteryGeneration       = 20;
    enableGraphics                          = True;
    
    #create storage file
    with open('log.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['schedCounter','days', 'partialDays', 'batteryLevel', 
                             'averageTemperature', 'moistureLevel' ])
    
    return [s,sleepTime,environmenStopCondition,schedCounter,batteryLevel,
            moistureLevel,averageTemperature,
            maxSolarPowerForBatteryGeneration,enableGraphics];
