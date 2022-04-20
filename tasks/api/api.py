from django.conf.urls import url

from tasks.api.view import AddRecipeToTaskSet, QuickAddRecipeToTaskQueue, RunSetOnModule

urlpatterns = [
    url(r'^add-to-task-set/$', AddRecipeToTaskSet.as_view(), name='add_to_task_set'),
    url(r'^quick-add-to-task-queue/$', QuickAddRecipeToTaskQueue.as_view(), name='quick_add_to_task_queue'),
    url(r'^run-set/$', RunSetOnModule.as_view(), name='quick_add_to_task_queue'),
]
