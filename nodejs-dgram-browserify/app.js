'use strict';

/**
 * Author: Aravinth Panchadcharam
 * Email: me@aravinth.info
 * Date: 02/01/15.
 * Contributors:
 */

var PORT = 50006;
var HOST = 'localhost';

var dgram = require('dgram');
var server = dgram.createSocket('udp4');

server.on('listening', function () {
	var address = server.address();
	console.log('UDP Server listening on ' + address.address + ":" + address.port);
});

server.on('message', function (message, remote) {
	console.log(remote.address + ':' + remote.port + ' - ' + message);
	socket.io.emit('client', {
		skeleton: message
	});
});

server.bind(PORT, HOST);