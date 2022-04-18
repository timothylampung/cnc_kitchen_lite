import os
import threading

from django.core import management
from django.core.management.base import BaseCommand
from redis import Redis
from rq import Queue, Worker
import django_rq

from recipe.models import Recipe
from tasks.models import TaskSet
from tasks.recipe_runner import run_task


class Command(BaseCommand):
    help = 'Cook Recipe On Worker'

    def add_arguments(self, parser):
        parser.add_argument('recipe_id', type=int)
        parser.add_argument('task_name', type=str)

    def handle(self, *args, **options):
        recipe_id = options['recipe_id']
        task_name = options['task_name']
        recipe = Recipe.objects.get(pk=recipe_id)
        task_set, _ = TaskSet.objects.get_or_create(
            recipe=recipe,
            task_name=task_name
        )
        queue_name = recipe.queue_handler
        redis = Redis()
        queue = Queue(queue_name, connection=redis)
        queue.enqueue(run_task,
                      kwargs={
                          'task_id': task_set.id,
                          'task_name' : task_set.task_name
                      })


