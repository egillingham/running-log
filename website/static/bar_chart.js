
function barChart(chart_data, base_class, yAxisTitle, tot_height, tot_width) {
    // find data key name
    var data_keys = Object.keys(chart_data[0]);
    data_keys.splice(data_keys.indexOf('date'), 1);
    var dkey = data_keys[0];

    // size settings
    var margin = {top: 20, right: 40, bottom: 30, left: 40};
    // char set-up
    var chart_base = d3.select(base_class);
    var chart = chart_base.append("div").attr("class", "chart").style("position", "relative");
    //var legend = chart.append("div").attr("class", "legend");
    var svg = chart.append('svg').attr('height', tot_height).attr('width', tot_width).style("shape-rendering", "crispEdges");
    var width = svg.attr("width") - margin.left - margin.right,
        height = svg.attr("height") - margin.top - margin.bottom;
    var bar_width = (width / (chart_data.length + 2));
    var g = svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // make the damn chart
    var y = d3.scaleLinear()
      .range([height, 0])
      .domain([0, d3.max(chart_data, function(d) { return d[dkey]; })]);

    var x = d3.scaleTime()
      .range([0, width])
      // TODO: make date buffers dynamic to range of data
      .domain([d3.min(chart_data, function(d) {date = new Date(Date.parse(d.date)); return date.setDate(date.getDate() - 7); }),
               d3.max(chart_data, function(d) {date = new Date(Date.parse(d.date)); return date.setDate(date.getDate() + 7); })
              ]);

    g.selectAll('rect.bar')
      .data(chart_data)
      .enter()
        .append('rect')
          .attr("class", "bar")
          .attr('fill', "#adc698")
          .attr('rx', '1.5')
          .attr('ry', '1.5')
          .attr('x', function(d) { return x(new Date(Date.parse(d.date))) - bar_width / 2; })
          .attr('width', bar_width)
          .attr('y', function(d) {
            // remember that SVG is y-down while our graph is y-up!
            // here, we set the top-left of this bar segment to the
            // larger value of the pair
            return y(d[dkey]);
          }).attr('height', function(d) {
            // since we are drawing our bar from the top downwards,
            // the length of the bar is the distance between our points
            return height - y(d[dkey]);
          })
          .on("mouseover", function() {
            d3.select("#tooltip").transition().delay(2).style("opacity", 1)
            })
          .on("mouseout", function() {
            d3.select("#tooltip").transition().delay(2).style("opacity", 0);
            })
          .on("mousemove", function(d) {
            var xPosition = d3.mouse(this)[0] - 15;
            var yPosition = y(d[dkey]);
            tooltip.style("left", xPosition + 'px');
            tooltip.style("top", yPosition + 'px');
            tooltip.select("div.tooltip-title").text(d.date);
            tooltip.select("div.tooltip-text").text(d[dkey] + " " + yAxisTitle);
          });

    // AXIS
    g.append("g")
        .attr("class", "y-axis")
        .call(d3.axisLeft(y).ticks(4))
     .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .attr("fill", '#000')
        .text(yAxisTitle);

    g.append('g')
      .attr('class', 'x-axis')
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));


    // Prep the tooltip bits, initial display is hidden
    var tooltip = chart.append("div")
      .attr("id", "tooltip")
      .style("display", "inline-block")
      .style("opacity", 0);

    tooltip.append("div")
      .attr("class", "tooltip-title")
      .attr("x", 15)
      .attr("dy", "1.2em")
      .attr("width", 50)
      .attr("height", 50)

    tooltip.append("div")
      .attr("class", "tooltip-text")
      .attr("x", 15)
      .attr("dy", "1.2em")
      .attr("width", 50)
      .attr("height", 50)

}

function getDates(startDate, stopDate) {
    var dateArray = [];
    var currentDate = startDate;
    while (currentDate <= stopDate) {
        dateArray.push(new Date(currentDate))
        currentDate.setDate(currentDate.getDate() + 1);
    }
    return dateArray;
}
