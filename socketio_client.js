//client.js
var io = require('socket.io-client');
var socket = io.connect('http://localhost:5000', {reconnect: true});

// Add a connect listener
socket.on('connect', function (socket) {
    console.log('Connected!');
});

socket.on('bluehat_server_response', function(data) {
  console.log(data);
});

var json_data = {
      'observer_id':"1",
      'observer_location':"Location1",
      'advertiser_id':'bbbbbbb',
      'rssi':-58,
      'data':'1234567c3'
  }

socket.emit('observer_json_msg', json_data);
