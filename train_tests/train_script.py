from bluepy.btle import Scanner, DefaultDelegate
from apscheduler.schedulers.background import BlockingScheduler
from sys import argv
import logging
import requests
import json
import datetime
import threading
import time

script, filename = argv
print filename

scanner = Scanner()
def scheduledAdvertiserScan():
    devices = scanner.scan(.2)
    for dev in devices:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = dev.scanData.get(255, None)
        if(data is not None):
            adv_data = data.encode("hex")
            uuid = adv_data[:28]
            uuidStr = dev.scanData.get(255, None).encode("hex")[:28]
            if (uuid == "ffff0123456789abcdefffffffff"):
                deviceID = adv_data[28:36]
                rssi = dev.rssi
                data = adv_data[37:]
                print "Time: %s" % time
                print "Device ID: %s" % deviceID
                print "RSSI: %d dB\n" % rssi
                with open(filename, "a") as outputFile:
                    outputFile.write("Time %s \n" % time)
                    outputFile.write("ID: %s \n" % deviceID)
                    outputFile.write("RSSI: %d \n" % rssi)
                    outputFile.write("\n")
#


if __name__ == "__main__":

    print 'Starting Observer Scan Scheduler!\n'
    while True:
        scheduledAdvertiserScan()
