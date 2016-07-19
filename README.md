# crypto-geofence

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
inlat = (north - latitude) * (south-latitude)
```

The number would be negative for ```south < latitude < north```, and positive in any other
condition.  It would also be difficult to find north and south by factoring the result.
Unfortunately, multiplying encrypting numbers is not yet possible in Paillier Python
library.  I got this funny error:

<img src="http://i.imgur.com/Hipe0LB.png"/>

Anyway, you can get the same result by processing

```python
offset1 = (north - latitude) * random()
offset2 = (south - latitude) * random()
```

One of the offsets should be positive and the other negative, but the random factor makes
it difficult to figure out the true offset to the geofence. Combined with rate-limiting,
this could make your fence exta-secret.

### Going forward

I would like to calculate geofences for more complex shapes, but it doesn't look possible
to use the traditional point-in-polygon algorithm without knowing the actual coordinates!

## Libraries used

Using <a href="https://github.com/hardbyte/paillier.js">homomorphicjs</a> on the client,
and Australia NICTA's <a href="https://github.com/NICTA/python-paillier">Python-Paillier</a>
on the server

## License

MIT license
