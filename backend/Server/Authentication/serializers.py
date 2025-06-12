from rest_framework import serializers

from Users.models import User



class LoginPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)

    def validate_phone(self, value):
        if not User.objects.filter(phone=value).exists():
            raise serializers.ValidationError({'error': 'شماره تلفن موجود نیست'})
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError({'error': 'رمز عبور باید حداقل ۸ کاراکتر باشد'})
        return value

    def validate(self, data):
        phone = data.get('phone')
        password = data.get('password')
        if phone is None or password is None:
            raise serializers.ValidationError({'error': 'شماره تلفن و رمز عبور هر دو الزامی هستند'})
        user = User.objects.get(phone=phone)
        if not user.check_password(password):
            raise serializers.ValidationError({'error': 'رمز عبور اشتباه است'})
        return data