from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .pusher import pusher_client

class MessageAPIView(APIView):
    def post(self, request):
        # Validate incoming request data
        username = request.data.get('username')
        message = request.data.get('message')

        if not username or not message:
            return Response(
                {"error": "Both 'username' and 'message' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Trigger a Pusher event
            pusher_client.trigger('chat', 'message', {
                'username': username,
                'message': message,
            })

            return Response(
                {"status": "Message sent successfully."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to send message: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
