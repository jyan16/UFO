var map, heatmap;

function initMap() {
    var myLatLng = {lat: 40.78, lng: -97.21};

    // Create a map object and specify the DOM element for display.
    map = new google.maps.Map(document.getElementById('map'), {
            center: myLatLng,
            scrollwheel: false,
            zoom: 4
    });
    heatmap = new google.maps.visualization.HeatmapLayer({
    		data: getPoints(),
    		map: map
  	});

  	function getPoints() {
  		return [
  			new google.maps.LatLng(37.782551, -122.445368)
  		]
  	};
}
