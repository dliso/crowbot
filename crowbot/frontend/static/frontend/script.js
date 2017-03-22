// This file is loaded and executed when the main Crowbot page is opened.

class ListManager {

    constructor(listID){  //f.eks question-queue
        this.list = listID;
    }

    addTextToList(content, cssClasses){ //cssClasses er ei liste.
        var li = $("<li/>").text(content).addClass(cssClasses.join(" ")); // lager liste-element med klasser.
        this.list.append(li)
    }

    prettyDatetime(datetime) {
        return "[" + datetime.substring(0,10) + " " + datetime.substring(11,16) + "]";
    }

    addToListWithTimeAndUser(text, usertype, username, timestamp, cssClasses) {
        var subtext = "";
        if (username == "Crowbot") {
            subtext = "Answer by " + username; //Vi gidder ikke ha med "bot" og tid når Crowbot svarer
        }
        else if (username == undefined || username == "" || username == "Unknown"){
            subtext = timestamp.substring(0,10) + " " + timestamp.substring(11,16);
        }
        else{
            subtext = "Answer by " + usertype + " " + username + " " + "[" + timestamp.substring(0,10) + " " + timestamp.substring(11,16) + "]";
        }
        var listItem = $('<li/>')
            .append($('<div/>', {text: text}))
            .append($('<div/>', {text: subtext}).css('font-size', '10px'));
        var li = listItem.addClass(cssClasses.join(" ")); // lager liste-element med klasser.
        this.list.append(li);
   }

/*   //content is a list item.
    addListItemToList(content, cssClasses){ //cssClasses er ei liste.
        var li = content.addClass(cssClasses.join(" ")); // lager liste-element med klasser.
        this.list.append(li);
    }*/

}

let birdSounds = [
    'Caw caw!',
    'Squawk!',
    'Chirp chirp!',
    ''
];

function randomBirdSound() {
    let sound = '';
    if (Math.random(0,10) < 2) {
        sound = birdSounds[Math.floor(Math.random() * birdSounds.length)];
    }
    return sound;
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

    msgBox = document.getElementById("message-box");

    function updateScroll(element) {
        element.scrollTop = element.scrollHeight;
    }


    msgListManager = new ListManager($("#message-box"));

    //When a user writes in the box and clicks send, the user input is appended to the list
    $( "#message-form" ).submit(function( event ) {

        //Finds user input and appends it
        var input = $( "#user-input").val();
        //input_html = "<li class='message user-msg'>" + input + "</li>"; // Jeg kommenterte denne ut fordi det virker ikke som den brukes.
        msgListManager.addTextToList(input, ['user-msg', 'message']);
        updateScroll(msgBox);

        root = '/api/ask_question';

        //Sends input to URL
        $.ajax({
            url: root,
            method: "POST",
            data: {
                body: input
            }
        //Gets the input back and appends it to the list
        }).then(function(data_raw){
            if(Array.isArray(data_raw)) {
                data = data_raw;
            } else {
                data = [data_raw];
            }
            for(data of data) {
                console.log(data);
                var output = data.body;
                console.log(data.datetime);
                message = randomBirdSound() + ' ' + output;
                //msgListManager.addTextToList(message, ['bot-msg', 'message']);
                msgListManager.addToListWithTimeAndUser(message, data.usertype, data.username, data.timestamp,['bot-msg', 'message']);
                updateScroll(msgBox);
            }
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

    var q_list_root = '/api/question_queue';

    function addPendingQuestions(course_code, listmanager){
        $.ajax({
        //Get the question
            url: q_list_root + "/" + course_code,
            method: "GET"
        }).then(function(questions){
            for (q of questions){
                //var content = listmanager.prettyDatetime(q.datetime) + " " + q.text;
                listmanager.addToListWithTimeAndUser(q.text, "", "", q.datetime, []);
            }
        });
    }
    pendingQuestionList = new ListManager($("#question-queue"));

    addPendingQuestions("TDT4100", pendingQuestionList);

});
