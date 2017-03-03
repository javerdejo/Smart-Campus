#!/usr/bin/python
"""
Created on Fri Feb  3 13:09:32 2017

@author: Jamal Toutouh (http://www.jamal.es) jamaltoutouh@gmail.com

Smart Campus Sensor Project
"""

import os
import sys
import shutil

readingDirectory = '/bluetooht_sensed/';
storingDirectory = '/sensor_client/sensorBackup/to_send';
historicStoringDirectory = '/sensor_client/sensorBackup/pending';

listOfFiles = []
# As the data files have already the required format to be sent to the server we just move/copy them into the bakup directories
for file in os.listdir(readingDirectory):
    if file.endswith(".log"):
        listOfFiles.append(file)

#First copy files in the backup storing directory
for file in listOfFiles:
    source = readingDirectory + '/' + file
    destination = storingDirectory + '/'
    shutil.copy2(source, destination)

#Second move files in the historic storing directory
for file in listOfFiles:
    source = readingDirectory + '/' + file;
    destination = historicStoringDirectory + '/' + file;
    os.rename(source,destination);

#Restart bluetooth sensor service
os.system('sudo /etc/init.d/btscan.sh restart')
