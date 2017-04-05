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
        this.courseId = message.courseId;
        this.msgType = message.msgType;
        this.user = message.user;
        this.pk = message.pk;
        this.askedCount = message.askedCount;
        this.thisUserAsked = message.thisUserAsked;
        this.score = message.score;
    }

}

class FeedItem extends Message {
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
        let li = this.makeQuestionLi();
        li.addClass('feed-indent feed-reply');
        return li;
    }

    makeQuestionLi() {
        let li = $('<li/>');

        let elements = this.makeElements();

        li.addClass('flex-container');
        li.css('justify-content', 'space-between');

        let left = $('<div/>');
        left.append(elements.topDecoration);
        left.append(elements.content);
        left.append(elements.infoLine);

        let right = $('<div/>');
        right.append(elements.buttons);

        li.append(left);
        li.append(right);

        li.addClass('feed-item');
        return li;
    }

    makeElements() {
        /* Make the elements that go into the DOM representations of items. These
           are:
           - The actual message
           - Info line
             - Username, timestamp, course code
             - Question ID, if `this` is a question
           - Voting buttons, if `this` is an answer
           - +1 button, if `this` is a question
          */
        let elements = {};

        let content = $('<div/>');
        content.append(this.msgBody);
        content.addClass('message-content');
        elements.content = content;

        let infoLine = $('<div/>');
        let prettyTime = '2017-Feb-04 12:34';
        infoLine.append(`${this.user.name} ${prettyTime}`);
        elements.infoLine = infoLine;
        infoLine.addClass('info-line');

        let topDecoration = $('<div/>');
        topDecoration.append(`${this.msgType} #${this.pk}`);
        topDecoration.addClass('info-line')
        elements.topDecoration = topDecoration;

        if (this.msgType == MESSAGETYPE.storedQuestion) {
            infoLine.append(` #${this.pk}`);
            let replyButton = $('<span/>', {text: ' reply'});
            replyButton.attr('data-toggle', 'modal');
            replyButton.attr('data-target', '#answer-modal');
            replyButton.click(e => {
                $('#modal-question-pk').html(this.pk);
                $('#modal-question-text').html(this.msgBody);
                $('#answer-modal-submit').attr('data-question-pk', this.pk);
            })
            infoLine.append(replyButton);

            let buttons = $('<div/>');
            let plusOne = $('<input/>', {type: 'checkbox', value: this.thisUserAsked, id: `asked-toggle-${this.pk}`});
            plusOne.css('display', 'none');
            let plusOneLabel = $('<label/>', {'for': plusOne.attr('id'), text: '+1'});
            plusOneLabel.addClass('label-button');
            let counter = $('<div/>')
                .append(this.askedCount);
            plusOne.change(e => {
                let count = parseInt(counter.html(), 10);
                if ( plusOne.prop('checked') ) {
                    counter.html(count + 1);
                } else {
                    counter.html(count - 1);
                }
            })

            buttons
                .append(plusOne)
                .append(plusOneLabel)
                .append(counter);

            elements.buttons = buttons;
        }

        if (this.msgType == MESSAGETYPE.storedAnswer) {
            let buttons = $('<div/>');
            let upvote = $('<button/>').append('+1');
            let downvote = $('<button/>').append('-1');
            let score = $('<div/>').append(this.score);

            buttons
                .append(upvote)
                .append(score)
                .append(downvote);

            elements.buttons = buttons;
        }

        return elements;
    }
}

class ChatMessage extends FeedItem {
    makeLi() {
        let li = $('<li/>');

        if(!this.ownMessage) {
            // let elements = this.makeElements();
            // li.append(elements.topDecoration);
            return super.makeLi();
        }

        let content = $('<div/>');
        content.append(this.msgBody);

        let info = $('<div/>');
        info.addClass('info-line');
        if (this.user) {
            info.append(this.user.name)
        }
        if (this.timestamp) {
            info.append(this.timestamp)
        }

        li.append(content);
        li.append(info);
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
            let primaryKeyRegex = /\#([0-9]+) (.*)/;
            var regexArray = input.match(primaryKeyRegex);
            var q_pk = regexArray[1];
            let q_body = regexArray[2];
            console.log(regexArray);
            let submit_answer_route = "/api/submit_answer/";
            $.post(submit_answer_route, {q_pk: q_pk, body: q_body})
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
                        message = new ChatMessage(message);
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
            parent = new FeedItem(firstMessageRaw);
            new Message(firstMessageRaw);
            console.log(parent);
            let li = parent.makeLi();
            container.append(li);
            // li.addClass('message bot-msg');
            li.attr('data-courseId', parent.courseId);
            li.attr('data-msgType', parent.msgType);
            li.attr('data-pk', parent.pk);
            replies = [];
            for (rRaw of repliesRaw) {
                let r = new FeedItem(rRaw);
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

    $('#answer-modal-submit').click(e =>{
        let answer = $('#question-answer').val();
        let q_pk = $('#answer-modal-submit').attr('data-question-pk');
        // console.log(x);
        // console.log(answer);
        $.post('/api/submit_answer/', {
            q_pk: q_pk,
            body: answer
        })
    });

});
