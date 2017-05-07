
/**
 * Created by jinyan on 19/04/2017.
 */

var map;
var margin = {top: 19.5, right: 19.5, bottom: 19.5, left: 39.5};

function initMap() {
    var myLatLng = {lat: 40.78, lng: -97.21};

    // Create a map object and specify the DOM element for display.
    map = new google.maps.Map(document.getElementById("map"), {
        center: myLatLng,
        scrollwheel: false,
        zoom: 4,
        mapTypeId: 'satellite'
    });
}

function getData(survey) {

    ///////////////////////////
    //draw D3 chart and table//
    ///////////////////////////

    $.get('/submit', survey.data, function(response) {
        response = JSON.parse(response);
        var info = [];
        var prob = [];
        for (var key in response) {
            if (key=="lat" || key=="lng" || key=="weather" || key=="visibility") {
                info[key] = response[key];
            } else {
                prob[key] = response[key];
            }
        }
        draw_table(info);
        draw_d3(prob);
        draw_map_label();
        $.get('/google', function(response) {
            $("#map").css("visibility", "visible");
            var marker = new google.maps.Marker({
                position: {lat: info.lat, lng: info.lng},
                map: map,
                title: 'I am here!'
            });
            var data = createData(response);
            var heatmap = new google.maps.visualization.HeatmapLayer({
                data: data,
                map: map
            });
        })
    });
}

function createData(response) {
    var result = [];
    for (item in response) {
        for (var i = 0; i < response[item].num; i++) {
            var tmp = new google.maps.LatLng(response[item].lat, response[item].lng);
            result.push(tmp);
        }
    }
    return result;
}

function draw_map_label() {
    var svg = d3.select("#labelContainer").append("svg")
        .attr("class", "chart")
        .attr("width", 1000)
        .attr("height", 50);
    var label = svg.append("text")
        .attr("x", 450)
        .attr("y", 25)
        .style("text-anchor", "middle")
        .style("font", "30px sans-serif")
        .text("Accumulative UFO Sighting Distribution of U.S.")
}



function draw_table(response) {

    /////////////////////////////////////
    //draw table of numeric information//
    /////////////////////////////////////
    var width = 1000;
    var height = 200;
    var svg = d3.select("#tableContainer")
        .append("svg")
        .attr("class", "chart")
        .attr("width", width)
        .attr("height", height);
    var label = svg.append("text")
        .attr("x", width / 2 - 30)
        .attr("y", height / 4)
        .text("Numeric Information")
        .style("font", "30px sans-serif")
        .attr("text-anchor", "middle");

    var data = [];
    for (var key in response) {
        var tmp = {"name": key, "value": response[key]};
        data.push(tmp);
    }
    var head = svg.selectAll("g")
        .data(data).enter()
        .append("g")
        .attr("transform", function(d, i) {
            return "translate(" + ((i - 1) * width / 5 + 350) + "," + height / 2 + ")";
        });

    head.append("text")
        .attr("x", 0)
        .attr("y", 0)
        .text(function (d) {return d.name;});

    head.append("text")
        .attr("x", 0)
        .attr("dy", 25)
        .style("font_weight", "normal")
        .text(function (d) {
            if (d.name=="lat" || d.name=="lng") {
                return d.value.toString().substring(0,6);
            }
            return d.value});

}

function draw_d3(response) {

    ///////////////////////////////
    //calculate probability score//
    ///////////////////////////////
    var summary = (response.sum_log + response.sum_tree)/2;
    var numeric = (response.num_svm + response.num_tree)/2;

    var score = (summary + numeric)/2;
    if (score >= 0.5) {
        $(".complete").text("Congratulations! The true possibility is " + (score*100).toString().substring(0,5) + "%!");
    } else {
        $(".complete").text("Sorry, the true possibility is " + (score*100).toString().substring(0,5) + "%");
    }

    ///////////////////////////////
    //draw D3 chart about results//
    ///////////////////////////////
    var width = 1000;
    var height = 800;

    var pie_data = [];
    pie_data.push({"name":"summary", "prob":summary / (score * 2)});
    pie_data.push({"name":"numeric", "prob":numeric / (score * 2)});
    var svg = d3.select("#chartContainer").append("svg")
        .attr("class", "chart")
        .attr("width", width)
        .attr("height", height);
    //////////////////
    //draw pie chart//
    //////////////////
    var svg_pie = svg.append("g")
        .attr("class", "pie_chart")
        .attr("transform", "translate(" + (width / 2 - margin.left) + "," + (margin.top + height / 4) + ")");
    var label_pie = svg_pie
        .append("text")
        .attr("x", 0)
        .attr("y", -height / 4 + 20)
        .style("font", "30px sans-serif")
        .attr("text-anchor", "middle")
        .text("Information Contribution");
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
    var colorScale = d3.interpolateRgb("red", "yellow");

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
            return "translate(" + width / 5 + "," + (i - 1) * height / 15 + ")";
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
        var tmp = {"name": key, "prob": response[key]};
        data.push(tmp);
    }
    var barHeight = 70;
    var svg_his = svg.append("g")
        .attr("class", "histogram_chart")
        .attr("transform", "translate(" + (width / 3 - 30) + "," + (margin.top + height / 2 + 20) + ")");
    var label_his = svg_his
        .append("text")
        .attr("x", width / 8 + 30)
        .attr("y", 0)
        .style("font", "30px sans-serif")
        .attr("text-anchor", "middle")
        .text("Classifier Result");

    var bar = svg_his.selectAll("g")
        .data(data).enter()
        .append("g")
        .attr("transform", function(d, i) {
            return "translate(-50," + (i * barHeight + 30) + ")";
        });
    var x = d3.scaleLinear()
        .range([0, (width - margin.right - margin.left)/2])
        .domain([0, 1]);
    var colorScale1 = d3.interpolateRgb("purple", "blue");
    bar.append("rect")
        .attr("width", function(d) {
            return x(d.prob);})
        .attr("height", barHeight - 35)
        .style("fill", function(d, i) {return colorScale1(i / data.length)});

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
}
