// This file is loaded and executed when the main Crowbot page is opened.

class ListManager {

    constructor(listID){  //f.eks question-queue
        this.list = listID;
    }

    addItem(content, cssClasses){ //cssClasses er ei liste.
        var li = $("<li/>").text(content).addClass(cssClasses.join(" ")); // lager liste-element med klasser.
        this.list.append(li)
    }
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

    /* // Jeg erstattet denne funkjsonen med en som tar inn msgBox som parameter. Begge funker likt.
    msgBox = document.getElementById("message-box");
    function updateScroll() {
        msgBox.scrollTop = msgBox.scrollHeight;
    }
    */

    msgBox = document.getElementById("message-box");

    function updateScroll(element) {
        element.scrollTop = element.scrollHeight;
    }


/*    msgList = $("#message-box");
    function addMessage(msg, botOrUser) { // Jeg erstattet denne funkjsonen med den i klassen ListManager
        msgList.append(
            $(`<li>${msg}</li>`)
                .addClass(botOrUser === 'bot' ? 'bot-msg' : 'user-msg')
                .addClass('message')
        );
    }*/

    msgListManager = new ListManager($("#message-box"));

    //When a user writes in the box and clicks send, the user input is appended to the list
    $( "#message-form" ).submit(function( event ) {

        //Finds user input and appends it
        var input = $( "#user-input").val();
        //input_html = "<li class='message user-msg'>" + input + "</li>"; // Jeg kommenterte denne ut fordi det virker ikke som den brukes.
        msgListManager.addItem(input, ['user-msg', 'message']);
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
        }).then(function(data){
            console.log(data);
            var output = data.body;
            console.log(output);
            message = randomBirdSound() + ' ' + output;
            if (message.slice(-1) != '.') {
                message += '.';
            }
            msgListManager.addItem(message, ['bot-msg', 'message']);
            updateScroll(msgBox);
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

    qListManager = new ListManager($("#question-queue"));

    /*questionList = $("#question-queue");
    function addQuestion(question) {
        questionList.append(
            $(question)
        );
    }*/

    function questionQueueString(datetime, question) {
        //return "<li>" + "Question: " + question  + " Time: " + datetime + "</li>"
        return "[" + datetime.substring(0,10) + " " + datetime.substring(11,16) + "] " + question;
    }

    var q_list_root = '/api/question_queue';

    function addQuestionsToList(course_code){
        $.ajax({
        //Get the question
            url: q_list_root + "/" + course_code,
            method: "GET"
        }).then(function(questions){
            for (q of questions){
                var content = questionQueueString(q.datetime, q.text);
                qListManager.addItem(content, []);
            }
        });
    }

    addQuestionsToList("TDT4100");

    questionList2 = new ListManager($("#question-queue"));
    questionList2.addItem("hei",["bot-msg","test", "message"]);

});
