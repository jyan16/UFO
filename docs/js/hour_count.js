var margin1 = {top: 19.5, right: 50, bottom: 19.5, left: 39.5};
var width1 = 700 - margin1.right;
var height1 = 400 - margin1.top - margin1.bottom;


var xScale = d3.scaleLinear().domain([-1, 24]).range([0, width1]),
    yScale = d3.scaleLinear().domain([0, 14000]).range([height1, 0]);

var xAxis = d3.axisBottom(xScale).ticks(12),
    yAxis = d3.axisLeft(yScale).ticks(6);

var svg1 = d3.select("#chart_histogram_hour").append("svg")
    .attr("width", width1 + margin1.left + margin1.right)
    .attr("height", height1 + margin1.top + margin1.bottom)
    .attr("transform", "translate(" + margin1.left + "," + margin1.top + ")")
    .append("g")

var xx = svg1.append("g")
            .attr("class", "xaxis")
            .attr("transform", "translate("+margin1.left+"," + (height1+margin1.top)+")")
            .call(xAxis)

var yy = svg1.append("g")
            .attr("class", "yaxis")
            .attr("transform", "translate("+margin1.left+","+margin1.top+")")
            .call(yAxis);      

xx.append("text")
  .attr("class", "label")
  .text("hour/day")
  .attr("x", width1 + margin1.left)
  .style("text-anchor", "end")
  .attr("dy", -5)     

yy.append("text")
  .attr("class", "label")
  .text("UFO sighting number")
  .attr("transform","rotate(270)")
  .attr("dy", 10) 

xPadding = xScale(0)/3;

d3.json("/data/count_by_hour.json", function(hours) {
	svg1.append("g")
	   .attr("class", "hours")
	   .selectAll("rect")
	   .data(hours).enter()
	   .append("rect")
	   .attr("width", width1 / 24 - xPadding)
	   .attr("height", function(d) { return height1 - yScale(d.count);})
	   .attr("x", function(d) {return margin1.left - xPadding + xScale(parseInt(d.hour));})
	   .attr("y", function (d) {return margin1.top + yScale(d.count);})
     .attr("fill", "#3C8749");

})
