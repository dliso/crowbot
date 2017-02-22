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


    //Changes color of the list
    $( "#message-box").css("color","blue");

    //Adds the word "Hei" to the lists
    $( "#message-box").append("<li>Hei</li>");

    var xhttp = new XMLHttpRequest();
    //scooterlabs.com/echo
   //// xhttp.open("POST", "http://scooterlabs.com/echo", true);

    $.ajax({
        url: root + '/posts',
        method: "POST",
        data: {
            title: "foo",
            body: "bar",
            userId: 1
        }
        //dataType: "jsonp"
    }).then(function(data){
        console.log(data)
    });


    //When a user writes in the box and clicks send, the user input is appended to the list
    $( "#message-form" ).submit(function( event ) {
        var input = $( "#user-input").val();
        input = "<li>" + input + "</li>";
        $( "#message-box").append(input);

        $.ajax({
            url: root + '/posts',
            method: "POST",
            data: {

                body: input

            }
            //dataType: "jsonp"
        }).then(function(data){
            console.log(data)
        });

        //xhttp.send(input);
        //var echo = xhttp.response();
        //console.log("The echo" + echo);


        //legg til responsen i lista

        event.preventDefault();
    });




    $( "#message-box").append($( "#textarea").val());

})