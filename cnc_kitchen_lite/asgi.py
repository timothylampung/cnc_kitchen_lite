# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import threading

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Just HTTP for now. (We can add other protocols later.)
})



# driver_path = None
# if platform == "linux" or platform == "linux2":
#     pass
# elif platform == "darwin":
#     driver_path= os.path.join(CORE_DIR, "core/chrome_driver/macOS/chromedriver")
# elif platform == "win32":
#     pass
