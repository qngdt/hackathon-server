
const io = require('socket.io-client');

const socket = io('http://192.168.10.109:5000');

socket.on('connect', function () { console.log('connect!') });
socket.on('msg', (data) => {
    console.log('Data recieved from server', data); //this will console 'channel 2'
});

socket.emit('data', 'Hi server');
