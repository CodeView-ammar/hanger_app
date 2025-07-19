# your_app/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = f"user_{self.user_id}"

        # انضم إلى المجموعة الخاصة بالمستخدم
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # مغادرة المجموعة
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # استقبال الرسائل من السيرفر
    async def receive(self, text_data):
        pass  # في حالتنا لا حاجة لاستقبال رسائل من العميل

    # استقبال رسالة من السيرفر إلى العميل
    async def send_notification(self, event):
        await self.send_json({
        "type": "notification",
        "message": event["message"],
        "status": event["status"],
        "created_at": event["created_at"],
        "id": event["id"],
        "is_read": event["is_read"],
    })
