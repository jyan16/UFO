
var express = require('express'); //build server framework
var engines = require('consolidate'); //send html like a file, not a string
var exec = require('child_process').exec;
var app = express();

// setting app
app.engine('html', engines.hogan); // since items on html can change, we need to interpret html in another way, say hogan
app.set('views', __dirname + '/code/views'); //directory of html
app.set('view engine', 'html');
app.use('code/utility', express.static('public'));

app.get('/', function (request, response) {
    response.render('index.html');
});

app.get('/button', function(request, response) {
   var year = request.query.year;
   exec('python3 code/interactive/detect_fake.py -year ' + year, function(error, stdout, stderr) {

      console.log('fuck');
      //console.log(stdout);
      response.json(stdout);
      if (error) {
         console.log('stderr' + stderr);
      }
   });
});



app.listen(8080);





