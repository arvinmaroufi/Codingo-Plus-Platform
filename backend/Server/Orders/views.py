from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ViewSet
from rest_framework.views import Response, APIView
from rest_framework import status

from .models import Order, OrderCourseItem
from .serializers import OrderSerializer, OrderCourseItemSerializer
from .permissions import IsOrderOwnerOrAdmin, IsOrderItemOwnerOrAdmin


class OrderViewSet(ViewSet):
    
    permission_classes = [IsOrderOwnerOrAdmin]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = OrderSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, order_id=None):
        order = get_object_or_404(self.get_queryset(), order_id=order_id)
        self.check_object_permissions(request, order)
        serializer = OrderSerializer(order, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message': 'The Order is added.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, order_id=None):
        order = get_object_or_404(self.get_queryset(), order_id=order_id)
        self.check_object_permissions(request, order)
        serializer = OrderSerializer(order, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'The Order is updated.'}, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, order_id=None):
        order = get_object_or_404(self.get_queryset(), order_id=order_id)
        self.check_object_permissions(request, order)
        order.delete()
        return Response({'message': 'The Order is deleted.'}, status=status.HTTP_204_NO_CONTENT)
    
    def my_orders(self, request):
        queryset = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class OrderCourseItemViewSet(ViewSet):
    
    permission_classes = [IsOrderItemOwnerOrAdmin]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return OrderCourseItem.objects.all()
        return OrderCourseItem.objects.filter(order__user=self.request.user)
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = OrderCourseItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        item = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(request, item)
        serializer = OrderCourseItemSerializer(item)
        return Response(serializer.data)

    def create(self, request):
        serializer = OrderCourseItemSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.validated_data['order']
            self.check_object_permissions(request, order)
            
            course = serializer.validated_data['course']
            if OrderCourseItem.objects.filter(order=order, course=course).exists():
                return Response(
                    {"detail": "This course is already in the order."},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        queryset = self.get_queryset()
        item = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(request, item)
        
        serializer = OrderCourseItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = self.get_queryset()
        item = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(request, item)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    