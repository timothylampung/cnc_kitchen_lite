from django.contrib import admin

# Register your models here.
from ingredients.models import Ingredient, Coordinates

admin.site.register(Ingredient)
admin.site.register(Coordinates)
