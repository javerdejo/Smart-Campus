# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 13:09:32 2017

@author: Jamal Toutouh: jamaltoutouh@gmail.com
"""

import csv
import requests
import json

ADD_SOUND="http://150.214.214.19:3000/add/sound"
ADD_BLUETOOTH="http://150.214.214.19:3000/add/bluetooth"
ADD_WIFI="http://150.214.214.19:3000/add/wifi"



def sendData(url, data):
    sent = False
    headers = {'Content-type': 'application/json'}

    try:
        r = requests.post(url, data=json.dumps(data), headers=headers)
        print(r)
        sent = True
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
    except requests.exceptions.ConnectionError:
        # Error during connection
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print e
    return sent


with open('soundMin.log', 'r') as csvfile:
    with open('noSentSound.log','w') as csvWriterfile:
        csvFile = csv.reader(csvfile)
        csvWriterFile = csv.writer(csvWriterfile)
        for row in csvFile:
            if row[0] == 'Encabezado':
                continue;

            sensorId = row[0];
            noise = row[2];
            peak = row[3];
            dateTime = row[1];

            data ={'sensor_id':sensorId,
                   'noise':noise,
                   'peak':peak,
                   'date_time':dateTime}

            ok = sendData(ADD_SOUND, data)
            if (not ok):
                print "No tan perdecto"
                csvWriterFile.writerow(row)


with open('bluetoothMin.log', 'r') as csvfile:
    with open('noSentBT.log','w') as csvWriterfile:
        csvFile = csv.reader(csvfile)
        csvWriterFile = csv.writer(csvWriterfile)
        for row in csvFile:
            if row[0] == 'Current time':
                continue;

            sensorId = row[0];
            macAddress = row[2];
            dateTime = row[1];
            duration = row[3];

            data ={'sensor_id':sensorId,
                   'mac_address':macAddress,
                   'duration':duration,
                   'date_time':dateTime}

            ok = sendData(ADD_BLUETOOTH, data)
            if (not ok):
                print "No tan perdecto"
                csvWriterFile.writerow(row)

with open('wifiSensed.csv', 'r') as csvfile:
    with open('noSentWifi.log','w') as csvWriterfile:
        csvFile = csv.reader(csvfile)
        csvWriterFile = csv.writer(csvWriterfile)
        for row in csvFile:
            if row[0] == 'Sensor ID':
                continue;

            sensorId = row[0];
            macAddress = row[1];
            first_time = row[2];
            last_time = row[3];

            data ={'sensor_id':sensorId,
                   'mac_address':macAddress,
                   'first_time':first_time,
                   'last_time':last_time}

            ok = sendData(ADD_WIFI, data)
            if (not ok):
                print "No tan perdecto"
                csvWriterFile.writerow(row)
