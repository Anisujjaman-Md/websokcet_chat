import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from .models import ConnectionHistory, Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        token = self.scope['query_string'].decode().split('=')[1]
        self.user = await self.authenticate_user(token)

        if self.user is None:
            await self.close()
        else:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.create_connection_history()

            await self.accept()
            await self.notify_user_status('online')

    async def disconnect(self, close_code):
        await self.update_connection_history_status('offline')
        await self.notify_user_status('offline')
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        receiver_id = data.get('receiver_id')
        
        sender = self.user
        receiver = await self.get_user(receiver_id)
        
        if sender and receiver:
            await self.save_message(sender, receiver, message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender_id': sender.id,
                    'receiver_id': receiver.id,
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
            'receiver_id': event['receiver_id'],
        }))

    async def user_status(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user_id': event['user_id'],
            'status': event['status'],
        }))

    @database_sync_to_async
    def authenticate_user(self, token):
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            return User.objects.get(id=user_id)
        except Exception as e:
            return None

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def save_message(self, sender, receiver, content):
        return Message.objects.create(sender=sender, receiver=receiver, content=content)

    @database_sync_to_async
    def create_connection_history(self):
        return ConnectionHistory.objects.create(
            user=self.user,
            status=ConnectionHistory.ONLINE
        )

    @database_sync_to_async
    def update_connection_history_status(self, status):
        ConnectionHistory.objects.filter(user=self.user).update(status=status)

    async def notify_user_status(self, status):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_status',
                'message': f'{self.user.username} has {status}.',
                'user_id': self.user.id,
                'status': status,
            }
        )
