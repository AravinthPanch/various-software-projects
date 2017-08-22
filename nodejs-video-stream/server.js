var http = require('http');
var fs = require('fs');

http.createServer(function (req, res) {

//    var path = 'sample.ogv';
    var path = '/Users/Aravinth/Movies/big_buck_bunny_1080p_stereo.ogg';

    var stat = fs.statSync(path);

    var total = stat.size;

    if (req.headers['range']) {

        var range = req.headers.range;

        var parts = range.replace(/bytes=/, "").split("-");

        var partialstart = parts[0];

        var partialend = parts[1];

        var start = parseInt(partialstart, 10);

        var end = partialend ? parseInt(partialend, 10) : total - 1;

        var chunksize = (end - start) + 1;

        console.log('RANGE: ' + start + ' - ' + end + ' = ' + chunksize);

        var file = fs.createReadStream(path, {start: start, end: end});

        res.writeHead(206, { 'Content-Range': 'bytes ' + start + '-' + end + '/' + total, 'Accept-Ranges': 'bytes', 'Content-Length': chunksize, 'Content-Type': 'video/ogg', 'Access-Control-Allow-Origin': '*' });

        file.pipe(res);

    } else {
        console.log('ALL: ' + total);

        res.writeHead(200, { 'Content-Length': total, 'Content-Type': 'video/ogg' });

        fs.createReadStream(path).pipe(res);
    }

}).listen(8080);

console.log('Video Stream Server is running at 8080');


var connect = require('connect');

connect()
    .use(connect.static(__dirname))
    .listen(8000);

console.log('Web Server is running at 8000');