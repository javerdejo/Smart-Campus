#!/usr/bin/env python
# Auth: Jamal Toutouh
# Date: Jul/2016

import csv
import time
import os
import sys
import operator

from global_settings import (STATION_ID)

listOfFiles = [];

readingDirectory = '/wifi_sensed/';
storingDirectory = '/sensor_client/sensorBackup/to_send';
historicStoringDirectory = '/sensor_client/sensorBackup/pending';

storingCsvFile = 'registerwifi.csv';

wifiSensedInformationFile = open(storingDirectory + '/' + storingCsvFile, "w");
csvWriter = csv.writer(wifiSensedInformationFile);
csvWriter.writerow(['Sensor ID', 'MAC', 'First Seen', 'Last Seen', 'Power']);
devices = 0;
numberOfFiles = 0;

accessPoints = True;
for file in os.listdir(readingDirectory):
    if file.endswith(".csv"):
        listOfFiles.append(file)
        with open(readingDirectory + '/' + file, 'r') as f:
            reader = csv.reader(f)
            while True:
                try:
                    row = next(reader);
                except csv.Error:
                    continue
                except StopIteration:
                    break

                if len(row) == 0 or len(row) < 6:
                    continue

                if (row[0] in (None, "") or row[1] in (None, "")) or (row[2] in (None, "") or row[3] in (None, "")):
                    continue

                if row[0] == 'BSSID':
                    accessPoints = True;
                    continue;

                if row[0] == 'Station MAC':
                    accessPoints = False;
                    continue

                mac = row[0];
                firstSeen = row[1];
                lastSeen = row[2];

                if accessPoints == True:
                    power = row[8];
                else:
                    power = row[3];

                devices = devices + 1;
                csvWriter.writerow([STATION_ID, mac, firstSeen, lastSeen, power]);

wifiSensedInformationFile.close();

for file in listOfFiles:
    source = readingDirectory + '/' + file;
    destination = historicStoringDirectory + '/' + file;
    os.rename(source,destination);

print(devices);
print(len(listOfFiles));
