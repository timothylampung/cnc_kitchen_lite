from django.db import models
#  Copyright (c) 2021.
#  Volume Research & Development sdn. bhd.
#  Author : Timothy Lampung
#  Email : timothylampung@gmail.com
#  Contacts : +601165315133

from django.db.models.signals import post_save
from django.dispatch import receiver
import random
import string
import uuid
from django.utils import timezone
from django_lifecycle import hook, AFTER_UPDATE, BEFORE_UPDATE, LifecycleModel
from django.contrib.auth.models import User, Group, Permission

from django.db import models
from django.forms import JSONField
# Create your models here.
from cnc_kitchen_lite.core_model import DocumentModel, id_generator
from django.conf import settings

MODULE_QUEUE_NAME = getattr(settings, "MODULE_QUEUE_NAME", None)
HANDLER_TYPE = getattr(settings, "HANDLER_TYPE", None)


def upload_recipe_image(instance, filename):
    return f"images/recipes/{id_generator()}{filename}"


class Recipe(DocumentModel):
    handler_type = models.CharField(max_length=200, null=True, choices=HANDLER_TYPE, default=None)
    recipe_name = models.CharField(max_length=400, null=True)
    recipe_author = models.CharField(null=True, blank=True, max_length=400)
    description = models.CharField(null=True, blank=True, max_length=400)
    image_path = models.ImageField(upload_to=upload_recipe_image, null=True, blank=True)
    cook_counts = models.IntegerField(default=0, blank=True, null=True)
    etc = models.IntegerField(default=0, blank=True, null=True)
    rating = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    number_of_class = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.recipe_name


class Step(DocumentModel):
    PICKUP_STEP = 'Pickup Type'
    WOK_STEP = 'Wok Type'

    STEP_TYPES = (
        (PICKUP_STEP, PICKUP_STEP),
        (WOK_STEP, WOK_STEP)
    )

    step_name = models.CharField(null=True, blank=True, max_length=400)
    step_type = models.CharField(max_length=200, null=True, choices=STEP_TYPES, default=None)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, default=0, related_name="steps", )
    wait_for = models.IntegerField(default=0, null=True, blank=True, verbose_name=('Wait For (Seconds)'), )

    def __str__(self):
        return self.step_name


class SubStep(DocumentModel):
    parameters = JSONField()
    name = models.CharField(max_length=10, default='')

    def __str__(self):
        return self.name
