from bluepy.btle import Scanner, DefaultDelegate
from apscheduler.schedulers.background import BlockingScheduler
from socketIO_client import SocketIO, LoggingNamespace, BaseNamespace
import logging
import requests
import json
import datetime

OBSERVER_ID = "1"
OBSERVER_LOCATION = "Location 1"

class BlueHatObserver(BaseNamespace):
    def on_connect(self):
        print('[Connected]')

    def on_reconnect(self):
        print('[Reconnected]')

    def on_disconnect(self):
        print('[Disconnected]')

    def handleMessage(self):
        print('observer_json_msg', args)


def scheduledAdvertiserScan():
    devices = scanner.scan(3.0)
    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for dev in devices:
        if (dev.scanData.get(255, None).encode("hex")[:28] == "ffff0123456789abcdefffffffff"):
            print "Device ID: %s, RSSI: %d dB" % (dev.scanData.get(255, None).encode("hex")[29:36], dev.rssi)
            print "BlueHat Data: %s" % dev.scanData.get(255, None).encode("hex")[37:]
    print "\n"


if __name__ == "__main__":
    socketIO = SocketIO('http://e41f2ed7.ngrok.io')
    bluehatObserver_socket = socketIO.define(BlueHatObserver, '/BlueHatObserver')
    bluehatObserver_socket.emit('observer_json_msg', {'xxx': 'yyy'})
    logging.basicConfig()
    scanner = Scanner()

    print 'Starting Observer Scan Scheduler!\n'
    scheduler = BlockingScheduler()
    scheduler.add_job(scheduledAdvertiserScan, 'interval', seconds = 5, id = 'advertiserScan', misfire_grace_time = 1)
    scheduler.start()
