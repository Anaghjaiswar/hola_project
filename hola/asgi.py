"""
ASGI config for hola project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.routing import websocket_urlpatterns  # Import your websocket routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hola.settings')

# Define the ASGI application
application = ProtocolTypeRouter({
    # HTTP requests use Django's standard ASGI application
    "http": get_asgi_application(),
    
    # WebSocket requests will be handled by Channels
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # This refers to the websocket URL routing in the chat app
        )
    ),
})
