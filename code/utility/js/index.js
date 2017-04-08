/**
 * Created by jinyan on 08/04/2017.
 */
$(document).ready(function(){
    $('#fake').click(function() {
        var year = '2011';
        $.get('/button', {year: year}, function(response) {
            console.log(response);
        });
    });
});