from apscheduler.schedulers.background import BlockingScheduler
from socketIO_client import SocketIO, LoggingNamespace
import logging
import requests
import json
import datetime

OBSERVER_ID = "1"
OBSERVER_LOCATION = "Location 1"

def on_connect():
    print('Device: Connected to BlueHat Server')

def on_disconnect():
    print('Device: Disconnected from BlueHat Server')

def on_server_response(*args):
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
    socketIO.emit('observer_json_msg', json_data, on_server_response)
    print "Device ID: %s, RSSI: %d dB" % (json_data['advertiser_id'], json_data['rssi'])
    print "BlueHat Data: %s" % json_data['data']
    print "\n"

if __name__ == "__main__":
    logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
    logging.basicConfig()

    print('Connecting to BlueHat SocketIO Server')
    socketIO = SocketIO('http://127.0.0.1', 8000)
    socketIO.on('bluehat_server_response', on_server_response)

    print 'Starting Observer Scan Scheduler!\n'
    scheduler = BlockingScheduler()
    scheduler.add_job(scheduledAdvertiserScan, 'interval', seconds = 3, id = 'advertiserScan', misfire_grace_time = 1)
    scheduler.start()
