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

class ChatMessage {
    constructor(message) {
        this.message = message;
        console.log(message);
    }

    makeLi() {
        let li = $('<li/>');
        li.append(this.message.msgBody);
        return li;
    }
}

class Message {
    constructor(message) {
        this.msgBody = message.body;
        if (message.msgBody) {
            this.msgBody = message.msgBody;
        }
        this.ownMessage = message.ownMessage;
        this.courseId = message.courseId;
        this.msgType = message.msgType;
        this.user = message.user;
        this.pk = message.pk;
        this.askedCount = message.askedCount;
        this.score = message.score;
    }

    makeLi() {
        let li;
        switch (this.msgType) {
        case MESSAGETYPE.storedAnswer:
            li = this.makeAnswerLi();
            break;
        case MESSAGETYPE.storedQuestion:
            li = this.makeQuestionLi();
            break;
        case MESSAGETYPE.botResponse:
            li = this.makeBotLi();
            break;
        }
        return li;
    }

    makeBotLi() {
        let li = $('<li/>');
        li.append(this.msgBody);
        return li;
    }

    makeAnswerLi() {
        let li = $('<li/>');
        let contentSpan = $('<span/>').append(this.msgBody);
        let symbolSpan = $('<span/>').append('!');
        let buttonSpan = $('<span/>').append('👍' + this.score + '👎');
        let content = $('<div/>')
                .append(symbolSpan)
                .append(contentSpan)
                .append(buttonSpan);
        let infoLine = $('<div/>')
                .append(this.user.name)
                .append(this.courseId)
                .css('font-size', '0.7em');
        li.append(content);
        li.append(infoLine);
        li.addClass('message');
        li.addClass('user-msg');
        return li;
    }

    makeQuestionLi() {
        let li = $('<li/>');
        let contentSpan = $('<span/>').append(this.msgBody);
        let symbolSpan = $('<span/>').append('?');
        let buttonSpan = $('<span/>').append('+1');
        buttonSpan.click(event => {
            $.post('/api/toggle_interest/', {pk: this.pk})
                .then(console.log);
        });
        let content = $('<div/>')
                .append(symbolSpan)
                .append(contentSpan)
                .append(buttonSpan);
        let infoLine = $('<div/>')
                .append(this.user.name + '. Asked ' + this.askedCount + ' times.')
                .append(this.courseId)
                .append(' #' + this.pk)
                .css('font-size', '0.7em');
        li.append(content);
        li.append(infoLine);
        li.addClass('message');
        li.addClass('bot-msg');
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

class FeedManager {
    constructor() {
        // this.container = feedContainer;
        this.header = $('#feed-toggles');
        this.items = $('#feed-items');
        this.manager = new ListManager($('#feed-items'));
        this.itemsByCourse = new Object();
    }

    addItem(item) {
        let li = $('<li/>');
        li.append(item.itemContent.msgBody);

        let courseId = item.itemContent.courseId;
        if(this.itemsByCourse[courseId] === undefined) {
            this.itemsByCourse[courseId] = [];
        }
        this.itemsByCourse[courseId].push(courseId);

        this.manager.addItem(li);
        console.log(this.itemsByCourse);
    }
}

function prettyDatetime(datetime) { //brukes ikke
    return "[" + datetime.substring(0,10) + " " + datetime.substring(11,16) + "]";
}

function hideCourses(courseId) {
    $(`#feed-items [data-courseId=${courseId}]`).hide();
}

function showCourses(courseId) {
    $(`#feed-items [data-courseId=${courseId}]`).show();
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
        event.preventDefault();
        if (input == '') {
            return;
        }
        userMessage = new ChatMessage({msgBody: input, ownMessage: true});
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
                    let message = new ChatMessage(conf);
                    msgListManager.addItem(message.makeLi().addClass('message bot-msg'));
                    updateScroll(msgBox);
                });
        } else {
            let ask_question_route = '/api/ask_question';
            $.post(ask_question_route, {body: input})
                .then(function (messages) {
                    for(message of messages) {
                        console.log('received:');
                        console.log(message);
                        // message.ownMessage = false;
                        message = new Message(message);
                        console.log('received:');
                        console.log(message);
                        msgListManager.addItem(
                            message.makeLi().addClass('message bot-msg')
                        );
                        updateScroll(msgBox);
                    }
                });
        }
    });

    // Submit when the user presses enter
    $("#user-input").keypress(function (key) {
        if (key.which == 13) {
            $("#message-form").submit();
            $("#user-input").val('');
            return false;
        }
    });

    function populateFeedCourseList(courseList) {
        let feedContainer = $('#feed-container');
        let feedToggles = $('#feed-toggles');
        for (courseId of courseList) {
            let checkbox = $('<input />', {type: 'checkbox', id: 'cb-'+courseId, checked: true});
            checkbox.attr('data-cb-courseId', courseId);
            checkbox.hide();
            checkbox.change(event => {
                if (event.currentTarget.checked) {
                    showCourses(checkbox.attr('data-cb-courseId'));
                } else {
                    hideCourses(checkbox.attr('data-cb-courseId'));
                }
            });
            let label = $('<label/>', {'for': 'cb-'+courseId, text: courseId});
            feedToggles.append(checkbox);
            feedToggles.append(label);
        }
    }

    function decorate(container, type) {
        return container;
    }

    function populateFeed(feedResponse) {
        let feed = $('#feed-items');
        for (item of feedResponse) {
            let itemType = item.itemType;
            let firstMessageRaw = item.firstMessage;
            let repliesRaw = item.replies;
            let container = $('<div/>');
            container = decorate(container, itemType);
            parent = new Message(firstMessageRaw);
            console.log(parent);
            let li = parent.makeLi();
            container.append(li);
            // li.addClass('message bot-msg');
            li.attr('data-courseId', parent.courseId);
            li.attr('data-msgType', parent.msgType);
            li.attr('data-pk', parent.pk);
            replies = [];
            for (rRaw of repliesRaw) {
                let r = new Message(rRaw);
                let li = r.makeLi();
                li.attr('data-courseId', r.courseId);
                li.attr('data-msgType', r.msgType);
                li.attr('data-pk', r.pk);
                container.append(li);
            }
            feed.append(container);
        }
    }

    $.getJSON('/api/my_courses/').then(populateFeedCourseList);
    $.getJSON('/api/my_feed/').then(populateFeed);

});
