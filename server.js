var express = require('express'); //build server framework
var engines = require('consolidate'); //send html like a file, not a string
var exec = require('child_process').exec;
var app = express();

// setting app
app.engine('html', engines.hogan); // since items on html can change, we need to interpret html in another way, say hogan
app.set('views', __dirname + '/code/views'); //directory of html
app.set('view engine', 'html');
app.use(express.static('public'));

var sqlite3 = require('any-db');
var conn = sqlite3.createConnection('sqlite3://data/my_ufo.db');

//visit home html
app.get('/', function (request, response) {
    response.render('index.html');
});
app.get('/final_report', function (request, response) {
    response.sendFile(__dirname + '/docs/final_report.pdf');
});

//visit report html
app.get('/report', function (request, response) {
   response.render('report.html');

});

//submit report and decide whether it is true
app.get('/submit', function(request, response) {
   var data = request.query;
   var summary = data.summary.split(' ').join('_');
   var city = data.city.split(' ').join('_')
   var execute = 'python3 code/interactive/fake_detection.py -d ' + data.date + ' -t ' + data.time +
                 ' -sum ' + summary + ' -shape ' + data.shape + ' -c ' + city + ' -s ' + data.state;
   exec(execute, function(error, stdout, stderr) {
      response.json(stdout);
      if (error) {
         console.log('stderr' + stderr);
      }
   });
});

//show google map for user
app.get('/google', function(request, response) {
   response.sendFile(__dirname + '/data/json/report_show.json');

});

//show database
app.get('/datapage', function(request, response) {
    response.render('database.html');
});

app.get('/database_event', function(request, response) {
    conn.query('SELECT month, day, icon, city, state, shape, e.summary' +
        ' FROM events e, weathers w WHERE e.year=2017 and e.label=1 and e.event_id=w.event_id', function(err, data) {
        response.json(data);
    })
});
app.get('/database_state', function(request, response) {
    conn.query('SELECT p.state, area, population FROM populations p, areas a WHERE p.year=2016 and p.state=a.state', function(err, data) {
        response.json(data);
    })
});
//show statistic page
app.get('/statistic', function(request, response) {
    response.render('statistic.html');
});

//get statistic data for d3 graph
app.get('/statistic_data', function(request, response) {
    response.sendFile(__dirname + '/data/json/statistic_data.json');
});

// get states path to draw d3 map
app.get('/us-states', function(request, response) {
    response.sendFile(__dirname + '/data/json/us-states.json');
});

app.listen(8080);





