from django.core.management.base import BaseCommand
from django_rq.queues import get_queue_by_index, DjangoRQ
from django_rq.settings import QUEUES_LIST
from redis import Redis
from rq import Queue, Worker

from module.models import Module
from tasks.workers.task_worker import TaskWorker


class Command(BaseCommand):
    help = 'Populate Module'

    def handle(self, *args, **options):

        for index, config in enumerate(QUEUES_LIST):
            queue = get_queue_by_index(index)
            if isinstance(queue, DjangoRQ):
                if queue.name != 'default':
                    Module.objects.get_or_create(
                        ip_address=queue.name,
                        name=f'Module {index}'
                    )


