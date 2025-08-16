# myapp/fcm_service.py
import firebase_admin
from firebase_admin import credentials, messaging

# تهيئة Firebase Admin SDK باستخدام Service Account
cred = credentials.Certificate('/root/metasoft/hanger_app/serviceAccount.json')
firebase_admin.initialize_app(cred)

class FCMService:
    @staticmethod
    def send_message(token: str, title: str, body: str, data: dict = None) -> dict:
        """
        إرسال رسالة FCM إلى جهاز محدد
        :param token: FCM Device Token
        :param title: عنوان الإشعار
        :param body: نص الإشعار
        :param data: بيانات إضافية كـ dict
        :return: dict مع نتيجة العملية
        """
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                token=token,
                data=data or {}
            )
            response = messaging.send(message)
            return {"success": True, "response": response}
        except Exception as e:
            return {"success": False, "error": str(e)}
