$(document).ready(function () {
  var apiUrl = window.urls.countryList;
  var fields = [
    'country_name',
    'continent_name',
    'capital',
    'area_in_sq_km',
    'population'
  ];

  var $next = $('#next');
  var $prev = $('#prev');
  // Fetch data to load table
  function getData(url) {
    $.ajax({
      url: url,
      type: 'GET',
    }).then(function (data) {
      $next.toggleClass('disabled', !data.next);
      $next.data('url', data.next);

      $prev.toggleClass('disabled', !data.previous);
      $prev.data('url', data.previous);

      var els = $.map(data.results, function (obj) {
        var tr = $('<tr>');
        $.each(fields, function (idx, field) {
          var td = $('<td>');
          td.html(obj[field]);
          $(tr).append(td);
        });
        return tr;
      });
      $('#table-data').html(els);
    });
  };

  $next.on('click', function (e) {
    e.preventDefault();
    var url = $next.data('url');
    if (!url) {
      return;
    }
    getData(url);
  });

  $prev.on('click', function (e) {
    e.preventDefault();
    var url = $prev.data('url');
    if (!url) {
      return;
    }
    getData(url);
  })

  getData(apiUrl);
});


