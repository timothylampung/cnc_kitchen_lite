from django.urls import re_path

from cnc_kitchen_lite import consumers

websocket_urlpatterns = [
    re_path(r'ws/channel/(?P<room_name>\w+)/$',
            consumers.ChannelConsumer.as_asgi()),
]
