var express = require('express');
var bodyParser = require('body-parser');
var fs = require('fs');

var serverConnect = function () {
  var serverPort = 51434;

  var app = express();

  app.use(express.static('public'));
  app.use(bodyParser.json());
  app.use(bodyParser.urlencoded({ extended: false }));
  app.engine('html', require('ejs').renderFile);

  app.use((request, response) => {
    var url = request.url;
    if (request.url == '/favicon.ico') {
      response.writeHead(404);
      response.end();
      return;
    }
    response.writeHead(200);
    console.log(__dirname, url);
    response.end(fs.readFileSync(__dirname + "\\aaa.html"));
  });

  // index handling ###문제 있음
  app.get('/aaa.html', (req, res) => {
    res.render('/aaa.html');
  });

  // favicon (returns 404)
  app.get('/favicon.ico', (req, res) => { 
    res.writeHead(404);
    res.end();
  });

  // post handling
  app.post('/postTest', (req,res) => {

  });

  app.listen(serverPort, () => {
    console.log(`server running at ${serverPort}\n`);
  });
}

module.exports.serverConnect = serverConnect;