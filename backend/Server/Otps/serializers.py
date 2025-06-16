from rest_framework import serializers

from .models import OneTimePassword

from random import randint
import uuid




class OneTimePasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = OneTimePassword
        fields = "__all__"  
    

    def create(self, validated_data):

        code = randint(100000, 999999)

        token = uuid.uuid4()

        otp = OneTimePassword.objects.create(
            phone=validated_data['phone'],
            token=token,
            code=code
        )

        otp.save()

        otp.get_expiration()
        
        return {'token': token, 'code': code}