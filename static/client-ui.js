var kp = phe.generate_paillier_keypair(128);
$('#key').text(JSON.stringify(kp.public_key));

$('button').prop('disabled', false).click(function(e) {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var latitude = Math.round(position.coords.latitude * 1000);
      var longitude = Math.round(position.coords.longitude * -1000);
      $('#clientgeo').text((latitude / 1000) + ', ' + (longitude / -1000));
      latitude = kp.public_key.raw_encrypt(latitude + '');
      longitude = kp.public_key.raw_encrypt(longitude + '');

      $('#encryptlat').text(latitude);
      $('#encryptlng').text(longitude);

      $.get('/calculate', {
        g: kp.public_key.g.toString(),
        n: kp.public_key.n.toString(),
        lat: latitude.toString(),
        lng: longitude.toString()
      }, function (response) {
        console.log(response);
      });
    },
    function (error) {
      alert('Error: ' + JSON.stringify(error));
    });
  } else {
    alert('geolocation not possible');
  }
});
