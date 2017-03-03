#!/usr/bin/env python
# Auth: Jamal Toutouh
# Date: Feb/2017

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
