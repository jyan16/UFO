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
var width = 700 - margin.right;
var height = 600 - margin.top - margin.bottom;


// var color = d3.scaleThreshold()
//     .domain(d3.range(1, 9))
//     .range(d3.schemeBlues[9]);

//var color = d3.interpolateRgb(d3.rgb(198, 219, 239), d3.rgb(8, 48, 107));

// Create the SVG container and set the origin
var svg = d3.select("#chart_map_year_count").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Year label
var yearLabel = svg.append("text")
                .attr("class", "year label")
                .attr("text-anchor", "end")
                .attr("x", width)
                .attr("y", height - 20)
                .text(1954);



// Load the data.
d3.json("/data/statesPath.json", function(statesPath) {
	var state = svg.append("g")
					.attr("class", "states")
					.selectAll()
					.data(statesPath)
					.enter()
					.append("g")
					.attr("class", "state")
					.append("path")
					.attr("class", function(d) {
						return "statePath " + d.id;
					})
					.attr("d",function(d){ return d.d;})
					.style("fill","white");

	d3.json("/count_by_year.json", function(totals) {
		// A bisector since many nation's data is sparsely-defined.
		// We provide this to make it easier to linearly interpolate between years.
		var bisect = d3.bisector(function(d) { return d[0]; });

		// Interpolates the dataset for the given (fractional) year.
		function interpolateData(year) {
			return totals.map(function(d) {
			  return {
			    name: d.state,
			    income: interpolateValues(d.total, year),
			  };
			});
		}

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
		svg.transition()
		  .duration(30000)
		  .ease(d3.easeLinear)
		  .tween("year", tweenYear)


		// Tweens the entire chart by first tweening the year, and then the data.
		// For the interpolated data, the dots and label are redrawn.
		function tweenYear() {
			var year = d3.interpolateNumber(1954, 2003);
			return function(t) { 
			  	yearLabel.text(Math.round(year(t)));
				var totalList = totals[Math.round(year(t)) - 1954].state;
				for(var i = 0; i < totalList.length; i++) {
					d3.select("." + totalList[i][0])
					  .style("fill", function() {
					  		var count = totalList[i][1];
					  		if (count < 10) {
					  			count /= 25;
					  		} else if (count >= 10 && count < 50) {
					  			count = 0.45;
					  		} else if (count >= 50 && count < 100) {
					  			count = 0.50;
					  		} else if (count >= 100 && count < 150) {
					  			count = 0.55;
					  		} else if (count >= 150 && count < 250) {
					  			count = 0.6;
					  		} else if (count >= 250 && count < 350) {
					  			count = 0.7;
					  		} else if (count >= 350 && count < 450) {
					  			count = 0.8;
					  		} else if (count >= 450 && count < 550) {
					  			count = 0.9;
					  		} else {
					  			count = 1;
					  		}
					  		return d3.interpolateBlues(count);
					  });
				}
			};
		}
	});
});

