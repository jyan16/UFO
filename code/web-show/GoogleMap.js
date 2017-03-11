function initMap() {
    var myLatLng = {lat: 40.78, lng: -97.21};

    // Create a map object and specify the DOM element for display.
    var map = new google.maps.Map(document.getElementById('map'), {
            center: myLatLng,
            scrollwheel: false,
            zoom: 4
        });

}
