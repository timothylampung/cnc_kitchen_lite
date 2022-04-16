from django.db import models

# Create your models here.
from cnc_kitchen_lite.core_model import DocumentModel
from django.conf import settings

MODULE_QUEUE_NAME = getattr(settings, "MODULE_QUEUE_NAME", None)


class Module(DocumentModel):
    STIR_FRY_MODULE = 'STIR_FRY_MODULE'
    DEEP_FRY_MODULE = 'DEEP_FRY_MODULE'
    GRILLING_MODULE = 'GRILLING_MODULE'
    DRINKS_MODULE = 'DRINKS_MODULE'
    BOILER_MODULE = 'BOILER_MODULE'
    STEAMING_MODULE = 'STEAMING_MODULE'
    TRANSPORTER_MODULE = 'TRANSPORTER_MODULE'

    TYPE = (
        (STIR_FRY_MODULE, 'STIR_FRY_MODULE'),
        (DEEP_FRY_MODULE, 'DEEP_FRY_MODULE'),
        (GRILLING_MODULE, 'GRILLING_MODULE'),
        (DRINKS_MODULE, 'DRINKS_MODULE'),
        (BOILER_MODULE, 'BOILER_MODULE'),
        (STEAMING_MODULE, 'STEAMING_MODULE'),
        (TRANSPORTER_MODULE, 'TRANSPORTER_MODULE'),
    )

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
    queue_handler = models.CharField(max_length=200, null=True, choices=MODULE_QUEUE_NAME, default=None)
    ip_address = models.CharField(null=True, blank=True, max_length=400, unique=True)
    wok_camera = models.CharField(null=True, blank=True, max_length=400)
    camera_opened = models.BooleanField(default=False, null=True)
    port = models.IntegerField(default=8888, null=True, blank=True)
    status = models.CharField(max_length=200, null=True, blank=True, choices=STATUS, default=AVAILABLE)
    connectivity = models.CharField(max_length=200, null=True, blank=True, choices=CONNECTIVITY, default=DISCONNECTED)
    type = models.CharField(max_length=200, null=True, blank=True, choices=TYPE, default=STIR_FRY_MODULE)

    def __str__(self):
        return f'{self.name} ({self.ip_address})'
