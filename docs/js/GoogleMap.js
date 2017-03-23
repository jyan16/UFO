//$(document).ready(function() {
  
  //var year = 2017;

  //initMap();

  // $('.btn').click(function() {

  //   $('#map').empty();
  //   if (year == 1984) {
  //     year = 2017;
  //   }
  //   else {
  //     year = year - 1;
  //   }
  //   initMap(year);
  //   $('.btn').html = 'Year: ';
  //   console.log(year);
  // });

//});  

function initMap() {
    var myLatLng = {lat: 40.78, lng: -97.21};
    
    // Create a map object and specify the DOM element for display.
    var map = new google.maps.Map(document.getElementById('map'), {
      center: myLatLng,
      scrollwheel: false,
      zoom: 4
    });

    d3.json("lat_lng_google.json", function(data) {
      //console.log(data);

      var res = [];   
      for (var i = 0; i < data.length; i ++) {
        
          var LatLng = data[i].position;
          //console.log(item);
          for (var j = 0; j < LatLng.length; j++) {
            var lat = LatLng[j][0];
            var lng = LatLng[j][1];
            var item = new google.maps.LatLng(lat, lng);
            res.push(item);

          }  

      };
      //console.log(res);
      console.log(res.length);

      var heatmap = new google.maps.visualization.HeatmapLayer({
        data: res,
        map: map
      });

    });
};
