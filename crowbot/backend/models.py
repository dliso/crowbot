from django.db import models

# Create your models here.

class Course(models.Model):
    code = models.CharField(max_length=15)
    name = models.CharField(max_length=100)
    year = models.DateField()
    exam_date = models.DateField()
    exam_aids_code = models.CharField(max_length=10)
    exam_aids_name = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    semester = models.CharField(max_length=10)

class Book(models.Model):
    name = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)

class Room(models.Model):
    location = models.CharField(max_length=50)
