'use strict';

/**
 * Author: Aravinth Panchadcharam
 * Email: me@aravinth.info
 * Date: 02/01/15.
 * Contributors:
 */


var app = require('express')();
var server = require('http').createServer(app);
var io = require('socket.io')(server);

app.get('/', function (req, res) {
	res.sendfile('index.html');
});

io.on('connection', function (socket) {
	socket.on('hola', function (msg) {
		console.log('message: ' + msg);
	});
});

server.listen(3000);
console.log("Listen");