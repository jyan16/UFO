/**
 * Created by jinyan on 08/04/2017.
 */
$(document).ready(function(){
    $('#fake').click(function() {
        var year = '2017';
        var month = '04';
        var day = '01';
        var time = '10:00:00';
        var summary = 'heavy_reptile';
        var shape = 'circle';
        var city = 'providence';
        var state = 'RI';
        $.get('/button', {year: year, month: month, day: day, time: time, summary: summary,
                          shape: shape, city: city, state: state}, function(response) {
            console.log(summary)
            console.log(response);
        });
    });
});