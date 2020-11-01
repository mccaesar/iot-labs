
// send data to python backend
function to_server(message){
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

// get data from the surver
function from_server() {

    $.getJSON('http://127.0.0.1:5000/', {}, function(server_message) { 
        // get the server message
        var greet = server_message.server_greet;
        document.getElementById("greet_from_server").innerHTML = greet;
    });

}

function greeting(){

    // get the element from html
    var name = document.getElementById("myName").value;
    // update the content in html
    document.getElementById("greet").innerHTML = "Hello " + name + " !";
    // send the data to the server 
    to_server(name);
    from_server();

}
