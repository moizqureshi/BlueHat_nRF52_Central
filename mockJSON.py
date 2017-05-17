from apscheduler.schedulers.background import BlockingScheduler
from socketIO_client import SocketIO, LoggingNamespace, BaseNamespace
from execjs import get
import os
import logging
import requests
import json
import datetime


OBSERVER_ID = "1"
OBSERVER_LOCATION = "Location 1"

class Observer(BaseNamespace):
    def on_connect(self):
        print('Device: Connected to BlueHat Server')

    def on_disconnect(self):
        print('Device: Disconnected from BlueHat Server')

def on_server_response(self, *args):
    print('BlueHat Server Response: ', args)

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
    socketIO.emit('observer_json_msg', json_data)
    socketIO.wait(seconds=0.25)
    print('\n')


if __name__ == "__main__":
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.basicConfig(level=logging.DEBUG)

    print('Connecting to BlueHat SocketIO Server')
    socketIO = SocketIO('http://127.0.0.1', 5000, Observer)
    socketIO = socketIO.define(Observer, '/Observer')
    # socketIO.on('connect', thisObserver.on_connect)
    # socketIO.on('disconnect', thisObserver.on_disconnect)
    socketIO.on('observer_json_msg', on_server_response)

    print 'Starting Observer Scan Scheduler!\n'
    scheduler = BlockingScheduler()
    scheduler.add_job(scheduledAdvertiserScan, 'interval', seconds = 3, id = 'advertiserScan', misfire_grace_time = 1)
    scheduler.start()
