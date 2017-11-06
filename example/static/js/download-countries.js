$(document).ready(function () {
  var countriesUrl = window.urls.countryList + '?format=csv';
  var signer = window.urls.signer;

  $('#download-countries').on('click', function (e) {
    e.preventDefault();
    console.log('Download button clicked, fetching signed URL');

    // Sign URL
    $.post(signer, {url: countriesUrl}).then(function (data) {
      console.log('Redirecting to ', data);
      window.location.assign(data);
    });
  });
});
