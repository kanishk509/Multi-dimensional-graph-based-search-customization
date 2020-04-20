var max_y = 0

function updateScroll() {
    var doc = document, w = window;
    var x, y, docEl;
    
    if ( typeof w.pageYOffset === 'number' ) {
        x = w.pageXOffset;
		y = w.pageYOffset;
    } else {
        docEl = (doc.compatMode && doc.compatMode === 'CSS1Compat')? doc.documentElement: doc.body;
        x = docEl.scrollLeft;
		y = docEl.scrollTop;
    }
	
	if(y > max_y)
		max_y = y;
}

window.addEventListener("scroll", updateScroll);

window.addEventListener("blur", function () {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function () {
		if (this.readyState == 4 && this.status == 200) {
			console.log(this.responseText);
		}
	};
	xhttp.open("POST", "http://127.0.0.1:5000/scroll_update");
	xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
	xhttp.send(JSON.stringify({"url": this.window.location.href, "scroll_dist": max_y}));
	//xhttp.send(JSON.stringify({"scroll_dist": y_scroll}));
	//xhttp.send("hello")
})