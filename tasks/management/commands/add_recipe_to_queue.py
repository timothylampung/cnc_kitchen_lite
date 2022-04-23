from django.utils import timezone

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.management.base import BaseCommand
from redis import Redis
from rq import Queue
from rq.job import Job

from module.models import Module
from recipe.models import Recipe
from tasks.models import TaskSet
from tasks.task_handlers.recipe_runner import run_task


class Command(BaseCommand):
    help = 'Cook Recipe On Worker'

    def add_arguments(self, parser):
        parser.add_argument('recipe_id', type=int)
        parser.add_argument('task_name', type=str)
        parser.add_argument('module_id', type=str)

    def handle(self, *args, **options):
        recipe_id = options['recipe_id']
        task_name = options['task_name']
        module_id = options['module_id']

        recipe = Recipe.objects.get(pk=recipe_id)
        module = Module.objects.get(pk=module_id)

        task_set, _ = TaskSet.objects.get_or_create(
            recipe=recipe,
            task_name=task_name,
            module=module,
            queued_time=timezone.now()
        )

        queue_name = module.ip_address
        redis = Redis()
        queue = Queue(queue_name, connection=redis)
        job = queue.enqueue(run_task,
                            on_success=report_success, on_failure=report_failure,
                            kwargs={
                                'task_id': task_set.id,
                                'task_name': task_set.task_name,
                            })

        async_to_sync(get_channel_layer().group_send)(f'channel_1', {
            'type': 'channel_message',
            'message': 'Jobs added!',
        })
        recipe.cook_counts = recipe.cook_counts + 1
        recipe.save()
        task_set.rq_job_id = job.id
        task_set.task_origin = job.origin
        task_set.task_status = TaskSet.PENDING
        task_set.save()


def report_success(job, connection, result, *args, **kwargs):
    task_id = job.kwargs['task_id']
    task = TaskSet.objects.get(pk=task_id)
    task.task_status = TaskSet.SUCCESS
    task.completed_time = timezone.now()
    task.error_message = result
    task.save()

    async_to_sync(get_channel_layer().group_send)(f'channel_1', {
        'type': 'channel_message',
        'message': 'Jobs complete success!',
    })


def report_failure(job, connection, type, value, traceback):
    task_id = job.kwargs['task_id']
    task = TaskSet.objects.get(pk=task_id)
    task.task_status = TaskSet.FAILURE
    task.error_message = traceback
    task.save()
    async_to_sync(get_channel_layer().group_send)(f'channel_1', {
        'type': 'channel_message',
        'message': 'Jobs complete failed!',
    })
