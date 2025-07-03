from django.contrib.auth import authenticate

from rest_framework import serializers, validators

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import UserRegisterOneTimePassword, UserLoginOneTimePassword

from Users.models import User
from Otps.models import OneTimePassword

from random import randint
import uuid



class MainTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Include standard claims plus a string URL for the user's profile picture.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Basic user info
        token['phone']     = user.phone
        token['email']     = user.email
        token['is_admin']  = user.is_staff
        token['full_name'] = user.full_name
        token['username']  = user.username
        token['user_type'] = user.user_type

        # Map user types to their OneToOne related_name
        related_map = {
            'AD': 'admin_profile',
            'TE': 'teacher_profile',
            'ST': 'student_profile',
            'SU': 'supporter_profile',
        }

        profile_url = None
        related_name = related_map.get(user.user_type)

        if related_name:
            try:
                profile = getattr(user, related_name)
                pic = getattr(profile, 'profile_picture', None)

                # grab the URL string, not the ImageFieldFile object
                if pic and hasattr(pic, 'url'):
                    profile_url = pic.url
                else:
                    # fallback: store the file path as string
                    profile_url = str(pic) if pic else None

            except:
                # user exists but no profile record yet
                profile_url = None

        token['profile'] = profile_url
        return token




class LoginPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True, max_length=255)

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        # 1. Required fields
        if not phone or not password:
            raise serializers.ValidationError({'error': 'شماره تلفن و رمز عبور هر دو الزامی هستند'})

        # 2. Password length
        if len(password) < 8:
            raise serializers.ValidationError({'error': 'رمز عبور باید حداقل ۸ کاراکتر باشد'})

        # 3. Authenticate user (also checks existence)
        user = authenticate(phone=phone, password=password)
        if user is None:
            # Could be wrong phone or wrong password
            raise serializers.ValidationError({'error': 'شماره تلفن یا رمز عبور اشتباه است'})

        # 4. Attach the user for your view to use
        attrs['user'] = user
        return attrs




class UserLoginOneTimePasswordSerializer(serializers.Serializer):

    phone = serializers.CharField(required=True, write_only=True)

    def validate_phone(self, value):
        if value is None:
            raise serializers.ValidationError('The phone number is needed')
        return value

    def validate(self, atters):
        if User.objects.filter(phone=atters['phone']).exists():
            return atters
        else:
            raise serializers.ValidationError('The user is not found')

    def create(self, validated_data):

        code = randint(100000, 999999)

        token = uuid.uuid4()
        
        otp = OneTimePassword.objects.create(
            token=token,
            code=code
        )
        
        otp.save()

        otp.get_expiration()
        
        user = User.objects.get(phone=validated_data['phone'])
        
        user_login_otp = UserLoginOneTimePassword.objects.create(
            otp=otp,
            user=user,
            phone=validated_data['phone']
        )

        user_login_otp.save()

        return {'phone': user_login_otp.phone, 'token': token, 'code': code}


class UserLoginOneTimePasswordValidateSerializer(serializers.Serializer):

    code = serializers.CharField(max_length=6, min_length=6, required=True)

    def validate(self, attrs):
        otp_token = self.context.get('otp_token')
        
        otp = OneTimePassword.objects.get(token=otp_token)

        if otp.status_validation() == 'ACT':
            if otp.code == attrs['code']:
                return attrs
            else:
                raise serializers.ValidationError({'code': 'Invalid OTP code.'})
        else:
            raise serializers.ValidationError('Inactive OTP')



