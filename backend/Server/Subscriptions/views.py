from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated

from .models import Subscription, SubscriptionPlan
from .serializers import SubscriptionSerializer, SubscriptionPlanSerializer
from .permissions import IsAdminOrReadOnly



class SubscriptionPlanViewSet(viewsets.ViewSet):

    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        queryset = SubscriptionPlan.objects.all()
        serializer = SubscriptionPlanSerializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def retrieve(self, request, slug):
        instance = get_object_or_404(SubscriptionPlan, slug=slug)
        serializer = SubscriptionPlanSerializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def create(self, request):
        serializer = SubscriptionPlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'پلن ایجاد شد.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'erorr': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, slug):
        instance = get_object_or_404(SubscriptionPlan, slug=slug)
        self.check_object_permissions(request=request, obj=instance)
        serializer = SubscriptionPlanSerializer(data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'پلن آپدیت شد.'}, status=status.HTTP_200_OK)
        else:
            return Response({'erorr': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    def list(self, request):
        if request.user.is_staff:
            queryset = Subscription.objects.all()
            serializer = SubscriptionSerializer(instance=queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'You dont have the permission.'}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, pk):
        if request.user.is_staff:
            instance = get_object_or_404(Subscription, user__id=pk)
            serializer = SubscriptionSerializer(instance=instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'You dont have the permission.'}, status=status.HTTP_403_FORBIDDEN)

    def my_subscription(self, request):
        instance = get_object_or_404(Subscription, user=request.user)
        serializer = SubscriptionSerializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)