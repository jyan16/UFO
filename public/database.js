/**
 * Created by jinyan on 22/04/2017.
 */
$.get("/database_event", function(response) {
    draw_event(response);
    $(document).ready( function () {
        $('#eventTable').DataTable();
    });
});
$.get("/database_state", function(response) {
    draw_state(response);
    $(document).ready( function () {
        $('#stateTable').DataTable();
    });
});
function draw_event(data) {
    var table = d3.select("#eventTableContainer").append("table")
        .attr("id", "eventTable");
    var thead = table.append("thead");
    var tbody = table.append("tbody");
    thead.append("tr")
        .selectAll("th")
        .data(data.fields).enter()
        .append("th")
        .text(function(d) {return d.name;});

    var rows = tbody.selectAll("tr")
        .data(data.rows).enter()
        .append("tr");
    var cells = rows.selectAll("td")
        .data(function(d) {
            return data.fields.map(function (column) {return {name: column.name, value: d[column.name]};});
        }).enter()
        .append("td")
        .html(function(d) {return d.value;});
}

function draw_state(data) {
    var table = d3.select("#stateTableContainer").append("table")
        .attr("id", "stateTable");
    var thead = table.append("thead");
    var tbody = table.append("tbody");
    thead.append("tr")
        .selectAll("th")
        .data(data.fields).enter()
        .append("th")
        .text(function(d) {return d.name;});

    var rows = tbody.selectAll("tr")
        .data(data.rows).enter()
        .append("tr");
    var cells = rows.selectAll("td")
        .data(function(d) {
            return data.fields.map(function (column) {return {name: column.name, value: d[column.name]};});
        }).enter()
        .append("td")
        .html(function(d) {return d.value;});
}