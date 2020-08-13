document.onkeydown = updateKey;
document.onkeyup = resetKey;

// send data to python backend
function send_data(message){
    var data = $.ajax({
        url: "http://127.0.0.1:5000",
        type: "POST",
        data:JSON.stringify(message),    
        contentType: 'application/json;charset=UTF-8'
    });
    data.done(function(){
      ;
    })
  
}

// for detecting which key is been pressed w,a,s,d
function updateKey(e) {

    e = e || window.event;

    if (e.keyCode == '87') {
        // up (w)
        document.getElementById("upArrow").style.color = "green";
        send_data("87");
    }
    else if (e.keyCode == '83') {
        // down (s)
        document.getElementById("downArrow").style.color = "green";
        send_data("83");
    }
    else if (e.keyCode == '65') {
        // left (a)
        document.getElementById("leftArrow").style.color = "green";
        send_data("65");
    }
    else if (e.keyCode == '68') {
        // right (d)
        document.getElementById("rightArrow").style.color = "green";
        send_data("68");
    }
}

// reset the key to the start state 
function resetKey(e) {

    e = e || window.event;

    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";
}


// get the video frames from the opencv python backend
function get_frame() {

    $.getJSON('http://127.0.0.1:5000/', {}, function(py_backend) { 
        // update camera frames
        var frame = py_backend.frame;
        if (frame != "-"){
            var src = "data:image/png;base64, " + frame;
        }
        document.getElementById("pics").src = src;

        // update bluetooth return values
        var bluetooth_val = py_backend.bluetooth;
        document.getElementById("bluetooth").innerHTML = bluetooth_val;
    });

}

// update frame for every 50ms
function updateVideo(){
    setInterval(function(){
        get_frame();
    }, 50);
}
