from rest_framework.views import APIView, Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken


from .serializers import LoginPasswordSerializer
from .permissions import IsNotAuthenticated


from Users.models import User




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