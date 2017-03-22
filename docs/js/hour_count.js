var margin = {top: 19.5, right: 50, bottom: 19.5, left: 39.5};
var width = 700 - margin.right;
var height = 400 - margin.top - margin.bottom;


var xScale = d3.scaleLinear().domain([-1, 24]).range([0, width]),
    yScale = d3.scaleLinear().domain([0, 14000]).range([height, 0]);

var xAxis = d3.axisBottom(xScale).ticks(12),
    yAxis = d3.axisLeft(yScale).ticks(6);

var svg = d3.select("#chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
    .append("g")

var xx = svg.append("g")
            .attr("class", "xaxis")
            .attr("transform", "translate("+margin.left+"," + (height+margin.top)+")")
            .call(xAxis)

var yy = svg.append("g")
            .attr("class", "yaxis")
            .attr("transform", "translate("+margin.left+","+margin.top+")")
            .call(yAxis);      

xx.append("text")
  .attr("class", "label")
  .text("hour/day")
  .attr("x", width + margin.left)
  .style("text-anchor", "end")
  .attr("dy", -5)     

yy.append("text")
  .attr("class", "label")
  .text("UFO sighting number")
  .attr("transform","rotate(270)")
  .attr("dy", 10) 

xPadding = xScale(0)/2;

d3.json("data/count_by_hour.json", function(hours) {
	svg.append("g")
	   .attr("class", "hours")
	   .selectAll("rect")
	   .data(hours).enter()
	   .append("rect")
	   .attr("width", width / 24 - xPadding)
	   .attr("height", function(d) { return height - yScale(d.count);})
	   .attr("x", function(d) {return margin.left + xScale(parseInt(d.hour)) - xPadding;})
	   .attr("y", function (d) {return margin.top + yScale(d.count);})
     .attr("fill", "#3C8749");

})
