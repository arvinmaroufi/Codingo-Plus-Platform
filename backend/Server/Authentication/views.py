from django.shortcuts import get_object_or_404

from rest_framework.views import APIView, Response
from rest_framework import status


from .serializers import (
    LoginPasswordSerializer,
    MainTokenObtainPairSerializer,
    UserLoginOneTimePasswordSerializer,
    UserRegisterOneTimePasswordSerializer,
    UserLoginOneTimePasswordValidateSerializer,
    UserRegisterOneTimePasswordValidateSerializer,
)
from .permissions import IsNotAuthenticated


from Users.models import User
from Otps.models import OneTimePassword




class LoginPasswordAPIView(APIView):

    permission_classes = [IsNotAuthenticated]

    def post(self, request):

        serializer = LoginPasswordSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):

            phone = serializer.validated_data['phone']
            user = User.objects.get(phone=phone)

            if not user.is_active:
                return Response({'error': 'کاربر فعال نیست'}, status=status.HTTP_401_UNAUTHORIZED)
            
            refresh = MainTokenObtainPairSerializer.get_token(user)
            
            return Response(
                {
                    'refresh': str(refresh), 
                    'access': str(refresh.access_token)
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class UserLoginRequestOtpAPIView(APIView):

    def post(self, request):
        if not request.user.is_authenticated:
            serializer = UserLoginOneTimePasswordSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                otp_data = serializer.create(validated_data=serializer.validated_data)

                return Response(
                    {
                        'detail': {
                            'message': 'Otp created successfully',
                            'token': otp_data['token'], 
                            'code': otp_data['code']
                        }
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'You are already logged in'}, status=status.HTTP_400_BAD_REQUEST)



class UserLoginValidateOtpAPIView(APIView):
    def post(self, request, token):
        otp = get_object_or_404(OneTimePassword, token=token)

        login_otp = otp.login_otps.get()
        
        serializer = UserLoginOneTimePasswordValidateSerializer(data=request.data, context={'otp_token': token})

        if request.user.is_authenticated:
            return Response({"message": "شما قبلاً وارد شده‌اید"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if serializer.is_valid():
                user = login_otp.user

                if not user.is_active:
                    return Response({'error': 'کاربر فعال نیست'}, status=status.HTTP_401_UNAUTHORIZED)
                
                refresh = MainTokenObtainPairSerializer.get_token(user)
                
                return Response(
                    {
                        'refresh': str(refresh), 
                        'access': str(refresh.access_token)
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterRequestOtpAPIView(APIView):

    def post(self, request):
        
        if not request.user.is_authenticated:  

            serializer = UserRegisterOneTimePasswordSerializer(data=request.data)

            if serializer.is_valid(raise_exception=True):

                otp_data = serializer.create(validated_data=serializer.validated_data)

                return Response(
                    {
                        'detail': {
                            'message': 'کد اعتبار سنجی با موفقیت ایجاد شد.',
                            'token': otp_data['token'], 
                            'code': otp_data['code']
                        }
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'شما قبلا وارد شده اید.'}, status=status.HTTP_400_BAD_REQUEST)



class UserRegisterValidateOtpAPIView(APIView):

    def post(self, request, token):

        if not request.user.is_authenticated:
            otp = get_object_or_404(OneTimePassword, token=token)
            if otp:
                if otp.registration_otps:
                    serializer = UserRegisterOneTimePasswordValidateSerializer(data=request.data, context={'otp_token': otp.token})
                    if serializer.is_valid(raise_exception=True):

                        tokens = serializer.create(
                            validated_data=serializer.validated_data, 
                            token=token
                        )

                        return Response(
                            {
                                'detail': {
                                    'message': 'کاربر با موفقیت ایجاد شده است.',
                                    'token': tokens['tokens']
                                }
                            },
                            status=status.HTTP_201_CREATED
                        )
                    else:
                        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': 'کد اعتبار سنجی موجود نیست.'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': 'Otp does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'شما احراز هویت شده اید.'}, status=status.HTTP_400_BAD_REQUEST)