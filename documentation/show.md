## Introduction
### Part 1
Our project focus on finding correlations between UFO sighting reports and other source of information, such as geometry, weather, population and area data.

### Part 2
We collect our data from four different data sources --- UFO report data from NUFORC, national UFO Report Center, Geometry data from Google Map, weather data from Darksky, and population and area data from United States Census. Several ways are used to collect data, and we finally build a database for them.

### Part 3
Based on our data, we first do some statistic analysis. These statistic results are integrated into website. _**Show demo**_
We can see that most sightings occur at night, no matter clear or cloudy. This figure shows how the sighting number varies with year. We can see that it increases as a whole, while decreased a little bit recently. Figure 5 shows the correlation between population, year and sighting number. We use 4 degree polynomial regression to fit UFO sighting number with year and population. The result is good, and this model predicts about 5500 sightings in 2017.

### Part 4
This map shows the cumulative distribution around U.S. As you can see, california reports more sightings than other states, as well as Texas, Washington and Florida. The abundance of reports might due to their geography condition --- desert and sea. These statistic results are integrated into website.

### Part 5
Furthermore, we use machine learning to detect fake reports. We use logistic regression and decision treeto process summary data, and rbf kernel SVM and decision tree to check numeric data. All these classifiers vote in average to give out final grade of user reports. We also build a user interface lets users to submit their reports, while giving feedback based on our models. **Show demo** 