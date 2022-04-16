import random
import string

from django_lifecycle import LifecycleModel
from django.conf import settings
from django.db import models
import uuid


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class DocumentModel(LifecycleModel):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'

    DOCUMENT_STATUS_CHOICES = (
        (ACTIVE, 'ACTIVE'),
        (INACTIVE, 'INACTIVE'),
    )

    document_status = models.CharField(
        max_length=200, null=True, choices=DOCUMENT_STATUS_CHOICES, default=ACTIVE)
    editor = models.ForeignKey(settings.AUTH_USER_MODEL,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE,
                               related_name="%(class)s_editor",
                               )
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                null=True,
                                blank=True,
                                related_name="%(class)s_creator",
                                )
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    document_code = models.CharField(null=True, blank=True, max_length=400)

    def save(self, **kwargs):
        if self.id is None:
            self.document_code = uuid.uuid4()
        super().save(**kwargs)

    class Meta:
        abstract = True
