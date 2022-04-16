from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from recipe.views import (RecipeListView,
                          RecipeDetailView,
                          RecipeCreateView,
                          RecipeDeleteView, step_add
                          )

urlpatterns = [
    path('', RecipeListView.as_view(), name='recipes-list'),
    path('detail/<pk>/', RecipeDetailView.as_view(), name='recipes-detail'),
    path('delete/<pk>/', RecipeDeleteView.as_view(), name='recipes-delete'),
    path('create/', RecipeCreateView.as_view(), name='recipes-create'),
    path('add-step/', step_add, name='add-step'),
]
