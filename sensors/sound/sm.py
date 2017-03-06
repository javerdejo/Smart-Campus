#!/usr/bin/env python
# Auth: Javier Arellano-Verdejo (J@Vo)
# Date: Jul/2016

import usb.core
import usb.util
import signal
import math
import time
import sys

from settings import (VERBOSE, INTERVAL, LOGPATH, FLOGGING, DATAHTML, LAEQ)
from global_settings import (STATION_ID)

class SoundMeterGM1356(object):

	class StopException(Exception):
		pass

	def __init__(self):
		global _soundsensor
		_soundsensor = self

		self.fLogging = open(FLOGGING,'a')
		self.datahtml = open(DATAHTML,'w')

		self._running = False

		self.VENDOR_ID = 0x64bd
		self.PRODUCT_ID = 0x74e3

		devFound = False
		while not devFound:
			self.device = usb.core.find(idVendor=self.VENDOR_ID, idProduct=self.PRODUCT_ID)
			if self.device is None:
				self.printlog("Device not found ...")
				time.sleep(3)
			else:
				self.printlog("Device found")
				devFound = True

		strTime = time.strftime("%H:%M:%S")
		strDate = time.strftime("%Y-%m-%d")

		self.FILELOG = LOGPATH + "/registersound_" + strDate + "_" + strTime + ".log"
		self.fileLog = open(self.FILELOG,'w')
		self.fileLog.write("Sensor ID, Date Time,Measure,Max,Speed,Curve,Range\n")

		if INTERVAL < 0.5:
			self.PAUSE = 1
		else:
			self.PAUSE = INTERVAL

	def start(self):
		self._running = True
		peak = 0
		low = 999

		if self.device.is_kernel_driver_active(0):
			try:
				self.device.detach_kernel_driver(0)
				self.printlog("kernel driver detached")
			except usb.core.USBError as e:
				self.printlog("Could not detach kernel driver: %s" % str(e))
				sys.exit("Could not detach kernel driver: %s" % str(e))

		try:
			self.printlog("Taking measurements of sound ...")

			start_time = time.time()
			cur_time = time.time()
			laeq = 0
			ti = 1
			read_count = 0

			while self._running:

				if cur_time - start_time < LAEQ:
					try:
						data = "b3 00 00 00 00 00 00 00"
						buf = data.replace(" ", "").decode('hex')
						self.device.write(0x02, buf, 1000)
						ret = self.device.read(0x81, 8, 1000)
						values = bytearray(ret)
					except usb.core.USBError:
						continue

					if len(values) == 8:
						measure = (256*values[0] + values[1]) / 10.0

						if measure > 130 or measure < 0:
							measure = 0

						if measure > peak:
							peak = measure

						if measure < low:
							low = measure

						laeq = laeq + (math.pow(10, (measure/10)) * INTERVAL)
						read_count = read_count + 1

					cur_time = time.time()
				else:
					laeq = 10 * math.log10(laeq/read_count);
					self.save_data(laeq, peak, low)
					read_count = 0
					laeq = 0
					ti = 1

					start_time = cur_time
					time.sleep(self.PAUSE)

			self.stop()
		except self.__class__.StopException:
			self.stop()

	def save_data(self, laeq, peak, low):
		try:
			data = "b3 00 00 00 00 00 00 00"
			buf = data.replace(" ", "").decode('hex')
			self.device.write(0x02, buf, 1000)
			ret = self.device.read(0x81, 8, 1000)
			values = bytearray(ret)
		except usb.core.USBError:
			pass

		strTime = time.strftime("%H:%M:%S")
		strDate = time.strftime("%Y-%m-%d")

		if (values[2] >> 6) == 1:
			strSpeed = "Fast"
		else:
			strSpeed = "Slow"

		if (values[2] >> 4 & 0x01) == 0:
			strCurve = "A"
		else:
			strCurve = "C"

		range_cfg = values[2] & 0x07
		strDataLog = "%s,%s %s,%2.1f,%2.1f,%2.1f,%s,%s,%d\n" % (STATION_ID,strDate, strTime, laeq, low, peak, strSpeed, strCurve, range_cfg)

		self.fileLog.write(strDataLog)
		self.fileLog.flush()

		strDataHtml = "%2.1f %2.1f\n" % (laeq, peak)
		self.datahtml.seek(0)
		self.datahtml.write(strDataHtml)
		self.datahtml.flush()

		if VERBOSE == 1:
			self.printlog("%s %s %s %2.1f db Max: %2.1f db %s %s %d" % (strDate, strTime, STATION_ID, laeq, peak, strSpeed, strCurve, range_cfg))

	def stop(self):
		self.printlog('Stopping')
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

# -- Fin de la clase SoundMeterGM1356 ------------------------------

def sigint_handler(signum, frame):
	_soundsensor.running()

if __name__ == '__main__':
	signal.signal(signal.SIGINT, sigint_handler)
	signal.signal(signal.SIGTERM, sigint_handler)

	sm = SoundMeterGM1356()
	sm.start()
