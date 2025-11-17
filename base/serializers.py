from rest_framework import serializers
from .models import User, Profile
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields =("id", "username", "email", "password", "role")

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data.get("email"),
            role=validated_data.get("role", "customer")
        )
        user.set_password(validated_data["password"])
        user.save()

        Profile.objects.create(user=user)

        return user


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'phone', 'address']