#!/usr/bin/env python

import bluetooth

import string
import signal
import time
import sys

from settings import (BT_SCANNER_DURATION, BT_SCANNER_LOGGING, BT_SCANNER_DATAHTML, BT_SCANNER_LOGPATH)
from global_settings import (STATION_ID) 

# -- Inicio de la clase BluetoothScanner ------------------------------

class BluetoothScanner(object):

	class StopException(Exception):
		pass

	def __init__(self):
		global _btsensor
		_btsensor = self

		self.fLogging = open(BT_SCANNER_LOGGING,'a')
		msg = "Initializing bluetooth devices sensor..."
        	self.printlog(msg)

		self.datahtml = open(BT_SCANNER_DATAHTML,'w')

        	current_time = time.strftime("%Y-%m-%d_%H:%M:%S")
        	self.FILELOG = BT_SCANNER_LOGPATH + "/registerbt_" + current_time + ".log"
		self.fileLog = open(self.FILELOG,'w')
		self.fileLog.write("Sensor ID, Current time, MAC address, Bluetooth scanner duration\n")

        	msg = "Created %s file to store sesor data." % (self.FILELOG)
        	self.printlog(msg)

        	msg = "Sensing duration is %d seconds. " % (BT_SCANNER_DURATION)
        	self.printlog(msg)

		self._running = False

 	def start(self):
        	self._running = True
		try:
            		while self._running:
                		nearby_devices = bluetooth.discover_devices(duration=BT_SCANNER_DURATION,lookup_names=False)

                		current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                		for addr in nearby_devices:
                			self.fileLog.write("%s, %s, %s, %d \n" % (STATION_ID,current_time,addr,BT_SCANNER_DURATION))
              				self.fileLog.flush()

                		self.datahtml.seek(0)
                		number_of_devices = len(nearby_devices)
                		self.datahtml.write("%d\n" % number_of_devices)
                		self.datahtml.flush()

        	except self.__class__.StopException:
			self.stop()

	def stop(self):
		self.printlog('Bluetooth scanner stopping')
		self.fileLog.close()
		self.fLogging.close()
		self.datahtml.close()

	def running(self):
		self._running = False

	def printlog(self, msg):
		strTime = time.strftime("%H:%M:%S")
		strDate = time.strftime("%Y-%m-%d")

		self.fLogging.write("INFO " + strDate + " " + strTime + " => " + msg + "\n")
		self.fLogging.flush()

# -- Fin de la clase BluetoothScanner ------------------------------

def sigint_handler(signum, frame):
	_btsensor.running()

if __name__ == '__main__':
	signal.signal(signal.SIGINT, sigint_handler)
	signal.signal(signal.SIGTERM, sigint_handler)

	btscan = BluetoothScanner()
	btscan.start()
