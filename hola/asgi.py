"""
ASGI config for hola project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import sys
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.routing import websocket_urlpatterns

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hola.settings')
import sys
print("PYTHONPATH:", sys.path)

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})