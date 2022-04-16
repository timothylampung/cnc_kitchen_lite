import os
import threading
from django.core.management.base import BaseCommand
from redis import Redis
from rq import Queue, Worker
import django_rq

from tasks.recipe_runner import run_recipe


class Command(BaseCommand):
    help = 'Cook Recipe On Worker'

    def add_arguments(self, parser):
        parser.add_argument('recipe_id', type=str)

    def handle(self, *args, **options):
        recipe_id = options['recipe_id']
        queue_name = 'cooking_module'
        redis = Redis()
        queue = Queue(queue_name, connection=redis)
        queue.enqueue(run_recipe,
                      kwargs={
                          'recipe_id': recipe_id
                      })
