import os
import threading

from django.contrib.sites import management
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Cook Recipe On Worker'

    def add_arguments(self, parser):
        parser.add_argument('ingredient_id', type=str)
        parser.add_argument('requester_id', type=str)

    def handle(self, *args, **options):
        queue_name = 'cooking_module'
        worker_name = options['worker_name']
        from redis import Redis
        from rq import Queue, Worker
        redis = Redis()
        queue = Queue(queue_name, connection=redis)
        worker = Worker([queue], connection=redis, name=worker_name)
        worker.work()

    def cook_recipe(self):
        pass

    def pick_ingredients(self):
        pass
