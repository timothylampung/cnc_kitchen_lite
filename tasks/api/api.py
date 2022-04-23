from django.conf.urls import url
from django.urls import path

from tasks.api.view import (AddRecipeToTaskSet,
                            QuickAddRecipeToTaskQueue,
                            RunSetOnModule,
                            GetQueuedTaskSet,
                            GetStartedTaskSet,
                            GetFailedTaskSet,
                            GetSuccessTaskSet, send_remote_data)

urlpatterns = [
    url(r'^add-to-task-set/$', AddRecipeToTaskSet.as_view(), name='add_to_task_set'),

    url(r'^get-failed-tasks/$', GetFailedTaskSet.as_view(), name='get_failed_tasks'),
    url(r'^get-success-tasks/$', GetSuccessTaskSet.as_view(), name='get_success_tasks'),
    url(r'^get-running-tasks/$', GetStartedTaskSet.as_view(), name='get_running_tasks'),
    url(r'^get-queued-tasks/$', GetQueuedTaskSet.as_view(), name='get_queued_tasks'),

    url(r'^quick-add-to-task-queue/$', QuickAddRecipeToTaskQueue.as_view(), name='quick_add_to_task_queue'),
    url(r'^run-set/$', RunSetOnModule.as_view(), name='quick_add_to_task_queue'),
    # url(r'^send-remote-data/<form_type>/$', send_remote_data, name='send-remote-data'),
    path('send-remote-data/<form_type>/', send_remote_data, name='send-remote-data'),

]
