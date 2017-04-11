/**
 * Created by jinyan on 10/04/2017.
 */
var data = [
    { "book": "A", "scores": 45 },
    { "book": "B", "scores": 34 },
    { "book": "C", "scores": 54 },
    { "book": "D", "scores": 27 },
    { "book": "E", "scores": 70 },
    { "book": "F", "scores": 25 },
    { "book": "G", "scores": 92 },
    { "book": "H", "scores": 22 },
    { "book": "I", "scores": 40 },
    { "book": "J", "scores": 10 },
    { "book": "K", "scores": 40 }
];
//## Create Chart Objects
var scoreChart = dc.barChart("#dc-score-barchart")
    .xAxisLabel('book_id')
    .yAxisLabel('score');
var goodYesNoPieChart = dc.pieChart('#dc-coreAcc-piechart');
//### Create Crossfilter Dimensions and Groups
var ndx = crossfilter(data);
var all = ndx.groupAll();
var bookDimension = ndx.dimension(function (d) {return d.book;}),
    bookscoresGroup = bookDimension.group().reduceSum(function(d) {return d.scores;});
//## score bar chart
scoreChart.width(320)
    .height(320)
    .dimension(bookDimension)
    .group(bookscoresGroup)
    .elasticY(true)
    .x(d3.scale.ordinal())
    .xUnits(dc.units.ordinal)
    .colors(["orange"])
    .yAxis().ticks(5);
//## pie chart
// reusable function to create threshold dimension
function coreCount_from_threshold() {
    var scoreThreshold=document.getElementById('slideRange').value;
    scoreThreshold=parseFloat(scoreThreshold);
    if (isNaN(scoreThreshold)) {
        scoreThreshold=0.5
    }
    return ndx.dimension(function (d) {
        var maxNumber=80;
        if (d.scores >maxNumber*scoreThreshold) {
            return 'High';
        } else {
            return 'Low';
        }
    });
}
var coreCount = coreCount_from_threshold();
var coreCountGroup = coreCount.group();
goodYesNoPieChart
    .width(320)
    .height(320)
    .radius(120)
    .innerRadius(40)
    .dimension(coreCount)
    .title(function(d){return d.value;})
    .group(coreCountGroup)
    .label(function (d) {
        if (goodYesNoPieChart.hasFilter() && !goodYesNoPieChart.hasFilter(d.key)) {
            return d.key + '(0%)';
        }
        var label = d.key;
        if (all.value()) {
            label += '(' + Math.floor(d.value / all.value() * 100) + '%)';
        }
        return label;
    })
dc.renderAll();
//## change slider score value to re-assign the data in pie chart
function updateSlider(slideValue) {
    var sliderDiv = document.getElementById("sliderValue");
    sliderDiv.innerHTML = slideValue;
    coreCount.dispose();
    coreCount = coreCount_from_threshold();
    coreCountGroup = coreCount.group();
    goodYesNoPieChart
        .dimension(coreCount)
        .group(coreCountGroup);
    dc.redrawAll();
}