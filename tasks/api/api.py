from django.conf.urls import url

from tasks.api.view import AddRecipeToTaskSet

urlpatterns = [
    url(r'^add-to-task-set/$', AddRecipeToTaskSet.as_view(), name='add_to_task_set'),
]
