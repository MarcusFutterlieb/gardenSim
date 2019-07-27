# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 2019

@author: Marcus Futterlieb
"""
import pandas
import matplotlib.pyplot as plt
#analysis #####################################################################
###############################################################################
def csv_plotter():
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
