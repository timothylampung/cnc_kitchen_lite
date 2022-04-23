import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer

TASK_UPDATE_BOARD_CAST = getattr(settings, "TASK_UPDATE_BOARD_CAST", None)


class ChannelConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'channel_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print(f'ROOM NAME => {self.room_group_name}')
        print(f'CHANNEL NAME => {self.channel_name}')
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        type = text_data_json['type']
        print(text_data_json)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': type,
                'message': message
            }
        )

    # Receive message from room group
    async def channel_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
