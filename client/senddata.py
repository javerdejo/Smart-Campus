#!/usr/bin/python
"""
Created on Fri Feb  3 13:09:32 2017

@author: Jamal Toutouh (http://www.jamal.es) jamaltoutouh@gmail.com

Smart Campus Sensor Project

Required "requests" module. Installation:
curl -OL https://github.com/kennethreitz/requests/tarball/master
"""

import csv
import requests
import json
import os
import socket
import fcntl
import struct
import sys
import getopt
import time

from global_settings import (STATION_ID)


ADD_SOUND="http://150.214.214.19:3000/add/sound"
ADD_BLUETOOTH="http://150.214.214.19:3000/add/bluetooth"
ADD_WIFI="http://150.214.214.19:3000/add/wifi"
ADD_STATUS="http://150.214.214.19:3000/add/status"

def writeLog(message):
    print message

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def renewIp():
    os.system('sudo dhclient -v -r wlan0')
    os.system('sudo dhclient -v wlan0')
    return get_ip_address('wlan0')

def sendData(url, data):
    sent = False
    headers = {'Content-type': 'application/json'}

    try:
        r = requests.post(url, data=json.dumps(data), headers=headers)
        sent = True
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        writeLog('Timeot')
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        writeLog('TooManyRedirects')
    except requests.exceptions.ConnectionError:
        # Error during connection
        writeLog('ConnectionError')
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        writeLog(e)
    return sent

def sendStatus(ip,event):
    current_time = time.strftime("%Y-%m-%d_%H:%M:%S");
    data ={'sensor_id':STATION_ID,
           'ip':ip,
           'event':event,
           'date_time':current_time}
    ok = sendData(ADD_STATUS, data)


def main(argv):
    soundFile = ''
    bluetoothFile = ''
    wifiFile = ''

    try:
        opts, args = getopt.getopt(argv,"hb:s:w:",[])
    except getopt.GetoptError:
        print 'sendData.py -s <sound data file> -b <bluetooth data file> -w <wifi data file>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'sendData.py -s <sound data file> -b <bluetooth data file> -w <wifi data file>'
            sys.exit()
        elif opt == '-s':
            soundFile = arg
        elif opt == '-b':
            bluetoothFile = arg
        elif opt == '-w':
            wifiFile = arg
    writeLog(soundFile)
    writeLog(bluetoothFile)
    writeLog(wifiFile)

    #First the ip is renewed in order to limit connection problems
    sensorIp = renewIp()
    message = 'Senosor IP address: ' + str(sensorIp)
    writeLog(message)

    event = 1
    sendStatus(sensorIp,event)

    if (soundFile !=''):
        writeLog('Sending SOUND data....')
        rowOk = 0;
        rowError = 0;
        with open(soundFile, 'r') as csvfile:
            noSentFile =  soundFile + '.noSent'
            with open(noSentFile,'w') as csvWriterfile:
                csvFile = csv.reader(csvfile)
                csvWriterFile = csv.writer(csvWriterfile)
                try:

                    for row in csvFile:
                        if row[0] == 'Sensor ID':
                            csvWriterFile.writerow(row)
                            continue;

                        sensorId = row[0];
                        noise = row[2];
                        peak = row[3];
                        dateTime = row[1];

                        data ={'sensor_id':STATION_ID,
                               'noise':noise,
                               'peak':peak,
                               'date_time':dateTime}

                        ok = sendData(ADD_SOUND, data)
                        if (not ok):
                            csvWriterFile.writerow(row)
                            rowError = rowError + 1
                        else:
                            rowOk = rowOk + 1
                except csv.Error:
                    pass

        message = 'Correctly sent: ' + str(rowOk) + ', Failed: ' + str(rowError)
        writeLog(message)

    if (bluetoothFile !=''):
        rowOk = 0;
        rowError = 0;
        writeLog('Sending BLUETOOTH data....')
        with open(bluetoothFile, 'r') as csvfile:
	    nosentBT = bluetoothFile + '.noSent'
            with open(nosentBT,'w') as csvWriterfile:
                csvFile = csv.reader(csvfile)
                csvWriterFile = csv.writer(csvWriterfile)
                try:
                    for row in csvFile:
                        if row[0] == 'Sensor ID':
                            csvWriterFile.writerow(row)
                            continue;

                        sensorId = row[0];
                        macAddress = row[2];
                        dateTime = row[1];
                        duration = row[3];

                        data ={'sensor_id':STATION_ID,
                               'mac_address':macAddress,
                               'duration':duration,
                               'date_time':dateTime}

                        ok = sendData(ADD_BLUETOOTH, data)
                        if (not ok):
                            csvWriterFile.writerow(row)
                            rowError = rowError + 1
                        else:
                            rowOk = rowOk + 1
                except csv.Error:
                    pass

        message = 'Correctly sent: ' + str(rowOk) + ', Failed: ' + str(rowError)
        writeLog(message)

    if (wifiFile !=''):
        rowOk = 0;
        rowError = 0;
        writeLog('Sending WIFI data....')
        with open(wifiFile, 'r') as csvfile:
	    nosentWifi = wifiFile + '.noSent'
            with open(nosentWifi,'w') as csvWriterfile:
                csvFile = csv.reader(csvfile)
                csvWriterFile = csv.writer(csvWriterfile)
                try:
                    for row in csvFile:
                    	if row[0] == 'Sensor ID':
                        	csvWriterFile.writerow(row)
                        	continue;

                    	sensorId = row[0];
                    	macAddress = row[1];
                    	first_time = row[2];
                    	last_time = row[3];
                    	power = row[4];

                    	data ={'sensor_id':STATION_ID,
                           'mac_address':macAddress,
                           'first_time':first_time,
                           'last_time':last_time,
                           'power': power}

                    	ok = sendData(ADD_WIFI, data)
                    	if (not ok):
                        	csvWriterFile.writerow(row)
                        	rowError = rowError + 1
                    	else:
                        	rowOk = rowOk + 1
                except csv.Error:
                    pass
        message = 'Correctly sent: ' + str(rowOk) + ', Failed: ' + str(rowError)
        writeLog(message)

if __name__ == "__main__":
   main(sys.argv[1:])
