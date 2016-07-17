const fs = require('fs');
const bn = require('jsbn');
const phe = require('homomorphicjs');

// generate key if it doesn't exist
var key;
try {
  key = require('./key.json');
} catch(e) {
  key = phe.generate_paillier_keypair(128);
  fs.writeFile('./key.json', JSON.stringify(key), function (err) {
    if (err) {
      throw err;
    }
  });
}

module.exports = function (box, g, n, lat, lng, callback) {
  console.log(g);
  console.log(n);
  var public_key = new phe.PublicKey(new bn(g), new bn(n));

  console.log(public_key);

  var xmin = Math.round(box[0] * 1000);
  var ymin = Math.round(box[1] * 1000);
  var xmax = Math.round(box[2] * 1000);
  var ymax = Math.round(box[3] * 1000);

  console.log('coords');

  xmin = public_key.raw_encrypt(xmin);
  ymin = public_key.raw_encrypt(ymin);
  xmax = public_key.raw_encrypt(xmax);
  ymax = public_key.raw_encrupt(ymax);

  console.log('encrypted box');
 
  var lat = new bn(lat);
  var latoffset1 = lat.subtract(ymin);
  var latoffset2 = lat.subtract(ymax);

  var lng = new bn(lng);
  var lngoffset1 = lat.subtract(xmin);
  var lngoffset2 = lat.subtract(xmax);
 
  callback(null, {
    lat: [latoffset1, latoffset2],
    lng: [lngoffset1, lngoffset2]
  });
};
