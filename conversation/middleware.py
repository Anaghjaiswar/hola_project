from jwt import decode, exceptions
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from urllib.parse import parse_qs
from accounts.models import CustomUser  # Update the path to your user model

@database_sync_to_async
def get_user_from_token(token):
    try:
        decoded_data = decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_data.get("user_id")
        return CustomUser.objects.get(id=user_id)
    except (CustomUser.DoesNotExist, exceptions.InvalidTokenError, exceptions.DecodeError):
        return AnonymousUser()

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"].decode()
        params = parse_qs(query_string)
        token = None

        # Check for token in query params or headers
        if "token" in params:
            token = params["token"][0]
        else:
            headers = dict(scope["headers"])
            if b"authorization" in headers:
                auth_header = headers[b"authorization"].decode()
                if auth_header.startswith("Bearer "):
                    token = auth_header.split("Bearer ")[1]

        scope["user"] = await get_user_from_token(token)
        return await super().__call__(scope, receive, send)
