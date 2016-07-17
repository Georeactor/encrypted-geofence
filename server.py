# server.py

import os, re, json
import flask
from flask import request
from phe import paillier

app = flask.Flask(__name__)

# colorado geo fence
# xmin, ymin, xmax, ymax // west, south, east, north
# * 1000
geobox = [102052, 36971, 109190, 41.01]

@app.route('/')
def print_index():
    return open('./index.html', 'r').read()

@app.route('/calculate')
def calculate_geo():
    # rebuild public key
    g = int(request.args.get('g'))
    n = int(request.args.get('n'))
    print('got pubkey 1')
    pubkey = paillier.PaillierPublicKey(g=g, n=n)
    print('got pubkey 2')

    lat = paillier.EncryptedNumber(pubkey, int(request.args.get('lat')), 1)
    lng = paillier.EncryptedNumber(pubkey, int(request.args.get('lng')), 1)
    print('got lat/lng')

    west = pubkey.encrypt(geobox[0])
    south = pubkey.encrypt(geobox[1])
    east = pubkey.encrypt(geobox[2])
    north = pubkey.encrypt(geobox[3])
    print ('got geo box')

    latoffset = (south - lat)
    latoffset2 = (north - lat)
    lngoffset = (west - lng)
    lngoffset2 = (east - lng)

    print ('made offsets')

    return json.dumps({
      "lat": latoffset.ciphertext(),
      "latex": latoffset.exponent,
      "lat2": latoffset2.ciphertext(),
      "lat2ex": latoffset2.exponent,
      "lng": lngoffset.ciphertext(),
      "lngex": lngoffset.exponent,
      "lng2": lngoffset2.ciphertext(),
      "lng2ex": lngoffset2.exponent
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
