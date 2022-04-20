import os
import threading

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core import management
from django.core.management.base import BaseCommand
from django_rq.queues import get_queue_by_index
from redis import Redis
from rq import Queue, Worker
import django_rq
from rq.job import Job

from recipe.models import Recipe
from tasks.models import TaskSet
from tasks.recipe_runner import run_task


class Command(BaseCommand):
    help = 'Delete Job Bulk'

    def add_arguments(self, parser):
        parser.add_argument('--job-ids', nargs='+', help='RQ job ids')
        parser.add_argument('--queue-index', type=int)

    def handle(self, *args, **options):
        t = threading.Thread(target=self.delete_jobs, args=(options['job_ids'], options['queue_index']))
        t.daemon = True
        t.start()

    def delete_jobs(self, job_ids, queue_index):
        for job_id in job_ids:
            queue_index = int(queue_index)
            queue = get_queue_by_index(queue_index)
            job = Job.fetch(job_id, connection=queue.connection)
            queue.connection.lrem(queue.key, 0, job.id)
            job.delete()
            task_set = TaskSet.objects.get(pk=job.kwargs['task_id'])
            task_set.delete()
        async_to_sync(get_channel_layer().group_send)(f'channel_1', {
            'type': 'channel_message',
            'message': 'Jobs deleted!',
        })
