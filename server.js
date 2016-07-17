const fs = require('fs');
const http = require('http');
const url = require('url');

const geofence = require('./index.js');

// secret geo fence
const xmin = -109.1903257;
const xmax = -102.0516883;
const ymin = 36.9710536;
const ymax = 41.0095746;
const geobox = [xmin, ymin, xmax, ymax];

// http server
const index_html = fs.readFileSync('./index.html');
const js_lib = fs.readFileSync('./client-crypto.js');

const port = process.env.PORT || 3000;
const requestHandler = (request, response) => {
  console.log(request.url);
  console.log(request.body);

  if (request.url.indexOf('/calculate') === 0) {
    var realurl = url.parse(request.url, true);
    var g = realurl.query.g;
    var n = realurl.query.n;
    var lat = realurl.query.lat;
    var lng = realurl.query.lng;
    request.url = '/calculate';
  }

  switch (request.url) {
    case '/':
      return response.end(index_html);

    case '/clientlib':
      return response.end(js_lib);

    case '/calculate':
      var verdict = geofence(geobox, g, n, lat, lng, function (err, verdict) {
        response.end(JSON.stringify(verdict));
      });
      break;

    default:
      response.end('action not found');
      break;
  }
};

const server = http.createServer(requestHandler);
server.listen(port, (err) => {
  console.log('server is live');
  if (err) {
    throw err;
  }
});
