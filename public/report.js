/**
 * Created by jinyan on 10/04/2017.
 */
$(document).ready(function(){
    $('#fake').click(function() {
        //get report information

        var year = document.getElementById("year").value;
        var month = document.getElementById("month").value;
        var day = document.getElementById("day").value;
        var time = document.getElementById("time").value;
        var summary = document.getElementById("summary").value;
        var shape = document.getElementById("shape").value;
        var city = document.getElementById("city").value;
        var state = document.getElementById("state").value;
        $.get('/submit', {year: year, month: month, day: day, time: time, summary: summary,
            shape: shape, city: city, state: state}, function(response) {
            document.getElementById("result").value = response;

        });
    });
});