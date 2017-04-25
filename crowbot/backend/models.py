from django.db import models
from django.contrib.auth.models import User

from api import answervote
from api.messagetype import *
from api.answervote import *

# Create your models here.

class Course(models.Model):
    code = models.CharField(max_length=15)
    name = models.CharField(max_length=100)
    recommended_previous_knowledge = models.CharField(max_length=500)
    required_previous_knowledge = models.CharField(max_length=500)
    exam_date = models.DateField(null=True)
    exam_support_code = models.CharField(max_length=10)
    exam_support_name = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    semester = models.CharField(max_length=10)
    teacher_name = models.CharField(max_length=100)
    teacher_email = models.CharField(max_length=100)
    ects_credits = models.DecimalField(max_digits=4, decimal_places=2, null=True)

    def __str__(self):
        return ','.join([self.code, self.name])

class Book(models.Model):
    name = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)

class Room(models.Model):
    location = models.CharField(max_length=50)

class Semester(models.Model):
    """
    """
    start_date = models.DateField()

class Question(models.Model):
    """
    Model for storing questions that the bot couldn't answer on its own. These will be added to a course's queue and
    shown to a human who can answer it.
    """
    user_id = models.ForeignKey(
        User,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
    )
    course = models.ForeignKey(
        Course,
        on_delete = models.SET_NULL,
        null = True,
    )
    semester = models.ForeignKey(
        Semester,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
    )
    creation_datetime = models.DateTimeField(auto_now_add = True)
    text = models.TextField()
    lemma = models.BinaryField()
    interested_users = models.ManyToManyField(User, related_name='interested_in',
                                              blank=True)

    def did_user_ask(self, user):
        if not user:
            was_interested = False
        else:
            was_interested = False if self.interested_users.filter(id = user.id).count() == 0 else True
        return was_interested

    def times_asked(self):
        return self.interested_users.count()

    def __str__(self):
        return str((self.creation_datetime, self.text))

    def to_dict(self, asking_user):
        profile = self.user_id.profile if self.user_id else None
        return {
            'user': profile.to_dict() if profile else None,
            'ownMessage': asking_user == self.user_id,
            'timestamp': self.creation_datetime,
            'msgBody': self.text,
            'courseId': self.course.code,
            'pk': self.id,
            'thisUserAsked': self.did_user_ask(profile.user) if profile else False,
            'askedCount': self.interested_users.count(),
            'msgType': MESSAGETYPE.stored_question,
        }

class Answer(models.Model):
    """
    Answers to questions.
    """
    question = models.ForeignKey(
        Question,
        on_delete = models.SET_NULL,
        null = True,
        related_name = 'answers',
        blank = True,
    )
    user_id = models.ForeignKey(
        User,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
    )
    creation_datetime = models.DateTimeField(auto_now_add = True)
    text = models.TextField()
    upvoted_by = models.ManyToManyField(User, related_name='upvoted',
                                        blank=True)
    downvoted_by = models.ManyToManyField(User, related_name='downvoted',
                                          blank=True)

    def score(self):
        return self.upvoted_by.count() - self.downvoted_by.count()

    def user_voted(self, user):
        if not user:
            pass
        elif self.upvoted_by.filter(id = user.id).count() == 1:
            return answervote.ANSWERVOTE.up
        elif self.downvoted_by.filter(id = user.id).count() == 1:
            return answervote.ANSWERVOTE.down
        return answervote.ANSWERVOTE.none

    def vote(self, user, button):
        # button: ANSWERVOTE.up | ANSWERVOTE.down
        old_vote = self.user_voted(user)
        if button == ANSWERVOTE.up:
            if old_vote == ANSWERVOTE.up:
                self.upvoted_by.remove(user)
            elif old_vote == ANSWERVOTE.down:
                self.downvoted_by.remove(user)
                self.upvoted_by.add(user)
            elif old_vote == ANSWERVOTE.none:
                self.upvoted_by.add(user)
        elif button == ANSWERVOTE.down:
            if old_vote == ANSWERVOTE.up:
                self.upvoted_by.remove(user)
                self.downvoted_by.add(user)
            elif old_vote == ANSWERVOTE.down:
                self.downvoted_by.remove(user)
            elif old_vote == ANSWERVOTE.none:
                self.downvoted_by.add(user)
        else:
            raise ValueError("'vote' must be one of 'up' or 'down'")
        return self.user_voted(user)

    def to_dict(self, asking_user):
        profile = self.user_id.profile if self.user_id else None
        return {
            'user': profile.to_dict() if profile else None,
            'ownMessage': self.user_id == asking_user,
            'timestamp': self.creation_datetime,
            'msgBody': self.text,
            'courseId': self.question.course.code,
            'pk': self.id,
            'score': self.score(),
            'thisUserVoted': self.user_voted(asking_user),
            'msgType': MESSAGETYPE.stored_answer,
        }

class ChatLog(models.Model):
    """Either a plain text message, a stored question, or a stored answer."""
    user_id = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        null = False,
        related_name = 'chatlog'
    )
    timestamp = models.DateTimeField(auto_now_add = True)
    plain_user = models.TextField(null = True)
    plain_bot = models.TextField(null = True)
    question = models.ForeignKey(
        Question,
        on_delete = models.SET_NULL,
        null = True
    )
    answer = models.ForeignKey(
        Answer,
        on_delete = models.SET_NULL,
        null = True
    )

    @classmethod
    def record_user_message(cls, text, user):
        print('Recording user message')
        if isinstance(user, User):
            log_entry = ChatLog(
                user_id = user,
                plain_user = text,
            )
            log_entry.save()
            print(log_entry.user_id)
            print(log_entry.timestamp)
            print(log_entry.plain_user)

    @classmethod
    def record_stored_object(cls, message, user):
        # print('Recording bot response')
        # print(user)
        # print(message['msgType'])
        # print(message)
        if isinstance(user, User):
            msg_type = message['msgType']
            if msg_type == MESSAGETYPE.bot_response:
                print('Recording bot response')
                msg = cls(
                    user_id=user,
                    plain_bot=message['msgBody']
                )
                msg.save()
            if msg_type == MESSAGETYPE.stored_answer:
                print('Recording stored answer')
                pk = message['pk']
                msg = cls(
                    user_id = user,
                    answer = Answer.objects.get(pk=pk)
                )
                msg.save()
                print(msg.answer)
            if msg_type == MESSAGETYPE.stored_question:
                print('Recording stored question')
                pk = message['pk']
                msg = cls(
                    user_id = user,
                    question = Question.objects.get(pk=pk)
                )
                msg.save()
                print(msg.question)

    @classmethod
    def record_message(self, message):
        print('Recording message in DB:')
        print(message)
        pass

    def format(self, user):
        res = {}
        res['user'] = self.user_id.profile.to_dict()
        if self.plain_user:
            res['msgType'] = MESSAGETYPE.user_message
            res['msgBody'] = self.plain_user
            res['timestamp'] = self.timestamp
            res['ownMessage'] = True
        if self.plain_bot:
            res['msgType'] = MESSAGETYPE.bot_response
            res['msgBody'] = self.plain_bot
            res['timestamp'] = self.timestamp
            res['ownMessage'] = False
        if self.answer:
            res = self.answer.to_dict(user)
        if self.question:
            res = self.question.to_dict(user)
        return res

    def get(self, num_msgs = 10):
        pass
