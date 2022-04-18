import os

from django.core.management.base import BaseCommand
from django.core import management
from redis import Redis


class Command(BaseCommand):
    help = 'Start Workers'

    def handle(self, *args, **options):
        management.call_command("start_worker", ("stir_fry", "MODULE_2"))
        management.call_command("start_worker", ("stir_fry", "MODULE_1"))
