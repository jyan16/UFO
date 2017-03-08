# Introduction

  There are many UFO reports across the United States categorized by event date, state, shape of UFO and date posted.Our project tends to analyze correlation between UFO reports and other data, like GIS and weather. Our project tends to analyze correlation between UFO reports and other data, like GIS and weather.

# Questions of interest

  1. How can we predict when and where UFO will appear, and the trend of its occurrence? 
  2. With so many UFO reports, how can we figure out which of these UFO reports are fake? 
  3. Are there any relationships between UFOs features or characteristics with corresponding weather or GIS information?
  
# Data structure

  data source: The National UFO Reporting Center Online Database (http://www.nuforc.org/webreports.html)
  
        ![Data structure](https://github.com/jyan16/UFO/blob/master/img/data%20structure.png)
        
# Method & Technology

  To clean UFO-report data, we plan to drop the witness data too early, because of the lack of weather data and the change of geography circumstance. 

	Predicting about UFO needs correlation of many sources of data, including the UFO-report data, geography information, and the weather. UFO Reports is the basic data of our system. There are 5 steps regarding our data: 
	1). Creating database of GIS, UFO-Reports and weather.	
  2). Using NLP technology to analyze summary data in the UFO Reports data. To extract features about UFO. Creating chart (style, color, characteristics) of UFO. 
  3). Indexed by date and location data of UFO Reports, scraping the corresponding GIS and weather data, and integrating them together. 
	4). Using machine-learning or neural network to train our data, figure out patterns and correlation between UFO witness with GIS and weather at that time. 
	5). Combining the information entered by user and weather forecasting data to do prediction In order to predict the possibility to see an UFO in the future. 
  
	We will use SQLite to store our data. We will create a system based in python that does Natural Language Processing, Classification and generating statistical results. With UFO-witness summaries, we are able to extract high probability features of UFO occurrence, such as shape, color, movement, brightness. We would then use these data to generate charts of all documented UFO characteristics. With time, location and weather data we could used to predict future events of UFO. By user inputting desired destination, time and weather condition, our system will generate a probability one would encounter UFO appearance. We will also build an interactive front-end for users to change parameters and see results.
  
