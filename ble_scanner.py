from bluepy.btle import Scanner, DefaultDelegate
from apscheduler.schedulers.background import BlockingScheduler
from socketIO_client import SocketIO, LoggingNamespace, BaseNamespace
import logging
import requests
import json
import datetime

logging.getLogger('requests').setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)

HOST = 'http://127.0.0.1/'
PORT = 8000
NAMESPACE = "/observer"

OBSERVER_ID = "1"
OBSERVER_LOCATION = "Location 1"

class Observer(BaseNamespace):
    def on_connect(self):
        print('Device: Connected from BlueHat Server')

    def on_disconnect(self):
        print('Device: Disconnected from BlueHat Server')

def on_server_response(*args):
    print('BlueHat Server Response: ', args)

socketIO = SocketIO(HOST, PORT)
observer = socketIO.define(Observer, NAMESPACE)
observer.on('on_server_response', on_server_response)
socketIO.wait(seconds=1)


def scheduledAdvertiserScan():
    devices = scanner.scan(2.0)
    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for dev in devices:
        if (dev.scanData.get(255, None).encode("hex")[:28] == "ffff0123456789abcdefffffffff"):
            print "Device ID: %s, RSSI: %d dB" % (dev.scanData.get(255, None).encode("hex")[29:36], dev.rssi)
            print "BlueHat Data: %s" % dev.scanData.get(255, None).encode("hex")[37:]
    print "\n"
    observer.emit('observer_json_msg', json_data)
    socketIO.wait(seconds=0.5)


if __name__ == "__main__":
    print 'Starting Observer Scan Scheduler!\n'
    scheduler = BlockingScheduler()
    scheduler.add_job(scheduledAdvertiserScan, 'interval', seconds = 5, id = 'advertiserScan', misfire_grace_time = 1)
    scheduler.start()
