from django.shortcuts import get_object_or_404

from rest_framework.views import APIView, Response
from rest_framework.validators import ValidationError
from rest_framework import status

from .serializers import ResetPasswordOtpRequestSerializer, ResetPasswordOtpValidateSerializer

from Otps.models import OneTimePassword




class ResetPasswordRequestOtpAPIView(APIView):

    def post(self, request):
        if not request.user.is_authenticated:
            serializer = ResetPasswordOtpRequestSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                otp_data = serializer.create(validated_data=serializer.validated_data)

                return Response(
                    {
                        'detail': {
                            'message': 'کد اعتبار سنجی ایجاد شد.',
                            'token': otp_data['token'], 
                            'code': otp_data['code']
                        }
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'شما قبلا وارد شده اید'}, status=status.HTTP_400_BAD_REQUEST)



