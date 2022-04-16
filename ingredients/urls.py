from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from ingredients.views import (IngredientListView,
                               IngredientDetailView,
                               IngredientCreateView,
                               IngredientDeleteView,
                               IngredientUpdateView
                               )

urlpatterns = [
    path('', IngredientListView.as_view(), name='ingredients-list'),
    path('detail/<pk>/', IngredientDetailView.as_view(), name='ingredients-detail'),
    path('delete/<pk>/', IngredientDeleteView.as_view(), name='ingredients-delete'),
    path('update/<pk>/', IngredientUpdateView.as_view(), name='ingredients-update'),
    path('create/', IngredientCreateView.as_view(), name='ingredients-create'),

]
