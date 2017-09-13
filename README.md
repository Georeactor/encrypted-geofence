# crypto-geofence

[![Greenkeeper badge](https://badges.greenkeeper.io/Georeactor/crypto-geofence.svg)](https://greenkeeper.io/)

Is it possible for me to check if I'm inside a geofence, without revealing my location to
the server, and without the server giving me the true geofence?

## What is homomorphic encryption?

<a href="https://en.wikipedia.org/wiki/Homomorphic_encryption">Homomorphic encryption</a> is a new technique where you can perform arithmetic operations on
encrypted numbers.  It's possible with a few different algorithms, including the factoring-based one
used here (Paillier).  In the future it might be better to use a quantum-resistent algorithm
based on lattice cryptography.

If you send the encrypted numbers and a public key, another computer can perform arithmetic on
the number and scalar values without seeing the actual values.

## Applying it to Geofences

Encrypted coordinates and the public key are POSTed to the server

Originally I was hoping to find if you were in the box by testing this:

```python
latitude_offset = (north - latitude) * (south-latitude)
```

The number would be negative for ```south < latitude < north```, and positive in any other
condition.  It would also be difficult to find north and south by factoring the result.
Unfortunately, multiplying encrypting numbers is not possible in the Paillier
cryptosystem.  I got this funny error:

<img src="http://i.imgur.com/Hipe0LB.png"/>

Anyway, you can obfuscate offsets by multiplying by a random scalar instead:

```python
north_offset = (north - latitude) * random()
south_offset = (south - latitude) * random()
```

One of the offsets should be positive and the other negative, but the random factor makes
it difficult to figure out the true offset to the geofence. Combined with rate-limiting,
this could make your fence exta-secret.

### Going forward

I would like to:

- calculate geofences for more complex shapes, by breaking them into rectangles or triangles
- calculate distance, using a different cryptosystem which allows multiplication

## Libraries used

Using Brian Thorne's <a href="https://github.com/hardbyte/paillier.js">homomorphicjs</a> on the client,
and Australia NICTA's <a href="https://github.com/NICTA/python-paillier">Python-Paillier</a>
on the server

## License

MIT license
