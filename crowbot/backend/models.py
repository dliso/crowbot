from django.db import models

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

class User(models.Model):
    """
    Placeholder User model.
    """

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
    )
    course = models.ForeignKey(
        Course,
        on_delete = models.SET_NULL,
        null = True,
    )
    creation_datetime = models.DateTimeField(auto_now_add = True)
    text = models.TextField()

class Answer(models.Model):
    """
    Answers to questions.
    """
    question = models.ForeignKey(
        Question,
        on_delete = models.SET_NULL,
        null = True,
    )
    user_id = models.ForeignKey(
        User,
        on_delete = models.SET_NULL,
        null = True,
    )
    creation_datetime = models.DateTimeField(auto_now_add = True)
    text = models.TextField()

