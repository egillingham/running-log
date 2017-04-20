
function add_background_image(image_url) {
    // add background image class to body
    var body = document.getElementsByTagName("body")[0];
    body.setAttribute("class", "b-image");
    // add background image
    body.setAttribute("style", "background-image: url(" + image_url + ")");
}

function parseDate(date) {
  const parsed = Date.parse(date);
  if (!isNaN(parsed)) {
    return parsed;
  }

  return Date.parse(date.replace(/-/g, '/').replace(/[a-z]+/gi, ' '));
}

function render_charts(chart_data) {
    for (i = 0; i < chart_data.length; i++) {
        chart = chart_data[i];
        if (chart['chart_type'] == 'stacked_bar') {
            stackedBar(chart['data'], 'div.chart-' + chart['id'], chart['axis_title'], chart['chart_height'], chart['chart_width']);
        } else if (chart['chart_type'] == 'bar_chart') {
            barChart(chart['data'], 'div.chart-' + chart['id'], chart['axis_title'], chart['chart_height'], chart['chart_width']);
        }
    }
}