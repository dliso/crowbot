from django.db import models

# Create your models here.

class UserQuery(models.Model):
    query_text = models.CharField(max_length=500)

    def __str__(self):
        return self.query_text[:50]
