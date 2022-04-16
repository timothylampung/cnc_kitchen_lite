import time

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Enqueue Tasks'

    def handle(self, *args, **options):
        import django_rq
        queue = django_rq.get_queue('cooking_module')
        queue.enqueue(loop_50_times, kwargs={'recipe_id': 100})


def loop_50_times(recipe_id=None):
    print(recipe_id)
    time.sleep(2)
