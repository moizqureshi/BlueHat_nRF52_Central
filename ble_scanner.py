from bluepy.btle import Scanner, DefaultDelegate
from apscheduler.schedulers.background import BlockingScheduler
from socketIO_client import SocketIO, LoggingNamespace, BaseNamespace
import logging
import requests
import json
import datetime
import threading
import time

logging.basicConfig()
# logging.getLogger('requests').setLevel(logging.WARNING)
# logging.basicConfig(level=logging.DEBUG)

HOST = 'http://0f0e739a.ngrok.io'
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
    print('\n')

def emitWorker(json_list):
    observer.emit('observer_json_msg', json.dumps(json_list))
    socketIO.wait(seconds=0.5)


socketIO = SocketIO(HOST, None)
observer = socketIO.define(Observer, NAMESPACE)
observer.on('on_server_response', on_server_response)
socketIO.wait(seconds=1)

scanner = Scanner()


def scheduledAdvertiserScan():
    start = time.time()
    devices = scanner.scan(3.0)
    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    json_list = []
    for dev in devices:
        json_data = {}
        uuid = dev.scanData.get(255, None).encode("hex")[:28]
        if (uuid is not None and uuid == "ffff0123456789abcdefffffffff"):
            json_data = {}
            deviceID = dev.scanData.get(255, None).encode("hex")[29:36]
            rssi = dev.rssi
            data = dev.scanData.get(255, None).encode("hex")[37:]
            json_data = {
                "DeviceID":deviceID,
                "RSSI":rssi,
                "Data":data
            }
            print "Device ID: %s, RSSI: %d dB" % (deviceID, rssi)
            print "BlueHat Data: %s" % data
        json_list.append(json_data)
    threading.Thread(name='emitWorker', target=emitWorker, args=(json_list,)).start()
    end = time.time()
    print(end-start)

if __name__ == "__main__":

    print 'Starting Observer Scan Scheduler!\n'
    scheduler = BlockingScheduler()
    scheduler.add_job(scheduledAdvertiserScan, 'interval', seconds = 5, id = 'advertiserScan', misfire_grace_time = 1)
    scheduler.start()
