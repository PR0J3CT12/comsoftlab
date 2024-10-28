from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from django.core.exceptions import ValidationError
from comsoftlab.apps.front.emails import EmailClient
from comsoftlab.apps.users.models import User, Message
import asyncio


class MailConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = 'mail_group'
        self.uid = None
        self.user = None
        self.last_message_id = None
        self.email = None
        self.password = None
        self.provider = None

    async def connect(self):
        print("Соединение WebSocket установлено")
        self.channel_layer.group_add(self.group_name, self.channel_name)
        self.uid = self.scope['url_route']['kwargs']['uid']
        self.user = await sync_to_async(User.objects.get)(id=self.uid)
        messages = await sync_to_async(lambda: Message.objects.filter(user=self.user).order_by('-sent_date'))()
        self.last_message_id = await sync_to_async(lambda: messages[0].id if messages.exists() else None)()
        self.email = self.user.email
        self.password = self.user.password
        self.provider = self.user.email.split('@')[-1]

        await self.accept()
        await self.fetch_emails()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_progress_msg(self, type_, msg, progress, result_progress, data=None):
        await asyncio.sleep(1)
        await self.send(
            text_data=json.dumps(
                {
                    "type": type_,
                    "message": msg,
                    "progress": progress,
                    "result_progress": result_progress,
                    "data": data
                }
            )
        )

    async def send_completed_msg(self, msg, progress, result_progress):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "completed",
                    "message": msg,
                    "progress": progress,
                    "result_progress": result_progress
                }
            )
        )

    async def send_error_msg(self, msg):
        await self.send(text_data=json.dumps({"type": "error", "message": msg}))

    async def fetch_emails(self):
        await self.send_progress_msg("loading", "Чтение сообщений | Подключение к почте...", 0, 0)
        client = EmailClient(email=self.email, password=self.password, provider=self.provider)
        client.connect()
        await self.send_progress_msg("loading", "Чтение сообщений...", 0, 0)
        messages = client.fetch_messages()
        messages_amount = len(messages)
        await self.send_progress_msg("loading", f"Чтение сообщений | Прочитано {messages_amount} сообщений...", 0, 0)
        counter = 0
        new_messages = []
        for message in messages:
            counter += 1
            await self.send_progress_msg("loading", f"Чтение сообщений | Проверено {counter} сообщений...", 0, 0)
            if message['id'] == self.last_message_id:
                break
            else:
                new_messages.append(message)
        total = len(new_messages)
        await self.send_progress_msg("loading", f"Чтение сообщений | Найдено {total} новых сообщений...", 0, 0)
        new_messages.reverse()
        for progress, message in enumerate(new_messages, start=1):
            msg_data = {
                'id': message['id'],
                'user_id': self.uid,
                'subject': message['from'] if message['from'] != self.email else message['to'],
                'sent_date': message['date'],
                'message_text': message['body'],
                'message_subject': message['subject'],
                'attachments': message['attachments'] if message['attachments'] else []
            }
            message_ = Message(**msg_data)
            try:
                await sync_to_async(message_.full_clean)()
                await sync_to_async(message_.save)()
                received_date = message_.received_date.strftime("%d.%m.%Y %H:%M")
                sent_date = msg_data['sent_date'].strftime("%d.%m.%Y %H:%M")
                msg_data['sent_date'] = sent_date
                msg_data['received_date'] = received_date
                await self.send_progress_msg("new_message", f"Получение сообщений | {progress}/{total}", progress, total, msg_data)
            except ValidationError as e:
                await self.send_error_msg(str(e))
                continue

        await self.send_completed_msg("Загрузка завершена.", total, total)
        client.close_connection()
        await self.disconnect(1000)
