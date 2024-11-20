from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    full_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('id', 'full_name', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            username=validated_data['email'],  # Using email as username
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    
class UserProfileSerializer(serializers.ModelSerializer):
    num_posts = serializers.SerializerMethodField()
    num_followers = serializers.SerializerMethodField()
    num_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'bio', 'profile_photo', 'background_photo',
            'num_posts', 'num_followers', 'num_following'
        ]
        read_only_fields = ['id', 'username', 'num_posts', 'num_followers', 'num_following']

    def get_num_posts(self, obj):
        return obj.posts.count()

    def get_num_followers(self, obj):
        return obj.followers.count()

    def get_num_following(self, obj):
        return obj.following.count()
 