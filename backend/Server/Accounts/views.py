from django.shortcuts import get_object_or_404

from rest_framework.views import APIView, Response
from rest_framework.validators import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import ResetPasswordOtpRequestSerializer, ResetPasswordOtpValidateSerializer, AccountResetPasswordSerializer

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



class ResetPasswordValidateOtpAPIView(APIView):
    def post(self, request, token):
        otp = get_object_or_404(OneTimePassword, token=token)

        if otp.status_validation() == False:
            otp.delete()
            return Response({'error': 'کد اعتبار سنجی منقضی شده است.'})

        
        serializer = ResetPasswordOtpValidateSerializer(data=request.data, context={'otp_token': token})

        if request.user.is_authenticated:
            return Response({"error": "شما قبلاً وارد شده‌اید"}, status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            otp.delete()
            return Response({'message': 'رمزعبور ریست شد.'}, status=status.HTTP_200_OK)
        else:
            otp.delete()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



class AccountResetPasswordAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AccountResetPasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response({'message': 'رمزعبور شما ریست شد.'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
