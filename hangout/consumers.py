from channels.generic.websocket import AsyncWebsocketConsumer
import json
import jwt
from channels.db import database_sync_to_async
from django.conf import settings
from accounts.models import User
from enrolls.models import Enroll
from .serializers import ChatSerializer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = await self.get_user_from_token()
        if user is None:
            await self.close()
        self.user = user
        self.course_id = self.scope['url_route']['kwargs']['course_id']
        self.course_group_name = f'chat_{self.course_id}'
        
        if await self.is_enrolled():
            await self.channel_layer.group_add(
                self.course_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.course_group_name,
            self.channel_name
        )
        print("Disconnected")

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
            message = data['message']

            await self.save_chat_message(message)

            await self.channel_layer.group_send(
                self.course_group_name,
                {
                    'type': 'chat.message',
                    'message': message,
                    'sender': self.user.email
                }
            )
        except Exception as e:
            await self.send_error_response("An unexpected error occurred.")
    
    async def chat_message(self, event):
        message = event.get('message')
        sender = event.get('sender')
        await self.send(json.dumps({
            'message': message,
            'sender': sender
        }))

    async def send_error_response(self, error_message):
        await self.send(json.dumps({
            'error': error_message
        }))

    @database_sync_to_async
    def save_chat_message(self, message):
        data = {
            'sender': self.user.id,
            'course': self.course_id,
            'message': message
        }
        serializer = ChatSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

    @database_sync_to_async
    def get_user_from_token(self):
        try:
            headers = self.scope.get('headers', [])
            auth_header = next((value for name, value in headers if name == b'authorization'), b'').decode('utf-8')

            if auth_header.startswith('Bearer '):
                token = auth_header.split('Bearer ')[1]
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = payload['user_id']
                user  = User.objects.get(pk=user_id)
                return user

        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

        return None
    
    @database_sync_to_async
    def is_enrolled(self):
        user = self.user
        course = self.course_id
        if user is not None:
            return Enroll.objects.filter(user=user, course=course).exists()
        else:
            return False