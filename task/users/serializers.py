from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()



class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def create(self, validated_data):
        username = validated_data['username']
        password1 = validated_data['password1']
        password2 = validated_data['password2']

        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match.")
        
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("A user with this username already exists.")

        user = User(username=username)
        user.set_password(password1)
        user.save()
        return user