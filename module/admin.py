from django.contrib import admin

# Register your models here.
from module.models import Module
from recipe.models import Recipe

admin.site.register(Module)
