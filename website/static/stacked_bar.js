
function stackedBar(data, base_class, tot_height, tot_width) {
    // data transformation
    var activity_keys = Object.keys(activity_min[0]);
    activity_keys.splice(activity_keys.indexOf('date'), 1);
    var stack = d3.stack().keys(activity_keys);
    var stacked_min = stack(activity_min);

    // size settings
    var margin = {top: 20, right: 40, bottom: 30, left: 40};

    // color
    var color = d3.scaleOrdinal(["#adc698", "#61988e", "#592d51", "#eabda8"]);

    // char set-up
    var chart = d3.select(base_class)
    var legend = chart.append("div").attr("class", "legend");
    var svg = chart.append('svg').attr('height', tot_height).attr('width', tot_width);
    var width = svg.attr("width") - margin.left - margin.right,
        height = svg.attr("height") - margin.top - margin.bottom,
        bar_width = (width / (activity_min.length + 2));
    var g = svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // make the damn chart
    var maxY = d3.max(stacked_min, function(d) {
      return d3.max(d, function(d) {
        return d[1];
      });
    });

    var y = d3.scaleLinear()
      .range([height, 0])
      .domain([0, maxY]);

    var x = d3.scaleTime()
      .range([0, width])
      // .domain(d3.extent(activity_min, function(d) {
      //   return new Date(Date.parse(d.date));
      // }))
      .domain([d3.min(activity_min, function(d) {date = new Date(Date.parse(d.date)); return date.setDate(date.getDate() - 1); }),
               d3.max(activity_min, function(d) {date = new Date(Date.parse(d.date)); return date.setDate(date.getDate() + 1); })
                ]);

    var layers = g.selectAll('g.layer')
      .data(stacked_min, function(d) { return d.key; })
        .enter()
          .append('g')
            .attr('class', 'layer')
            .attr('fill', function(d) { return color(d.key); })

    layers.selectAll('rect.bar')
      .data(function(d) { return d; })
      .enter()
        .append('rect')
          .attr("class", "bar")
          .attr('rx', '1.5')
          .attr('ry', '1.5')
          .attr('x', function(d) { return x(new Date(Date.parse(d.data.date))) - bar_width / 2; })
          .attr('width', bar_width)
          .attr('y', function(d) {
            // remember that SVG is y-down while our graph is y-up!
            // here, we set the top-left of this bar segment to the
            // larger value of the pair
            return y(d[1]);
          }).attr('height', function(d) {
            // since we are drawing our bar from the top downwards,
            // the length of the bar is the distance between our points
            return y(d[0]) - y(d[1]);
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
        .text("Minutes of Activity");

    g.append('g')
      .attr('class', 'x-axis')
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x).ticks(7));


    // LEGEND
    legend.selectAll('text')
          .data(stacked_min, function(d) { return d.key; })
          .enter()
            .append('div')
              .attr('class', 'legend-item');

    var legend_items = legend.selectAll('div.legend-item');

    legend_items.append('div')
      .attr('class', 'legend-icon')
      .attr('style', function(d) { return 'background-color:' + color(d.key) + ';border-color:' + color(d.key); });

    legend_items.append('div')
      .attr('class', 'legend-txt')
      .text(function(d) { return d.key; });

}
