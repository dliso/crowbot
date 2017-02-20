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
