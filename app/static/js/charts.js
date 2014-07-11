
function lineChart(data){
    console.log(data);

    nv.addGraph(function() {
      var chart = nv.models.lineWithFocusChart()
                .x(function(d) { return d[0] })
                .y(function(d) { return d[1] });

      chart.xAxis
          .tickFormat(function(d) { return d3.time.format('%X')(new Date(d)) });

      chart.yAxis
          .tickFormat(d3.format(',.2f'));

      chart.x2Axis
            .tickFormat(function(d) {
                return d3.time.format('%x')(new Date(d))
              });

      chart.y2Axis
          .tickFormat(d3.format(',.2f'));

      d3.select('#chart svg')
          .datum(data)
          .transition().duration(500)
          .call(chart);

      nv.utils.windowResize(chart.update);

      return chart;
    });
}