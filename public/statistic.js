/**
 * Created by jinyan on 10/04/2017.
 */
$(document).ready(function(){
    $.get('/statistic_data', function(response) {
        var numberFormat = d3.format(".2f");
        var data = response;
            shapeRingChart   = dc.pieChart("#chart-ring-shape");
            weatherRingChart   = dc.pieChart("#chart-ring-weather");
            yearLineChart = dc.lineChart("#chart-line-year");
            weekRowChart = dc.rowChart("#chart-row-day");
            hourHistChart  = dc.barChart("#chart-hist-hour");
            yearRangeChart = dc.barChart("#year-range-chart");
            geoMapChart = dc.geoChoroplethChart("#chart-geo-map");
        var dateFormat = d3.time.format('%Y-%m-%dT%H:%M:%SZ');
        data.forEach(function(d) {
            d.dd = dateFormat.parse(d.date);
            d.month = d3.time.month(d.dd);
        });

        // set crossfilter
        var ndx = crossfilter(data),
            stateDim = ndx.dimension(function(d) {return d.state;}),
            shapeDim  = ndx.dimension(function(d) {return d.shape;}),
            weatherDim  = ndx.dimension(function(d) {return d.weather;}),
            hourDim = ndx.dimension(function(d) {
                var hour = d.dd.getHours();
                return hour;
            }),
            weekDim  = ndx.dimension(function(d) {
                var day = d.dd.getDay();
                var name = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
                //return day + '.' + name[day];
                return name[day];
            }),
            yearDim = ndx.dimension(function(d) {
                return d.month;
            }),
            countPerState = stateDim.group().reduceCount(),
            countPerShape = shapeDim.group().reduceCount(),
            countPerWeather = weatherDim.group().reduceCount(),
            countPerDay = weekDim.group().reduceCount(),
            hourHist = hourDim.group().reduceCount(),
            yearGroup = yearDim.group().reduceCount(),
            weekGroup = weekDim.group();

        $.get('/us-states', function(statesJson) {
            geoMapChart
                .width(990)
                .height(500)
                .dimension(stateDim)
                .group(countPerState)
                .colors(d3.scale.quantize().range(["#E2F2FF", "#C4E4FF", "#9ED2FF", "#81C5FF", "#6BBAFF", "#51AEFF", "#36A2FF", "#1E96FF", "#0089FF", "#0061B5"]))
                .colorDomain([0, 11147])
                .colorCalculator(function (d) { return d ? geoMapChart.colors()(d) : '#ccc'; })
                .overlayGeoJson(statesJson.features, "state", function (d) {
                    return d.properties.name;
                })
                .valueAccessor(function(kv) {
                    return kv.value;
                })
                .title(function (d) {
                    return "State: " + d.key + "\nTotal Number of UFO Report: " + d.value;
                })
                .turnOnControls(true);
            shapeRingChart
                .dimension(shapeDim)
                .group(countPerShape)
                .turnOnControls(true)
                .innerRadius(50)
                .controlsUseVisibility(true);

            weatherRingChart
                .dimension(weatherDim)
                .group(countPerWeather)
                .innerRadius(50)
                .controlsUseVisibility(true);

            hourHistChart
                .dimension(hourDim)
                .group(hourHist)
                .x(d3.scale.linear().domain([0, 24]))
                .renderHorizontalGridLines(true)
                // .elasticX(true)
                .elasticY(true)
                .controlsUseVisibility(true)
                .xAxis()
                .ticks(12);

            hourHistChart.xAxis().tickFormat(function(d) {

                if (d < 12) {
                    return d + "AM";
                } else if (d == 12) {
                    return d + "PM";
                } else {
                    return (d - 12) + "PM";
                }
            });
            // convert time
            hourHistChart.yAxis().tickFormat(d3.format("d"));
            hourHistChart.yAxis().ticks(3);
            hourHistChart.filter([0, 24]);

            var weekDic = {"Sun": "a", "Mon": "b", "Tue": "c", "Wed": "d", "Thu": "e", "Fri": "f", "Sat": "g"};

            weekRowChart
                .dimension(weekDim)
                .group(weekGroup)
                .elasticX(true)
                .controlsUseVisibility(true)
                .ordering(function(d) {
                    //return weekDic[d.key.split('.')[1]];
                    return weekDic[d.key];
                })
                .label(function(d) {
                    //return d.key.split('.')[1];
                    return d.key;
                })
                .xAxis().ticks(3);

            weekRowChart.xAxis().tickFormat(d3.format("d"));

            function show_empty_message(chart) {
                var is_empty = d3.sum(chart.group().all().map(chart.valueAccessor())) === 0;
                var data = is_empty ? [1] : [];
                var empty = chart.svg().selectAll('.empty-message').data(data);
                empty.enter().append('text')
                    .text('NO DATA!')
                    .attr({
                        'text-anchor': 'middle',
                        'alignment-baseline': 'middle',
                        class: 'empty-message',
                        x: chart.margins().left + chart.effectiveWidth()/2,
                        y: chart.margins().top + chart.effectiveHeight()/2
                    })
                    .style('opacity', 0);
                empty.transition().duration(1000).style('opacity', 1);
                empty.exit().remove();
            }

            yearLineChart
                .renderArea(true)
                .width(990)
                .height(200)
                .transitionDuration(1000)
                .margins({top: 30, right: 50, bottom: 25, left: 40})
                .dimension(yearDim)
                .mouseZoomable(true)
                .rangeChart(yearRangeChart)
                .x(d3.time.scale().domain([new Date(1985, 0, 1), new Date(2012, 11, 31)]))
                .round(d3.time.month.round)
                //  .xUnites(d3.time.months)
                .elasticY(true)
                .renderHorizontalGridLines(true)
                .legend(dc.legend().x(800).y(10).itemHeight(13).gap(5))
                .brushOn(false)
                .group(yearGroup, "Total Numbers of UFO Reports");

            yearLineChart.yAxis().tickFormat(d3.format("d"));

            yearRangeChart
                .width(990)
                .height(40)
                .margins({top: 0, right: 50, bottom: 20, left: 40})
                .dimension(yearDim)
                .group(yearGroup)
                .centerBar(true)
                .gap(1)
                .x(d3.time.scale().domain([new Date(1985, 0, 1), new Date(2012, 11, 31)]))
                .round(d3.time.month.round)
                .alwaysUseRounding(true)
                .xUnits(d3.time.months);

            yearRangeChart.yAxis().tickValues([]);



            hourHistChart.on('pretransition', show_empty_message);
            weekRowChart.on('pretransition', show_empty_message);

            dc.renderAll();
        });
    });
});