// This file is loaded and executed when the main Crowbot page is opened.

let FEEDITEMTYPE = {
    question            : 'Question',
    questionWithAnswers : 'QuestionWithAnswers',
    faq                 : 'FAQ',
    info                : 'Info',
    highlyRated         : 'HighlyRated'
};

let USERTYPE = {
    bot        : 'Bot',
    instructor : 'Instructor',
    student    : 'Student',
    anonymous  : 'Anonymous'
};


let ANSWERVOTE = {
    none : 'none',
    up   : 'up',
    down : 'down'
};

let MESSAGETYPE = {
    botResponse    : 'BotResponse',
    storedQuestion : 'StoredQuestion',
    storedAnswer   : 'StoredAnswer'
};

class Message {
    constructor(message) {
        this.msgBody = message.body;
        if (message.msgBody) {
            this.msgBody = message.msgBody;
        }
        this.ownMessage = message.ownMessage;
    }

    makeLi() {
        let li = $('<li/>')
                .append(this.msgBody);
        return li;
    }
}

class ListManager {

    constructor(listID){  //f.eks question-queue
        this.list = listID;
    }

    addItem(item) {
        this.list.append(item);
    }

    appendText(content, cssClasses){ //cssClasses er ei liste.
        var li = $("<li/>").text(content).addClass(cssClasses.join(" ")); // lager liste-element med klasser.
        this.list.append(li);
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
            var text = this.randomBirdSound() + ' ' + text;
            var task = "play";
        }

        //Hvis svaret er lagt inn av anon:
        else if (username == undefined || username == "" || username == "Unknown"){
            subtext = timestamp.substring(0,10) + " " + timestamp.substring(11,16);
            var task = "stop";
        }

        //Hvis svaret er lagt inn av usertype 'instructor' eller 'student':
        else{
            subtext = "Answer by " + usertype + " " + username + " " + "[" + timestamp.substring(0,10)
                + " " + timestamp.substring(11,16) + "]";
               var task = "stop";
        }
        $(".crowsound").trigger('play');
        this.play_audio(task);
        this.appendWithSubtext(text, subtext, cssClasses);
    }

    play_audio(task) {
        if (task == 'play') {
            $(".crowsound").trigger('play');
        }
        if (task == 'stop') {
            $(".crowsound").trigger('pause');
            $(".crowsound").prop("currentTime", 0);
        }
    }

    randomBirdSound() {
        var birdSounds = ['Caw caw!', 'Squawk!', 'Chirp chirp!', ''];
        var sound = '';
        if (Math.random(0,10) < 2) {
            sound = birdSounds[Math.floor(Math.random() * birdSounds.length)];
        }
        return sound;
    }

}

function prettyDatetime(datetime) { //brukes ikke
    return "[" + datetime.substring(0,10) + " " + datetime.substring(11,16) + "]";
}



$( document).ready(function(){

    msgBox = document.getElementById("message-box");

    function updateScroll(element) {
        element.scrollTop = element.scrollHeight;
    }

    //RegEx pattern for q_pk (question primary key)
    let primaryKeyRegex = /\#[0-9]+/g;

    msgListManager = new ListManager($("#message-box"));

    //When a user writes in the box and clicks send, the user input is appended to the list
    $( "#message-form" ).submit(function( event ) {

        //Finds user input and appends it
        var input = $( "#user-input").val();
        if (input !== "") {
            userMessage = new Message({msgBody: input, ownMessage: true});
            msgListManager.addItem(
                userMessage.makeLi()
                    .addClass('message user-msg')
            );
            updateScroll(msgBox);

            if (input.startsWith("#")){
                var regexArray = input.match(primaryKeyRegex);
                var q_pk = regexArray[0].substring(1); //Removes the '#'
                let submit_answer_route = "/api/submit_answer/";
                $.post(submit_answer_route, {q_pk: q_pk, body: input})
                    .then(function(conf){ //conf = confirmation that the bot received the instructors answer
                        let message = new Message(conf);
                        msgListManager.addItem(message.makeLi().addClass('message bot-msg'));
                        updateScroll(msgBox);
                    });
            } else {
                let ask_question_route = '/api/ask_question';
                $.post(ask_question_route, {body: input})
                    .then(function (messages) {
                    for(message of messages) {
                        message.ownMessage = false;
                        message = new Message(message);
                        msgListManager.addItem(
                            message.makeLi().addClass('message bot-msg')
                        );
                        updateScroll(msgBox);
                    }
                });
            }
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

    function populateFeed(courseList) {
        let feedContainer = $('#feed-container');
        let feedToggles = $('#feed-toggles');
        for (courseId of courseList) {
            let checkbox = $('<input />', {type: 'checkbox', id: 'cb-'+courseId, checked: true});
            let label = $('<label/>', {'for': 'cb-'+courseId, text: courseId.toUpperCase()})
                    .css('border', '1px solid #c00000')
                    .css('margin', '1px')
                    .css('padding', '2px');
            feedToggles.append(checkbox);
            feedToggles.append(label);
        }
    }

    $.getJSON('/api/my_courses/').then(populateFeed);
    $.getJSON('/api/my_feed/').then(function(data) {
        for(d of data) {
            let itemType, itemContent;
            ({itemType, itemContent} = d);
            console.log(itemType);
            console.log(itemContent);
        }
    });

});
