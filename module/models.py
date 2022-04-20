from django.db import models

# Create your models here.
from cnc_kitchen_lite.core_model import DocumentModel
from django.conf import settings

MODULE_QUEUE_NAME = getattr(settings, "MODULE_QUEUE_NAME", None)
HANDLER_TYPE = getattr(settings, "HANDLER_TYPE", None)


class Module(DocumentModel):
    BUSY = 'BUSY'
    AVAILABLE = 'AVAILABLE'
    DISABLED = 'DISABLED'

    STATUS = (
        (BUSY, 'BUSY'),
        (AVAILABLE, 'AVAILABLE'),
        (DISABLED, 'DISABLED'),
    )

    BUSY = 'BUSY'
    AVAILABLE = 'AVAILABLE'
    DISABLED = 'DISABLED'

    CONNECTED = 'CONNECTED'
    DISCONNECTED = 'DISCONNECTED'

    CONNECTIVITY = (
        (CONNECTED, 'CONNECTED'),
        (DISCONNECTED, 'DISCONNECTED'),
    )

    name = models.CharField(null=True, blank=True, max_length=400)
    instance_code = models.CharField(null=True, blank=True, max_length=400)
    ip_address = models.CharField(max_length=200, null=True, choices=MODULE_QUEUE_NAME, default=None)
    type_handler = models.CharField(max_length=200, null=True, choices=HANDLER_TYPE, default=None)
    wok_camera = models.CharField(null=True, blank=True, max_length=400)
    camera_opened = models.BooleanField(default=False, null=True)
    port = models.IntegerField(default=8888, null=True, blank=True)
    status = models.CharField(max_length=200, null=True, blank=True, choices=STATUS, default=AVAILABLE)
    connectivity = models.CharField(max_length=200, null=True, blank=True, choices=CONNECTIVITY, default=DISCONNECTED)

    def __str__(self):
        return f'({self.type_handler}) {self.name} ({self.ip_address})'
