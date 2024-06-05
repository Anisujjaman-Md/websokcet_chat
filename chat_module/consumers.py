import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken


User = get_user_model()

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        token = self.scope['query_string'].decode().split('=')[1]
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        self.user = User.objects.get(id=user_id)
        if self.user is None:
            # If authentication fails, reject the connection
            self.close()
        else:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = 'chat_%s' % self.room_name

            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

            self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = self.user.id
        receiver_id = data['receiver_id']

        # Get the sender and receiver user instances
        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)

        # Save message to database
        Message.objects.create(sender=sender, receiver=receiver, content=message)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id,
                'receiver_id': receiver_id,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        sender_id = self.user.id
        receiver_id = event['receiver_id']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
            'receiver_id': receiver_id,
        }))
        
        
