# server.py

import os, re, json
import flask
from flask import request
from phe import paillier
from random import random
from vectors import Vec2, dot_product

app = flask.Flask(__name__)

# colorado geo fence
# xmin, ymin, xmax, ymax // west, south, east, north
# deg * 1000 units
# add 90 deg to north/south
# add 180 deg to east/west
geobox = [-109190 + 180000, 36971 + 90000, -102052 + 180000, 41010 + 90000]

@app.route('/')
def print_index():
    return open('./index.html', 'r').read()

@app.route('/calculate')
def calculate_geo():
    # rebuild public key
    g = int(request.args.get('g'))
    n = int(request.args.get('n'))
    # g is n+1 on both sides
    pubkey = paillier.PaillierPublicKey(n=n)

    # load the coordinates as EncryptedNumber type
    lat = paillier.EncryptedNumber(pubkey, int(request.args.get('lat')))
    lng = paillier.EncryptedNumber(pubkey, int(request.args.get('lng')))

    # use same key to encrypt the geobox
    west = pubkey.encrypt(geobox[0])
    south = pubkey.encrypt(geobox[1])
    east = pubkey.encrypt(geobox[2])
    north = pubkey.encrypt(geobox[3])

    latoffset = (south - lat) * random()
    latoffset2 = (north - lat) * random()
    lngoffset = (west - lng) * random()
    lngoffset2 = (east - lng) * random()

    return json.dumps({
      "lat": str(latoffset.ciphertext()),
      "lat2": str(latoffset2.ciphertext()),
      "lng": str(lngoffset.ciphertext()),
      "lng2": str(lngoffset2.ciphertext()),
    })

@app.route('/calculate_rotated')
def calculate_rotated():
    # rebuild public key
    g = int(request.args.get('g'))
    n = int(request.args.get('n'))
    # g = n+1 in the used implementation
    pubkey = paillier.PaillierPublicKey(n=n)

    # load the coordinate P(lat|lng) as EncryptedNumbers
    P_lat = paillier.EncryptedNumber(pubkey, int(request.args.get('lat')))
    P_lng = paillier.EncryptedNumber(pubkey, int(request.args.get('lng')))

    # calculate values
    # E(AP*AB), AB**2, E(AP*AD), AD**2
    A = Vec2(geobox[1], geobox[0])
    B = Vec2(geobox[1], geobox[2])
    C = Vec2(geobox[3], geobox[2])
    D = Vec2(geobox[3], geobox[0])

    AB = B - A
    AD = D - A

    e_A_lat = pubkey.encrypt(A.x)
    e_A_lng = pubkey.encrypt(A.y)
    e_B_lat = pubkey.encrypt(B.x)
    e_B_lng = pubkey.encrypt(B.y)

    e_AP_lat = P_lat - e_A_lat
    e_AP_lng = P_lng - e_A_lng

    e_AP_dot_AB = (e_AP_lat * AB.x) + (e_AP_lng * AB.y)
    e_AP_dot_AD = (e_AP_lat * AD.x) + (e_AP_lng * AD.y)

    sq_AB = dot_product(AB, AB)
    sq_AD = dot_product(AD, AD)

    return json.dumps({
        "e_AP_dot_AB": str(e_AP_dot_AB.ciphertext()),
        "sq_AB": str(sq_AB),
        "e_AP_dot_AD": str(e_AP_dot_AD.ciphertext()),
        "sq_AD": str(sq_AD)
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
