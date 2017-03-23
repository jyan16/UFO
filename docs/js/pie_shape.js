var margin1 = {top: 19.5, right: 50, bottom: 19.5, left: 39.5};
var width1 = 700 - margin1.right;
var height1 = 400 - margin1.top - margin1.bottom;


var svg2 = d3.select("#chart_pie_shape").append("svg")
    .attr("width", width1 + margin1.left + margin1.right)
    .attr("height", height1 + margin1.top + margin1.bottom)
    .append("g")
    .attr("class", "pie_shape")
    .attr("transform", "translate(" + (margin1.left + width1 / 2) + "," + (margin1.top + height1 / 2) + ")")
    

d3.json("/data/shape_all.json", function(shapes) {

    var pie = d3.pie()
                .sort(null)
                .value(function(d) {
                    return d.count;
                });
    var arcs = svg2.selectAll(".arc")
    			   .data(pie(shapes)).enter()
    			   .append("g")
    			   .attr("class", "arc")

    var myarc = d3.arc()
    			.outerRadius(200)
    			.innerRadius(0); 


    var colorScale = d3.interpolateRgb("red", "blue");

    arcs.append("path")
        .attr("class", "pie")
    	.attr("d", myarc)
    	.style("fill", function(d, i) {
    		console.log(i)
    		return colorScale(i/shapes.length);})
})
