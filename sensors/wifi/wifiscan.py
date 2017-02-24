#!/usr/bin/env python
# Auth: Jamal Toutouh & Javier Arellano-Verdejo (J@Vo)
# Date: Jul/2016

import os
import signal
import subprocess
import sys
import time
import usb.core
import usb.util

from settings import (VERBOSE, INTERVAL, LOG_PATH, FILE_LOG, DATA_HTML, INTERFACE, VENDOR_ID, PRODUCT_ID, MONITOR_INTERFACE, WIFI_DATAPATH_CSV, WIFI_SCANNER_LOGGING, WIFI_SENSING_TIME)

# -- Inicio de la clase WifiScanner ------------------------------

class WifiScan(object):
	class StopException(Exception):
		pass

	def __init__(self):

		global _wifisensor
		_wifisensor = self

		self.fLogging = open(WIFI_SCANNER_LOGGING,'a')
		msg = "Initializing wifi devices sensor..."
        	self.printlog(msg)

		devFound = False
		while not devFound:
			self.device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
			if self.device is None:
				self.printlog("Device not found ...")
				time.sleep(3)
			else:
				self.printlog("Device found")
				devFound = True

		output = subprocess.call(["iwconfig", MONITOR_INTERFACE], stderr=subprocess.STDOUT)
		if output != 0:
			self.printlog("Starting the interface " + INTERFACE + " in monitor mode ")
			subprocess.call(["airmon-ng", "start", INTERFACE],  stderr=subprocess.STDOUT)
			self.printlog("Interface " + INTERFACE + " started in monitor mode")


 	def start(self):
		self._running = True
		current_time = time.strftime("%Y-%m-%d_%H:%M:%S");
		self.CVS_FILELOG = WIFI_DATAPATH_CSV + '/registerwifi_' + current_time;
		self.fd = None
		try: 
			self.printlog("Starting getting data from " + MONITOR_INTERFACE + " monitor interface.");
			self.fd = subprocess.Popen(['airodump-ng', '--write', self.CVS_FILELOG, '--output-format', 'csv', MONITOR_INTERFACE], bufsize=1, stderr=subprocess.STDOUT)
			self.printlog("Monitor interface " + MONITOR_INTERFACE + " started getting data.");
			time.sleep(WIFI_SENSING_TIME);
			self.fd.kill();
			
			while self._running:
				current_time = time.strftime("%Y-%m-%d_%H:%M:%S");
                		self.CVS_FILELOG = WIFI_DATAPATH_CSV + '/registerwifi_' + current_time;
				self.fd = subprocess.Popen(['airodump-ng', '--write', self.CVS_FILELOG, '--output-format', 'csv', MONITOR_INTERFACE], bufsize=1, stderr=subprocess.STDOUT)
				self.printlog("Monitor interface " + MONITOR_INTERFACE + " is getting data.");
				time.sleep(WIFI_SENSING_TIME)
				self.fd.kill();
	
		except self.__class__.StopException:
			self.stop();

		self.printlog("Stopping getting data from " + MONITOR_INTERFACE + " monitor interface.");
		#self.fd.kill();
		self.printlog("Monitor interface " + MONITOR_INTERFACE + " is stopped.");

		
	def stop(self):
		self.fLogging.close()
		self._running = False

	def running(self):
		self._running = False

	def printlog(self, msg):
		strTime = time.strftime("%H:%M:%S")
		strDate = time.strftime("%Y-%m-%d")

		self.fLogging.write("INFO " + strDate + " " + strTime + " => " + msg + "\n")
		self.fLogging.flush()

# -- Fin de la clase WifiScanner ------------------------------

def sigint_handler(signum, frame):
	_wifisensor.running()

if __name__ == '__main__':
	signal.signal(signal.SIGINT, sigint_handler)
	signal.signal(signal.SIGTERM, sigint_handler)

	wifi_scan = WifiScan()
	wifi_scan.start()
