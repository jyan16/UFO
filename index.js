
var express = require('express')
var any_db = require('any-db')
var engines = require('consolidate')

var app = express();

app.engine('html', engines.hogan);
app.set('views', __dirname + '/web-show');
app.set('view engine', 'html'); 
app.use(express.static('js'));

var anyDB = require('any-db');
var conn = anyDB.createConnection('sqlite3://data/my_ufo.db');
  app.get('/', function(request, response){
      console.log('- Request received:', request.method.cyan, request.url.underline);
      response.render('GoogleMap.html');
  });
  app.get('/test', function(request, response){
  	  
  	  var q = conn.query('SELECT * FROM events', function(error, d) {
		 var messages = d.rows;
  	  	 response.json(messages);
	  });

  });
// your app's code here



app.listen(8080);





