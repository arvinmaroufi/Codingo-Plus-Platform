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



class AccountResetPasswordValidateSerializer(serializers.Serializer):

    code = serializers.CharField(max_length=6, min_length=6, required=True)
    password = serializers.CharField(max_length=16, min_length=8, required=True)
    password_conf = serializers.CharField(max_length=16, min_length=8, required=True)

    
    def validate(self, attrs):
        otp_token = self.context.get('otp_token')
        
        otp = OneTimePassword.objects.get(token=otp_token)
        reset_password_otp = otp.reset_password.get()
        
        if len(attrs['password']) < 8 or len(attrs['password']) > 16:
            raise serializers.ValidationError({'error': 'رمز عبور باید حداقل 8 کاراکتر و حداکثر 16 کاراکتر طول داشته باشد.'})

        if otp.status_validation() == 'ACT':
            if otp.code == attrs['code']:
                # Check if the password and password_conf match
                if attrs['password'] != attrs['password_conf']:
                    raise serializers.ValidationError({'erorr': 'رمزهای عبور با هم تطابق ندارند'})
            else:
                raise serializers.ValidationError({'error': 'کد یکبار مصرف نامعتبر نیست.'})
        else:
            raise serializers.ValidationError({'erorr': 'کد یکبار مصرف فعال نیست'})