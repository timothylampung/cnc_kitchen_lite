from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from tasks.views import TaskListView, TaskDeleteView, TaskCreateView

urlpatterns = [
    path('', TaskListView.as_view(), name='task_set'),
    path('delete/<pk>/', TaskDeleteView.as_view(), name='tasks-delete'),
    path('create/', TaskCreateView.as_view(), name='tasks-create'),
    path("api/", include("tasks.api.api")),  # UI Kits Html files,

]
