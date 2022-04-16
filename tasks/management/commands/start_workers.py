import os

from django.core.management.base import BaseCommand
from django.core import management
from redis import Redis


class Command(BaseCommand):
    help = 'Start Workers'

    def handle(self, *args, **options):
        management.call_command("start_worker", ("cooking_module", "MODULE_1"))
        management.call_command("start_worker", ("cooking_module", "MODULE_2"))
