
function barChart(chart_data, base_class, yAxisTitle, tot_height, tot_width) {
    // size settings
    var margin = {top: 20, right: 40, bottom: 30, left: 40};

    // color
    var color = d3.scaleOrdinal(["#adc698", "#61988e", "#592d51", "#eabda8"]);

    // char set-up
    var chart = d3.select(base_class)
    var legend = chart.append("div").attr("class", "legend");
    var svg = chart.append('svg').attr('height', tot_height).attr('width', tot_width);
    var width = svg.attr("width") - margin.left - margin.right,
        height = svg.attr("height") - margin.top - margin.bottom;
    // define bar width using date range
//    var date_range = getDates(d3.min(data, function(d) {return new Date(Date.parse(d.date))}),
//                              d3.max(data, function(d) {return new Date(Date.parse(d.date))}));
    var bar_width = (width / (chart_data.length + 2));
    var g = svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // make the damn chart
    var y = d3.scaleLinear()
      .range([height, 0])
      // TODO make value key ambiguous
      .domain([0, d3.max(chart_data, function(d) { return d.miles; })]);

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
            return y(d.miles);
          }).attr('height', function(d) {
            // since we are drawing our bar from the top downwards,
            // the length of the bar is the distance between our points
            return height - y(d.miles);
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
