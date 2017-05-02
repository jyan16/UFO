/**
 * Created by jinyan on 01/05/2017.
 */
var width = 1100, barHeight = 30;
var frontLength = 400;
var backLength = 50;

var data = [
    {"name" : "rept", "weight" : 3.3650},
    {"name" : "maneuv", "weight" : 3.1224},
    {"name" : "cigarett", "weight" : 2.8503},
    {"name" : "miami", "weight" : 2.8345},
    {"name" : "treelin", "weight" : 2.7730},
    {"name" : "disapp", "weight" : 2.7530},
    {"name" : "instantli", "weight" : 2.7271},
    {"name" : "nearbi", "weight" : 2.7036},
    {"name" : "meteoer", "weight" : -4.5612},
    {"name" : "press", "weight" : -4.0950},
    {"name" : "unhuman", "weight" : -3.9992},
    {"name" : "barrow", "weight" : -3.5846},
    {"name" : "odin", "weight" : -3.5253},
    {"name" : "odin", "weight" : -3.5253},
    {"name" : "simsburi", "weight" : -3.4650},
    {"name" : "ussauali", "weight" : -3.2597}
];

var x = d3.scaleLinear()
    .range([0, width-frontLength-backLength])
    .domain([0, d3.max(data, function(d) {
        return Math.abs(d.weight);
    })]);
var bar = d3.select(".chart")
    .append("svg")
    .attr("class", "chart")
    .attr("width", width)
    .attr("height", barHeight * data.length)
    .selectAll("g")
    .data(data)
    .enter().append("g")
    .attr("transform", function(d, i) {
        return "translate(0," + i * barHeight + ")"; });

bar.append("rect")
    .attr("width", function(d) {
        return x(Math.abs(d.weight));})
    .attr("height", barHeight - 10)
    .attr("x", frontLength)
    .style("fill", function(d) {
        return d.weight>0 ? "#1a8cff" : " #ff6600";
    });

bar.append("text")
    .attr("x", function(d) { return frontLength+backLength+x(Math.abs(d.weight));})
    .attr("y", barHeight / 2)
    .text(function(d) {return d.weight;})
    .style("text-anchor", "end")
    .style("font-weight", "bold");

bar.append("text")
    .attr("x", frontLength-5)
    .attr("y", barHeight / 2)
    .text(function(d) {return d.name;})
    .style("text-anchor", "end")
    .style("font-weight", "bold");
