// Accessor functions
function total(d) {
    // Return state's total number of UFO events by year
    return d.income;
}

function key(d) {
    // Return state's name
    return d.name;
}

// Chart dimensions
var margin = {top: 19.5, right: 19.5, bottom: 19.5, left: 39.5};
var width = 960 - margin.right;
var height = 700 - margin.top - margin.bottom;


// var color = d3.scaleThreshold()
//     .domain(d3.range(1, 9))
//     .range(d3.schemeBlues[9]);

//var color = d3.interpolateRgb(d3.rgb(198, 219, 239), d3.rgb(8, 48, 107));

// Create the SVG container and set the origin
var svg3 = d3.select("#chart_map_year_count").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Year label
var yearLabel3 = svg3.append("text")
                .attr("class", "year label")
                .attr("text-anchor", "end")
                .attr("x", width)
                .attr("y", height - 20)
                .text(1950);



// Load the data.
d3.json("statesPath.json", function(statesPath) {
	var state = svg3.append("g")
					.attr("class", "states")
					.selectAll()
					.data(statesPath)
					.enter()
					.append("g")
					.attr("class", "state")
					.append("path")
					.attr("class", function(d) {
						return "statePath 3" + d.id;
					})
					.attr("d",function(d){ return d.d;})
					.style("fill","white");

	d3.json("frequency_by_year.json", function(percentage) {
		// A bisector since many nation's data is sparsely-defined.
		// We provide this to make it easier to linearly interpolate between years.
		var bisect = d3.bisector(function(d) { return d[0]; });

		// Interpolates the dataset for the given (fractional) year.
		// function interpolateData(year) {
		// 	return totals.map(function(d) {
		// 	  return {
		// 	    name: d.state,
		// 	    income: interpolateValues(d.total, year),
		// 	  };
		// 	});
		// }

		function interpolateValues(values, year) {
			var i = bisect.left(values, year, 0, values.length - 1),
			    a = values[i];
			if (i > 0) {
			  var b = values[i - 1],
			      t = (year - a[0]) / (b[0] - a[0]);
			  return a[1] * (1 - t) + b[1] * t;
			}
			return a[1];
		}

		// Start a transition that interpolates the data based on year.
		svg3.transition()
		  .duration(30000)
		  .ease(d3.easeLinear)
		  .tween("year", tweenYear)


		// Tweens the entire chart by first tweening the year, and then the data.
		// For the interpolated data, the dots and label are redrawn.
		function tweenYear() {
			var year = d3.interpolateNumber(1950, 2016);
			return function(t) { 
			  	yearLabel.text(Math.round(year(t)));
				var percentageList = percentage[Math.round(year(t)) - 1950].frequency;
				for(var i = 0; i < percentageList.length; i++) {
					d3.select(".3" + percentageList[i][0])
					  .style("fill", function() {
					  		return d3.interpolateBlues(percentageList[i][1] * 2);
					  });

				}
			};
		}
	});
});

