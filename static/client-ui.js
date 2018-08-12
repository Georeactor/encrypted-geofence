var kp = phe.generate_paillier_keypair(1024);
$('#key').text(JSON.stringify(kp.public_key));

$('button').prop('disabled', false).click(function(e) {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var latitude = Math.round(position.coords.latitude * 1000);
      var longitude = Math.round(position.coords.longitude * 1000);

      latitude = Math.round(39.7645183 * 1000);
      longitude = Math.round(-104.9955397 * 1000);

      $('#clientgeo').text((latitude / 1000) + ', ' + (longitude / 1000));
      latitude = kp.public_key.raw_encrypt((latitude + 90000) + '');
      longitude = kp.public_key.raw_encrypt((longitude + 180000) + '');

      $('#encryptlat').text(latitude);
      $('#encryptlng').text(longitude);

      $.get('/calculate', {
        g: kp.public_key.g.toString(),
        n: kp.public_key.n.toString(),
        lat: latitude.toString(),
        lng: longitude.toString()
      }, function (response) {
        response = JSON.parse(response);
        $('#response').text(JSON.stringify(response));

        var lat1 = kp.private_key.raw_decrypt(response.lat);
        var lat2 = kp.private_key.raw_decrypt(response.lat2);
        var lng1 = kp.private_key.raw_decrypt(response.lng);
        var lng2 = kp.private_key.raw_decrypt(response.lng2);

        var ymatch = (Math.log(lat1) > 50 && Math.log(lat2) < 50) || (Math.log(lat1) < 50 && Math.log(lat2) > 50);
        var xmatch = (Math.log(lng1) > 50 && Math.log(lng2) < 50) || (Math.log(lng1) < 50 && Math.log(lng2) > 50);

        var gotit = '';
        if (xmatch && ymatch) {
          gotit = "<h1>You're in Colorado!</h1>";
        } else if (xmatch) {
          gotit = '<strong>Inside the longitude bounds, but not latitude</strong>';
        } else if (ymatch) {
          gotit = '<strong>Inside the latitude bounds, but not longitude</strong>';
        } else {
          gotit = '<strong>Not in lat or lng bounds :( </strong>';
        }
        $('#result').html(gotit);
      });
    },
    function (error) {
      alert('Error: ' + JSON.stringify(error));
    });
  } else {
    alert('geolocation not possible');
  }
});
