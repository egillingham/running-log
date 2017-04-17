
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