
function add_background_image(image_url) {
    // add background image class to body
    var body = document.getElementsByTagName("body")[0];
    body.setAttribute("class", "b-image");
    // add background image
    body.setAttribute("style", "background-image: url(" + image_url + ")");
}