class UserRegisterOneTimePasswordSerializer(serializers.ModelSerializer):

    # Define the email field with validation to ensure uniqueness
    email = serializers.EmailField(
        required=True,  # Email is required
        write_only=True,
        help_text="Enter a unique email address"  # Help text for the email field
    )

    # Define the phone field with validation to ensure uniqueness
    phone = serializers.CharField(
        required=True,  # Phone is required
        write_only=True,
        help_text="Enter a unique phone address"  # Help text for the phone field
    )

    # Define the username field
    username = serializers.CharField(
        required=True,  # Username is required
        write_only=True,
        help_text="Enter a unique username"  # Help text for the username field
    )

    # Define the full name field
    full_name = serializers.CharField(
        required=True,  # Full name is required
        write_only=True,
        help_text="Enter your full name"  # Help text for the full name field
    )

    # Define the password field with validation
    password = serializers.CharField(
        required=True,  # Password is required
        write_only=True,  # Password is not returned in the response
        help_text="Enter a password (8-16 characters)"  # Help text for the password field
    )

    # Define the password confirmation field
    password_conf = serializers.CharField(
        required=True,  # Password confirmation is required
        write_only=True,  # Password confirmation is not returned in the response
        help_text="Confirm your password (8-16 characters)"  # Help text for the password confirmation field
    )

    user_type = serializers.CharField(required=True, write_only=True)


    class Meta:
        model = UserRegisterOneTimePassword
        fields = "__all__"
        read_only_fields = ['otp']


    # Validate the entire serializer
    def validate(self, attrs):

        if attrs['password'] != attrs['password_conf']:
            raise serializers.ValidationError({'error': 'رمزهای عبور با هم تطابق ندارند'})
        
        if attrs['password'] == attrs['username']:
            raise serializers.ValidationError({'error': 'رمز عبور نمی‌تواند با نام کاربری یکسان باشد'})
        
        if len(attrs['phone']) == 12:
            raise serializers.ValidationError({'error': 'شماره تماس باید 11 رقمی باشد'})
        
        if len(attrs['password']) < 8 or len(attrs['password']) > 16:
            raise serializers.ValidationError({'error': 'رمز عبور باید حداقل 8 کاراکتر و حداکثر 16 کاراکتر طول داشته باشد.'})
        
        if len(attrs['full_name']) < 3 or len(attrs['full_name']) > 50:
            raise serializers.ValidationError({'error': 'نام کامل باید بین ۳ تا ۵۰ کاراکتر باشد'})
        
        if len(attrs['username']) < 3 or len(attrs['username']) > 20:
            raise serializers.ValidationError({'error': 'نام کاربری باید بین ۳ تا ۲۰ کاراکتر باشد'})
        
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({'error': 'نام کاربری باید یکتا باشد'})
        
        if User.objects.filter(phone=attrs['phone']).exists():
            raise serializers.ValidationError({'error': 'شماره تلفن باید یکتا باشد'})
        
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({'error': 'ایمیل باید یکتا باشد'})
        
        return attrs



    def create(self, validated_data):

        code = randint(100000, 999999)

        token = uuid.uuid4()

        otp = OneTimePassword.objects.create(
            token=token,
            code=code
        )

        otp.save()

        otp.get_expiration()

        user_register_otp = UserRegisterOneTimePassword.objects.create(
            otp=otp,
            email=validated_data['email'],
            phone=validated_data['phone'],
            username=validated_data['username'],
            password=validated_data['password'],
            user_type="ST",
            full_name=validated_data['full_name'],
            password_conf=validated_data['password_conf']
        )


        user_register_otp.save()

        return {'phone': user_register_otp.phone, 'token': token, 'code': code}




class UserRegisterOneTimePasswordValidateSerializer(serializers.Serializer):

    code = serializers.CharField(max_length=6, min_length=6, required=True)  

    def validate(self, attrs):
        
        otp_token = self.context.get('otp_token')

        otp = OneTimePassword.objects.get(token=otp_token)

        if otp.status_validation() == 'ACT':

            if otp.code == attrs['code']:
                return attrs
            else:
                raise serializers.ValidationError({'erorr': 'کد اعتبار سنجی نامعتبر است.'})
        else:
            raise serializers.ValidationError({'erorr': 'کد اعتبار سنجی فعال نمی باشد'})
    

    def create(self, validated_data, token):

        otp = OneTimePassword.objects.get(token=token)

        otp.is_used = True
        otp.save()

        user_register_otp = otp.registration_otps

        user = User.objects.create_user(
            email=user_register_otp.email,
            phone=user_register_otp.phone,
            username=user_register_otp.username,
            password=user_register_otp.password,
            full_name=user_register_otp.full_name,
            user_type=user_register_otp.user_type
        )

        user.save()

        refresh = MainTokenObtainPairSerializer.get_token(user)

        return {
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }