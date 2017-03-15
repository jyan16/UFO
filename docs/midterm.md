### [Return to Home Page](https://jyan16.github.io/UFO/)

# Introduction

We collect UFO reports data from website http://www.nuforc.org/, GIS data from Google’s API https://maps.googleapis.com/maps/api/geocode/ and weather data from https://darksky.net/.

After data cleaning, UFO reports data has eight columns: event_id, time, city, state, shape, duration, summary and location_id.
Here’s a glimpse of our UFO reports data stored as CSV file:
![UFO Reports Data](https://github.com/jyan16/UFO/blob/master/docs/img/ufo_reports_data.png)

GIS data has five columns: location_id, city, state, lat and lng.
Here’s a glimpse of our GIS data stored as CSV file:
![Geography Data](https://github.com/jyan16/UFO/blob/master/docs/img/geography_data.png)

Weather data has eleven columns: event_id, summary, icon, temperature, apparentTemp, dewPoint, humidity, windSpeed, windBearing, visibility and pressure.
Here’s a glimpse of our weather data stored as CSV file:
![Weather Data](https://github.com/jyan16/UFO/blob/master/docs/img/weather_data.png)

For the convenience of data analyzing, we create a relational database “my_ufo.db” which has two tables “events” and “weathers”.
	Here’s the schema of the two tables:
	events(event_id:int, year:int, month:int, day:int, time:text, city:text, state:text, shape:text, duration:text, summary:text, lat:float, lng:float)
	weathers(event_id:int, summary:text, icon:text, temperature:float, apparentTemperature:float, dewPoint:float, humidity:float, windSpeed:float, windBearing:int, visibility:float, pressure:float)

	We are investigating into the relationship of UFOs features or characteristics with corresponding weather or GIS information and probably predicting the occurrence of UFO at certain location and time. Thus we make use of Google heat map to show the distribution of UFO witnesses of a certain year.
	For example below is a heat map of UFO reports across United States in 2016:
