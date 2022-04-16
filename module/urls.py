from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from module.views import (ModuleListView,
                          ModuleDetailView,
                          ModuleCreateView,
                          ModuleDeleteView,
                          )

urlpatterns = [
    path('', ModuleListView.as_view(), name='modules-list'),
    path('detail/<pk>/', ModuleDetailView.as_view(), name='modules-detail'),
    path('delete/<pk>/', ModuleDeleteView.as_view(), name='modules-delete'),
    path('create/', ModuleCreateView.as_view(), name='modules-create'),

]
