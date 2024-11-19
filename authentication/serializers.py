from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        user = self.context.get('request').user
        old_password = attrs.get('old_password')
        if not user.check_password(old_password):
            raise serializers.ValidationError("Old password is incorrect.")
        return attrs
