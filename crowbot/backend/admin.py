from django.contrib import admin

from .models import *

admin.site.register(Course)
admin.site.register(Book)
admin.site.register(Room)
admin.site.register(Semester)
admin.site.register(Question)
admin.site.register(Answer)

# Register your models here.
