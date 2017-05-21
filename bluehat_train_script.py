from bluepy.btle import Scanner, DefaultDelegate
from apscheduler.schedulers.background import BlockingScheduler
from sys import argv
import logging
import requests
import json
import datetime
import threading
import time

logging.basicConfig()
# logging.getLogger('requests').setLevel(logging.WARNING)
# logging.basicConfig(level=logging.DEBUG)
#
script, filename = argv
print filename




scanner = Scanner()


def scheduledAdvertiserScan():
    devices = scanner.scan(1.0)
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    json_list = []
    for dev in devices:
        json_data = {}
        uuid = dev.scanData.get(255, None)
        if(uuid is not None):
            uuidStr = dev.scanData.get(255, None).encode("hex")[:28]
            if (uuidStr == "ffff0123456789abcdefffffffff"):
                json_data = {}
                deviceID = dev.scanData.get(255, None).encode("hex")[28:36]
                rssi = dev.rssi
                data = dev.scanData.get(255, None).encode("hex")[37:]
                print "Time: %s" % time
                print "Device ID: %s" % deviceID
                print "RSSI: %d dB\n" % rssi
                json_list.append(json_data)
                with open(filename, "a") as outputFile:
                    outputFile.write("Time %s \n" % time)
                    outputFile.write("ID: %s \n" % deviceID)
                    outputFile.write("RSSI: %d \n" % rssi)
                    outputFile.write("\n")

if __name__ == "__main__":

    print 'Starting Observer Scan Scheduler!\n'
    scheduler = BlockingScheduler()
    scheduler.add_job(scheduledAdvertiserScan, 'interval', seconds = 2, id = 'advertiserScan', misfire_grace_time = 1)
    scheduler.start()
