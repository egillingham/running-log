
function stackedBar(data, base_class, yAxisTitle, tot_height, tot_width) {
    // data transformation
    var data_keys = Object.keys(data[0]);
    data_keys.splice(data_keys.indexOf('date'), 1);
    var stack = d3.stack().keys(data_keys);
    var stacked_min = stack(data);

    // size settings
    var margin = {top: 20, right: 40, bottom: 30, left: 40};

    // color
    var color = d3.scaleOrdinal(["#adc698", "#61988e", "#592d51", "#eabda8"]);

    // date format
    var dateFormat = d3.timeFormat("%B %e, %Y")

    // char set-up
    var chart_base = d3.select(base_class);
    var chart = chart_base.append("div").attr("class", "chart").style("position", "relative");
    var legend = chart.append("div").attr("class", "legend");
    var svg = chart.append('svg').attr('height', tot_height).attr('width', tot_width);
    var width = svg.attr("width") - margin.left - margin.right,
        height = svg.attr("height") - margin.top - margin.bottom;
    // define bar width using date range
    var date_range = getDates(d3.min(data, function(d) {return new Date(parseDate(d.date))}),
                              d3.max(data, function(d) {return new Date(parseDate(d.date))}));
    var bar_width = (width / (date_range.length + 2));
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
      // TODO: make date buffers dynamic to range of data
      .domain([d3.min(data, function(d) {date = new Date(parseDate(d.date)); return date.setDate(date.getDate() - 1); }),
               d3.max(data, function(d) {date = new Date(parseDate(d.date)); return date.setDate(date.getDate() + 1); })
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
          .attr('x', function(d) { return x(new Date(parseDate(d.data.date))) - bar_width / 2; })
          .attr('width', bar_width)
          .attr('y', function(d) {
            // remember that SVG is y-down while our graph is y-up!
            // here, we set the top-left of this bar segment to the
            // larger value of the pair
            return y(d[1]);
          })
          .attr('height', function(d) {
            // since we are drawing our bar from the top downwards,
            // the length of the bar is the distance between our points
            return y(d[0]) - y(d[1]);
          })
          .on("mouseover", function() {
            chart.select(".tooltip").transition().delay(2).style("opacity", 1)
            })
          .on("mouseout", function() {
            chart.select(".tooltip").transition().delay(2).style("opacity", 0);
            })
          .on("mousemove", function(d) {
            var xPosition = d3.mouse(this)[0] - 15;
            var yPosition = y(d[1]);
            var cur_date = new Date(parseDate(d.data.date));
            var tool_text = '';
            for (var k in data_keys) {
                if (d.data[data_keys[k]] != null) {
                    t = data_keys[k] + ": " + d.data[data_keys[k]] + " " + yAxisTitle + "<br>";
                    tool_text += t;
                }
            }
            tooltip.style("left", xPosition + 'px');
            tooltip.style("top", yPosition + 'px');
            tooltip.select("div.tooltip-title").text(dateFormat(cur_date));
            tooltip.select("div.tooltip-text").html(tool_text);
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

    // Prep the tooltip bits, initial display is hidden
    var tooltip = chart.append("div")
      .attr("class", "tooltip")
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
