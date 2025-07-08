from rest_framework import serializers

from .models import AccountResetPassword

from Users.models import User
from Authentication.models import OneTimePassword

from random import randint
import uuid





class ResetPasswordOtpRequestSerializer(serializers.Serializer):

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
        
        reset_password_otp = AccountResetPassword.objects.create(
            otp=otp,
            user=user,
        )

        reset_password_otp.save()

        otp.get_expiration()

        return {'token': token, 'code': code}



class ResetPasswordOtpValidateSerializer(serializers.Serializer):

    code = serializers.CharField(max_length=6, min_length=6, required=True)
    password = serializers.CharField(max_length=16, min_length=8, required=True)
    password_conf = serializers.CharField(max_length=16, min_length=8, required=True)


    def validate(self, attrs):
        otp_token = self.context.get('otp_token')
        otp = OneTimePassword.objects.get(token=otp_token)
        reset_password_otp = otp.reset_password.get()

        # Enforced by field validators already
        if otp.status_validation() == 'ACT':
            if otp.code != attrs['code']:
                raise serializers.ValidationError({'error': 'کد یکبار مصرف نامعتبر نیست.'})

            if attrs['password'] != attrs['password_conf']:
                raise serializers.ValidationError({'error': 'رمزهای عبور با هم تطابق ندارند'})

            # All checks passed—apply the new password
            user = reset_password_otp.user
            user.set_password(attrs['password'])
            user.save()
        else:
            raise serializers.ValidationError({'error': 'کد یکبار مصرف فعال نیست'})
        
        return attrs
