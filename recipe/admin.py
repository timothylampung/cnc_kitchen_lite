from django.contrib import admin

# Register your models here.
from recipe.models import Recipe, SubStep, Step

admin.site.register(Recipe)
admin.site.register(Step)
admin.site.register(SubStep)
