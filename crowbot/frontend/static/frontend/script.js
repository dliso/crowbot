// This file is loaded and executed when the main Crowbot page is opened.

let birdSounds = [
    'Caw caw!',
    'Squawk!',
    '🐦',
    '🍰',
    'Chirp chirp!'
];

function randomBirdSound() {
    return birdSounds[Math.floor(Math.random() * birdSounds.length)];
}

$( document).ready(function(){

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
        input_html = "<li class='message user-msg'>" + input + "</li>";
        $( "#message-box").append(input_html);

        root = '/api/ask_question';

        //Sends input to URL
        $.ajax({
            url: root,
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
            $( "#message-box").append("<li class='message bot-msg'>" + randomBirdSound() + ' ' + output + ".</li>");
        });
        //preventDefault prevents the site from updating. I think.
        event.preventDefault();
    });

    // Submit when the user presses enter
    $("#user-input").keypress(function (key) {
        if (key.which == 13) {
            $("#message-form").submit();
            $("#user-input").val('');
            return false;
        }
    });


});
