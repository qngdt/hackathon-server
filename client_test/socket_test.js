import io from 'socket.io-client';

const socket = io('http://localhost:5000')

socket.emit('channel1', 'Hi server');
socket.on('channel1', (data) => {
    console.log('Data recieved from server', data); //this will console 'channel 2'
});
