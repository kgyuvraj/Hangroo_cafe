function drawPieChart(pie_chart_data) {
    // Define the chart to be drawn.
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Metric');
    data.addColumn('number', 'Percentage');
    data.addRows(pie_chart_data["data"]);

    // Set chart options
    var options = {
        'title' : pie_chart_data["title"]
    };

    // Instantiate and draw the chart.
    var chart = new google.visualization.PieChart(document
            .getElementById(pie_chart_data["element"]));
    chart.draw(data, options);
}

function drawLineChart(line_chart_data) {
    // Define the chart to be drawn.
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Month');
    data.addColumn('number', 'Count');

    data.addRows(line_chart_data["data"]);

    // Set chart options
    var options = {
        'title' : line_chart_data["title"],
        hAxis : {
            title : line_chart_data["x_axis_title"]
        },
        vAxis : {
            title : line_chart_data["y_axis_title"]
        },
    // 'width':550,
    // 'height':400
    };

    // Instantiate and draw the chart.
    var chart = new google.visualization.LineChart(document
            .getElementById(line_chart_data["element"]));
    chart.draw(data, options);
}

function drawBarChart(bar_chart_data) {
    // Define the chart to be drawn.
    var data = google.visualization.arrayToDataTable(bar_chart_data["data"]);

    var options = {
        title : bar_chart_data["title"]
    };

    // Instantiate and draw the chart.
    var chart = new google.visualization.ColumnChart(document
            .getElementById(bar_chart_data["element"]));
    chart.draw(data, options);
}
function drawAreaChart(area_chart_data) {
    // Define the chart to be drawn.
    var data = google.visualization.arrayToDataTable(area_chart_data["data"]);

    var options = {
        title : area_chart_data["title"],
        hAxis : {
            title : area_chart_data["x_axis_title"],
        /*            titleTextStyle : {
         color : '#333'
         }*/
        },
        vAxis : {
            minValue : 0
        }
    };

    // Instantiate and draw the chart.
    var chart = new google.visualization.AreaChart(document
            .getElementById(area_chart_data['element']));
    chart.draw(data, options);
}
