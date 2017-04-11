
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
   console.log('fuck!!!123')
   response.render('report.html');

})

//submit report and decide whether it is true
app.get('/submit', function(request, response) {
   var year = request.query.year;
   var month = request.query.month;
   var day = request.query.day;
   var time = request.query.time;
   var summary = request.query.summary;
   var shape = request.query.shape;
   var city = request.query.city;
   var state = request.query.state;
   var execute = 'python3 code/interactive/fake_detection.py -y ' + year + ' -m ' + month + ' -d' + day
                 + ' -t ' + time + ' -sum ' + summary + ' -shape ' + shape + ' -c ' + city + ' -s ' + state;
   exec(execute, function(error, stdout, stderr) {
      response.json(stdout);
      if (error) {
         console.log('stderr' + stderr);
      }
   });
});

app.listen(8080);





