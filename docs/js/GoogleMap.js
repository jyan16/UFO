function initMap() {
    var myLatLng = {lat: 40.78, lng: -97.21};
    
    // Create a map object and specify the DOM element for display.
    var map = new google.maps.Map(document.getElementById('map'), {
      center: myLatLng,
      scrollwheel: false,
      zoom: 4
    });

    d3.csv("data/file_ufo_lat.csv", function(data) {
      //console.log(data);

      var LatLng = [];
      for (var i = 0; i < data.length; i ++) {
        if (data[i].year == "2017") {
          var item = [data[i].lat, data[i].lng];
          //console.log(item);  
          LatLng.push(item); 
        }
      };

      //console.log(LatLng);
      res = [];   
      for (var i = 0; i < LatLng.length; i++) {
        var lat = LatLng[i][0];
        var lng = LatLng[i][1];
        var item = new google.maps.LatLng(lat, lng);
        //console.log(LatLng[i][0]);
        //console.log(LatLng[i][1]);
        //console.log(item);
        res.push(item);
      }
      //console.log(res);

      var heatmap = new google.maps.visualization.HeatmapLayer({
        data: res,
        map: map
      });

    });
}
