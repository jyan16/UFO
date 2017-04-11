
var express = require('express'); //build server framework
var engines = require('consolidate'); //send html like a file, not a string
var exec = require('child_process').exec;
var app = express();


// setting app
app.engine('html', engines.hogan); // since items on html can change, we need to interpret html in another way, say hogan
app.set('views', __dirname + '/code/views'); //directory of html
app.set('view engine', 'html');
app.use(express.static('public'));

//visit home html
app.get('/', function (request, response) {
    response.render('index.html');
});

//visit report html
app.get('/report', function (request, response) {
   response.render('report.html');

});

//submit report and decide whether it is true
app.get('/submit', function(request, response) {
   console.log(request.query);
   var data = request.query;
   var execute = 'python3 code/interactive/fake_detection.py -d ' + data.date + ' -t ' + data.time +
                 ' -sum ' + data.summary + ' -shape ' + data.shape + ' -c ' + data.city + ' -s ' + data.state;
   exec(execute, function(error, stdout, stderr) {
      response.json(stdout);
      if (error) {
         console.log('stderr' + stderr);
      }
   });
});

app.listen(8080);





