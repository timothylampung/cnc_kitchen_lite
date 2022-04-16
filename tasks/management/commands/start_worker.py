import os
import threading

from django.core.management.base import BaseCommand
import django_rq


class Command(BaseCommand):
    help = 'Start Worker'

    def add_arguments(self, parser):
        parser.add_argument('queue_name', type=str)
        parser.add_argument('worker_name', type=str)

    def handle(self, *args, **options):
        queue_name = options['queue_name']
        worker_name = options['worker_name']
        t = threading.Thread(target=self.run_worker, args=(queue_name, worker_name))
        t.daemon = True
        t.start()

    def run_worker(self, queue_name, worker_name):
        from redis import Redis
        from rq import Queue, Worker
        redis = Redis()
        queue = Queue(queue_name, connection=redis)
        # Start a worker with as custom name
        worker = Worker([queue], connection=redis, name=worker_name)
        worker.work()
