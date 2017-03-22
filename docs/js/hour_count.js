var margin = {top: 19.5, right: 19.5, bottom: 19.5, left: 39.5};
var width = 960 - margin.right;
var height = 500 - margin.top - margin.bottom;


var svg = d3.select("#chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
    .append("g")

var xScale = d3.scaleLinear().domain([00, 24]).range([0, width])
var yScale = d3.scaleLinear().domain([0,15000]).range([height, 0])

var xAxis = d3.axisBottom(xScale).ticks(24, d3.format(",d")),
    yAxis = d3.axisLeft(yScale);


var xx = svg.append("g")
            .attr("class", "xaxis")
            .attr("transform", "translate("+margin.left+"," + (height+margin.top)+")")
            .call(xAxis)
   

var yy = svg.append("g")
            .attr("class", "yaxis")
            .attr("transform", "translate("+margin.left+","+margin.top+")")
            .call(yAxis);