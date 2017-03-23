// This file is loaded and executed when the main Crowbot page is opened.

class ListManager {

    constructor(listID){  //f.eks question-queue
        this.list = listID;
    }

    appendText(content, cssClasses){ //cssClasses er ei liste.
        var li = $("<li/>").text(content).addClass(cssClasses.join(" ")); // lager liste-element med klasser.
        this.list.append(li)
    }

    appendWithSubtext(maintext, subtext, cssClasses){
        var listItem = $('<li/>')
            .append($('<div/>', {text: maintext}))
            .append($('<div/>', {text: subtext}).css('font-size', '10px'))
            .addClass(cssClasses.join(" ")); // lager liste-element med klasser.
        this.list.append(listItem);
    }

    addPendingQuestion(text, timestamp, number){
        var subtext = timestamp.substring(0,10) + " " + timestamp.substring(11,16) + " #" + number;
        this.appendWithSubtext(text, subtext, ["question-item"]);
    }

    chatReply(text, usertype, username, timestamp, cssClasses){
        var subtext = "";

        //Når Crowbot svarer (dvs. svaret kommer automatisk fra API.AI-boten:
        if (username == "Crowbot"){
            subtext = "Answer by " + username; //Vi gidder ikke ha med "bot" og tid når Crowbot svarer
        }

        //Hvis svaret er lagt inn av anon:
        else if (username == undefined || username == "" || username == "Unknown"){
            subtext = timestamp.substring(0,10) + " " + timestamp.substring(11,16);
        }

        //Hvis svaret er lagt inn av usertype 'instructor' eller 'student':
        else{
            subtext = "Answer by " + usertype + " " + username + " " + "[" + timestamp.substring(0,10)
                + " " + timestamp.substring(11,16) + "]";
        }
        this.appendWithSubtext(text, subtext, cssClasses);
    }

/*    addToListWithTimeAndUser(text, usertype, username, timestamp, cssClasses, number){
        var subtext = "";
        if (username == "Crowbot") {
            subtext = "Answer by " + username; //Vi gidder ikke ha med "bot" og tid når Crowbot svarer
        }
        else if (username == undefined || username == "" || username == "Unknown"){
            subtext = timestamp.substring(0,10) + " " + timestamp.substring(11,16);
            if (number != null){
                subtext += " id = " + number;
            }
        }
        else{
            subtext = "Answer by " + usertype + " " + username + " " + "[" + timestamp.substring(0,10)
                + " " + timestamp.substring(11,16) + "]";
        }
        var listItem = $('<li/>')
            .append($('<div/>', {text: text}))
            .append($('<div/>', {text: subtext}).css('font-size', '10px'));
        var li = listItem.addClass(cssClasses.join(" ")); // lager liste-element med klasser.

        this.list.append(li);
   }*/



/*   //content is a list item.
    addListItemToList(content, cssClasses){ //cssClasses er ei liste.
        var li = content.addClass(cssClasses.join(" ")); // lager liste-element med klasser.
        this.list.append(li);
    }*/

}

function prettyDatetime(datetime) { //brukes ikke
    return "[" + datetime.substring(0,10) + " " + datetime.substring(11,16) + "]";
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
    // $.ajax({
    //     url: root + '/posts', //URL
    //     method: "POST", //POST or GET etc...
    //     data: {
    //         title: "foo",
    //         body: "bar",
    //         userId: 1
    //     }
    //     //dataType: "jsonp"
    // }).then(function(data){ //"then" waits for the response and executes the function when it arrives.
    //     console.log(data)
    // });

    msgBox = document.getElementById("message-box");

    function updateScroll(element) {
        element.scrollTop = element.scrollHeight;
    }

    //RegEx pattern for q_pk (question primary key)
    var re = /\#[0-9]+/g;

    msgListManager = new ListManager($("#message-box"));

    //When a user writes in the box and clicks send, the user input is appended to the list
    $( "#message-form" ).submit(function( event ) {

        //Finds user input and appends it
        var input = $( "#user-input").val();
        //input_html = "<li class='message user-msg'>" + input + "</li>"; // Jeg kommenterte denne ut fordi det virker ikke som den brukes.
        msgListManager.appendText(input, ['user-msg', 'message']);
        updateScroll(msgBox);

        if (input.startsWith("#")){
            var regexArray = input.match(re);
            var q_pk = regexArray[0].substring(1); //Removes the '#'
            //console.log(q_pk);
            root = "/api/submit_answer/";
            $.ajax({
                url: root,
                method: "POST",
                data: {
                body: input,
                q_pk: q_pk
            }
            }).then(function(conf){ //conf = confirmation that the bot received the instructors answer
                msgListManager.appendText(conf.body,['bot-msg', 'message']);
                updateScroll(msgBox);
            });

        } else {
            root = '/api/ask_question';

            //Sends input to URL
            $.ajax({
                url: root,
                method: "POST",
                data: {
                    body: input
                }
                //Gets the input back and appends it to the list
            }).then(function (data) {
                message = randomBirdSound() + ' ' + data.body;
                msgListManager.chatReply(message, data.usertype, data.username, data.timestamp,['bot-msg', 'message']);
                updateScroll(msgBox);
            });
        }
        //preventDefault prevents the site from updating.
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
                listmanager.addPendingQuestion(q.text,q.datetime,q.pk);
                //listmanager.addPendingQuestion(q.text,q.datetime, q.question_pk);
            }
        });
    }
    pendingQuestionList = new ListManager($("#question-queue"));

    addPendingQuestions("TDT4100", pendingQuestionList);

    $("#showPQs").click(function(){
        $("#PendingQs").toggle();
    });

    function displaySelectedPQs(course) {
        $('#'+course+"checkbox").click(function() {
        if($(this).is(":checked")) {
            $('#PendingQs-courselists').show();
            $('#'+course+"div").show();
            console.log("show");
        } else {
             $('#PendingQs-courselists').hide();
            $('#'+course+"div").hide();
            console.log("hide");
        }
        });
    }


    var fakeCourseList = ["TDT4100", "TTM4100", "TDT4140", "TDT4145"];

    function createCheckboxes(subscribed_courses) {
        $("#info").append("Select the courses you want to see the pending questions for.").css('font-size', '12px');

        for (course of subscribed_courses) {

            $("#checkboxes").append($('<input/>', {id: course + "checkbox", type: "checkbox", name: "course", value: "Courses"})).append(" " + course.toUpperCase()).append($('<br>'));

            $("#PendingQs-courselists").append($('<ul/>', {id: course + "list"}).addClass("question-list"));

            lm = new ListManager($("#" + course + "list"));
            addPendingQuestions(course, lm);
            displaySelectedPQs(course);
        }
    }

    $.ajax({
        url: '/api/my_courses/', //URL
        method: "GET"
    }).then(function(data){ //"then" waits for the response and executes the function when it arrives.
        var my_courses = data;
        createCheckboxes(my_courses);
    });


});
