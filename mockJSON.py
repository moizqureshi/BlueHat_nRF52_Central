from apscheduler.schedulers.background import BlockingScheduler
from socketIO_client import SocketIO, LoggingNamespace, BaseNamespace
import os
import logging
import requests
import json
import datetime

# logging.getLogger('requests').setLevel(logging.WARNING)
# logging.basicConfig(level=logging.DEBUG)

OBSERVER_ID = "1"
OBSERVER_LOCATION = "Location 1"
HOST = 'http://127.0.0.1/'
PORT = 8000
NAMESPACE = "/observer"

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
    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    json_data = {
        'observer_id':OBSERVER_ID,
        'observer_location':OBSERVER_LOCATION,
        'advertiser_id':'bbbbbbb',
        'rssi':-58,
        'data':'1234567c3'
    }
    print "Device ID: %s, RSSI: %d dB" % (json_data['advertiser_id'], json_data['rssi'])
    print "BlueHat Data: %s" % json_data['data']
    observer.emit('observer_json_msg', json_data)
    socketIO.wait(seconds=0.1)
    print('\n')


if __name__ == "__main__":
    print 'Starting Observer Scan Scheduler!\n'
    scheduler = BlockingScheduler()
    scheduler.add_job(scheduledAdvertiserScan, 'interval', seconds = 3, id = 'advertiserScan', misfire_grace_time = 1)
    scheduler.start()
