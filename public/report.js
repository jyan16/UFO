/**
 * Created by jinyan on 19/04/2017.
 */

var margin = {top: 19.5, right: 19.5, bottom: 19.5, left: 39.5};
var width = 1000;
var height = 500;

function getData(survey) {

    $.get('/submit', survey.data, function(response) {
        ///////////////////////////////
        //calculate probability score//
        ///////////////////////////////
        response = JSON.parse(response);
        var summary = (response.sum_log + response.sum_tree)/2;
        var numeric = (response.num_svm + response.num_tree)/2;

        var score = (summary + numeric)/2;
        if (score >= 0.5) {
            $(".complete").text("Congratulations!! The true possibility is " + (score*100).toString().substring(0,5) + "%");
        } else {
            $(".complete").text("Sorry, the true possobility is " + (score*100).toString().substring(0,5) + "%, it maybe fake.");
        }

        ///////////////////////////////
        //draw D3 chart about results//
        ///////////////////////////////
        var pie_data = [];
        pie_data.push({"name":"summary", "prob":summary / (score * 2)});
        pie_data.push({"name":"numeric", "prob":numeric / (score * 2)});
        var svg = d3.select("#resultContainer").append("svg")
            .attr("width", width)
            .attr("height", height);

        //////////////////
        //draw pie chart//
        //////////////////
        var svg_pie = svg.append("g")
            .attr("class", "pie_chart")
            .attr("transform", "translate(" + (margin.left + width / 6) + "," + (margin.top + height / 2) + ")");
        var pie = d3.pie()
            .sort(null)
            .value(function(d) { return d.prob; });
        var arcs = svg_pie.selectAll(".arc")
            .data(pie(pie_data)).enter()
            .append("g")
            .attr("class", "arc");
        var radius = d3.arc()
            .outerRadius(150)
            .innerRadius(40);
        var colorScale = d3.interpolateRgb("red", "blue");

        arcs.append("path")
            .attr("class", "pie")
            .attr("d", radius)
            .style("fill", function(d, i) {
                return colorScale(i/pie_data.length);});
        arcs.append("title")
            .text(function(d) {
                return d.data.name;});

        //draw legend
        var legend = svg_pie.append("g")
            .selectAll("g")
            .data(pie_data).enter()
            .append("g")
            .attr("transform", function(d, i) {
                return "translate(-100" + "," + (-(i-1)*30 -height / 2 + 30) + ")";
            });

        legend.append("rect")
            .attr("width", 20)
            .attr("height", 20)
            .style("fill", function (d, i) { return colorScale(i/pie_data.length) });
        legend.append("text")
            .attr("x", 25)
            .attr("y", 15)
            .text(function(d) {
                return d.name + " : " + (d.prob * 100).toString().substring(0,4) + "%";
            });

        ////////////////////////
        //draw histogram chart//
        ////////////////////////
        var data = [];
        for (var key in response) {
            var tmp = {"name":key, "prob":response[key]};
            data.push(tmp);
        }
        var barHeight = 80;
        var svg_his = svg.append("g")
            .attr("class", "histogram_chart")
            .attr("transform", "translate(" + (width / 2 - 40) + "," + (margin.top + 100) + ")")
        var bar = svg_his.selectAll("g")
            .data(data).enter()
            .append("g")
            .attr("transform", function(d, i) {
                return "translate(0," + i * barHeight + ")";
            });
        var x = d3.scaleLinear()
            .range([0, (width - margin.right - margin.left)/2])
            .domain([0, 1]);
        bar.append("rect")
            .attr("width", function(d) {
                return x(d.prob);})
            .attr("height", barHeight - 40)
            .style("fill", "teal");

        bar.append("text")
            .attr("x", function(d) { return x(d.prob) + 5;})
            .attr("y", barHeight / 2 - 15)
            .style("text-anchor", "start")
            .text(function(d) {return (d.prob * 100).toString().substring(0,4) + "%"});

        bar.append("text")
            .attr("x", -5)
            .attr("y", barHeight / 2 - 15)
            .style("text-anchor", "end")
            .text(function(d) {return d.name;})

        //////////////////////////
        //Google Map result show//
        //////////////////////////

        
    });
    $.get('/google', function(response) {
        console.log(response);

    });

};
