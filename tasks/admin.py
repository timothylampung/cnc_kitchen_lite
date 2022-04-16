from django.contrib import admin

# Register your models here.
from tasks.models import TaskSet

admin.site.register(TaskSet)
