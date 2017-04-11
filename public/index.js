/**
 * Created by jinyan on 08/04/2017.
 */
$(document).ready(function(){
    $('#report').click(function() {
        $.get('/report',{}, function(response) {
            console.log(response);
        });
    });
});