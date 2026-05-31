from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'password',
            'role',
            'phone_number'
        ]

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'buyer'),
            phone_number=validated_data.get('phone_number')
        )

        return user
    

# Why Use create_user()?
# NEVER do:

# User.objects.create(...)

# for passwords.
# Because:
# password will store as plain text.

# huge security problem

# create_user() automatically:
# hashes password
# secures authentication 