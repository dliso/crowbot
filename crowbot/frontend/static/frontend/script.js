// This file is loaded and executed when the main Crowbot page is opened.

$( document).ready(function(){



    console.log('Hello, World');

    // jQuery example:
    var root = 'https://jsonplaceholder.typicode.com';

    $.ajax({
        url: root + '/posts/1',
        method: 'GET'
    }).then(function(data) {
        console.log(data);
    });


    //Changes color of the list:
    //$( '#message-box').css("color","blue");

    //Adds the word "Hei" to the lists:
    //$( "#message-box").append("<li>Hei</li>");

    //Creates a new XMLHttpRequest-object but we're not using it. Yet.
    //var xhttp = new XMLHttpRequest();

    // http://scooterlabs.com/echo is the url of an "echoing site",
    // but we're not using it and I don't even know if the code works.
    // xhttp.open("POST", "http://scooterlabs.com/echo", true);

    //Another jQuery example:
    $.ajax({
        url: root + '/posts', //URL
        method: "POST", //POST or GET etc...
        data: {
            title: "foo",
            body: "bar",
            userId: 1
        }
        //dataType: "jsonp"
    }).then(function(data){ //"then" waits for the response and executes the function when it arrives.
        console.log(data)
    });


    //When a user writes in the box and clicks send, the user input is appended to the list
    $( "#message-form" ).submit(function( event ) {

        //Finds user input and appends it
        var input = $( "#user-input").val();
        input = "<li>" + input + "</li>";
        $( "#message-box").append(input);

        //Sends input to URL
        $.ajax({
            url: root + '/posts',
            method: "POST",
            data: {
                body: input
            }
        //Gets the input back and appends it to the list
        }).then(function(data){
            console.log(data);
            //var data = JSON.parse(data);
            var output = data.body;
            console.log(output);
            $( "#message-box").append("Caw caw " + output);
        });
        //preventDefault prevents the site from updating. I think.
        event.preventDefault();
    });




});