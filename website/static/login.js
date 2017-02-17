
var HttpClient = function() {
    this.get = function(aUrl, aCallback) {
        var anHttpRequest = new XMLHttpRequest();
        anHttpRequest.onreadystatechange = function() {
            if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                aCallback(anHttpRequest.responseText);
        }

        anHttpRequest.open( "GET", aUrl, true );
        anHttpRequest.send( null );
    }
}

function render_login(class_to_render) {
    // Get the modal
    var popUpDiv = document.createElement('div');
    popUpDiv.setAttribute("id", "login-popup");
    popUpDiv.setAttribute("class", "popup");
    popUpDiv.setAttribute("style", "display: block");

    var client = new HttpClient;
    client.get('/login', function(response) {
        var content = document.createElement('div');
        content.innerHTML = response;

        var popUpContentDiv = document.createElement('div');
        popUpContentDiv.setAttribute("class", "popup-content");

        var content_html = content.getElementsByClassName("page")[0];
        popUpContentDiv.appendChild(content_html);
        popUpDiv.appendChild(popUpContentDiv);
        document.body.appendChild(popUpDiv);
    });

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target.id == "login-popup") {
            event.target.outerHTML = "";
            delete event.target;
        }
    }

}