from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.views import Response

from .models import User
from .serializers import UserSerializer
from .permissions import IsUserOwnerOrAdmin




class UserViewSet(viewsets.ViewSet):

    permission_classes = [IsUserOwnerOrAdmin]
    lookup_field = "username"

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, username):
        query = get_object_or_404(User, username=username)
        self.check_object_permissions(request=request, obj=query)
        serializer = UserSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, username):
        instance = get_object_or_404(User, username=username)
        self.check_object_permissions(request=request, obj=instance)
        serializer = UserSerializer(instance=instance, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'کاربر آپدیت شد.',
                    'user': serializer.data
                }, status=status.HTTP_205_RESET_CONTENT
            )
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

    def my_user_data(self, request):
        serializer = UserSerializer(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)