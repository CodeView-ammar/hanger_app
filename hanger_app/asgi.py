import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from notification import routing  # استبدل 'your_app_name' باسم تطبيقك
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hanger_app.settings')  # استبدل 'your_project_name'

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})