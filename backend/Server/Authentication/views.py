from django.shortcuts import get_object_or_404

from rest_framework.views import APIView, Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken


from .serializers import (
    LoginPasswordSerializer,
    UserRegisterOneTimePasswordSerializer,
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
            
            refresh = RefreshToken.for_user(user)
            
            return Response(
                {
                    'refresh': str(refresh), 
                    'access': str(refresh.access_token),
                    'user_type': user.user_type
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
                        'Detail': {
                            'Message': 'Otp created successfully',
                            'token': otp_data['token'], 
                            'code': otp_data['code']
                        }
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Detail': 'You are already logged in'}, status=status.HTTP_400_BAD_REQUEST)



class UserRegisterValidateOtpAPIView(APIView):

    def post(self, request, token):

        if not request.user.is_authenticated:
            otp = get_object_or_404(OneTimePassword, token=token)
            if otp:
                if otp.registration_otps:
                    serializer = UserRegisterOneTimePasswordValidateSerializer(data=request.data, context={'otp_token': otp.token})
                    if serializer.is_valid(raise_exception=True):

                        user_data = serializer.create(
                            validated_data=serializer.validated_data, 
                            token=token
                        )

                        return Response(
                            {
                                'Detail': {
                                    'Message': 'User created successfully',
                                    'User': user_data['user'],
                                    'Token': user_data['tokens']
                                }
                            },
                            status=status.HTTP_201_CREATED
                        )
                    else:
                        return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'Detail': 'Otp register does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'Detail': 'OTP does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'Detail': 'You are already authenticated'}, status=status.HTTP_400_BAD_REQUEST)