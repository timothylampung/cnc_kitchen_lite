from cnc_kitchen_lite.core_model import DocumentModel
from django.db import models
from module.models import Module
from recipe.models import Recipe

from django.conf import settings

MODULE_QUEUE_NAME = getattr(settings, "MODULE_QUEUE_NAME", None)


class TaskSet(DocumentModel):
    PENDING = 'PENDING'
    #: Task was received by a worker (only used in events).
    RECEIVED = 'RECEIVED'
    #: Task was started by a worker (:setting:`task_track_started`).
    STARTED = 'STARTED'
    #: Task succeeded.
    SUCCESS = 'SUCCESS'
    #: Task failed.
    FAILURE = 'FAILURE'
    #: Task was revoked.
    REVOKED = 'REVOKED'
    #: Task was rejected (only used in events).
    REJECTED = 'REJECTED'
    #: Task is waiting for retry.
    RETRY = 'RETRY'
    #: Task is waiting for ignored.
    IGNORED = 'IGNORED'

    TASK_STATUS = (
        (PENDING, 'PENDING'),
        (RECEIVED, 'RECEIVED'),
        (STARTED, 'STARTED'),
        (SUCCESS, 'SUCCESS'),
        (FAILURE, 'FAILURE'),
        (REVOKED, 'REVOKED'),
        (REJECTED, 'REJECTED'),
        (RETRY, 'RETRY'),
        (IGNORED, 'IGNORED'),
    )

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, default=None, related_name="tasks_on_recipe", )
    task_name = models.CharField(null=True, max_length=400)
    time_to_complete = models.IntegerField(default=0, null=True, blank=True, )
    task_status = models.CharField(max_length=200, null=True, choices=TASK_STATUS, default=PENDING)
    rq_job_id = models.CharField(null=True, blank=True, max_length=400)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, default=None, related_name="tasks", )

    def save(self, **kwargs):
        self.task_name = self.recipe.recipe_name + '-' + self.task_name
        super(TaskSet, self).save(**kwargs)
