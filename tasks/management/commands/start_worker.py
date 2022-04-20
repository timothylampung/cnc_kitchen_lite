import os
import threading

from django.core.management.base import BaseCommand
import django_rq
from redis import Redis
from rq import Queue, Worker

from tasks.workers.task_worker import TaskWorker


class Command(BaseCommand):
    help = 'Start Worker'

    def add_arguments(self, parser):
        parser.add_argument('queue_name', type=str)
        parser.add_argument('worker_name', type=str)

    def handle(self, *args, **options):
        queue_name = options['queue_name']
        worker_name = options['worker_name']
        redis = Redis()
        queue = Queue(queue_name, connection=redis)
        worker = TaskWorker(queues=queue, name=worker_name, connection=redis)
        worker.work()
