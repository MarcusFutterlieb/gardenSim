# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 2019

@author: Marcus Futterlieb
"""
def piFunctions(dayTime,batteryLevel,moistureLevel):
    pumpActivation = 0; # pump activation normalized between 0 and 100 
    shutdown = False;
    if (batteryLevel<5):
        print("pi : shut down Raspberry Pi due to low battery");
        shutdown = True;
   
    #Raspberry Pi functions
    if moistureLevel<10 and batteryLevel>40:
        if dayTime == True:
            pumpActivation = 100;
        else:
            pumpActivation = 20;
        print("pi: activating the pump");

    return [pumpActivation,shutdown];
