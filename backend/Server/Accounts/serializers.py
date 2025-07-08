from rest_framework import serializers

from .models import ResetPasswordOneTimePassword

from Users.models import User
from Authentication.models import OneTimePassword

from random import randint
import uuid





class AccountResetPasswordOTPSerializer(serializers.Serializer):

    phone = serializers.CharField(required=True, write_only=True)

    def validate(self, atters):
        if User.objects.filter(phone=atters['phone']).exists():
            return atters
        else:
            raise serializers.ValidationError({'error': 'شماره تلفن موجود نیست'})

    def create(self, validated_data):

        code = randint(100000, 999999)

        token = uuid.uuid4()
        
        otp = OneTimePassword.objects.create(
            token=token,
            code=code
        )
        
        otp.save()

        user = User.objects.get(phone=validated_data['phone'])
        
        reset_password_otp = ResetPasswordOneTimePassword.objects.create(
            otp=otp,
            user=user,
            phone=validated_data['phone']
        )

        reset_password_otp.save()

        otp.get_expiration()

        return {'phone': reset_password_otp.phone, 'token': token, 'code': code}
