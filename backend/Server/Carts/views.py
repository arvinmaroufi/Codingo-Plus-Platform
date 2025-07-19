from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ViewSet
from rest_framework.views import Response, APIView
from rest_framework import status

from .models import Coupon, Cart
from .serializers import CouponSerializer, CartSerializer
from .permissions import IsCouponOwnerOrAdmin, IsCartOwnerOrAdmin



class CouponViewSet(ViewSet):
    
    permission_classes = [IsCouponOwnerOrAdmin]
    
    def list(self, request):
        if request.user.is_staff:
            queryset = Coupon.objects.all()
        else:
            queryset = Coupon.objects.filter(user=request.user) | Coupon.objects.filter(user__isnull=True)
        serializer = CouponSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        coupon = get_object_or_404(Coupon, pk=pk)
        self.check_object_permissions(request, coupon)
        serializer = CouponSerializer(coupon)
        return Response(serializer.data)

    def create(self, request):
        serializer = CouponSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'The Coupon is added.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        coupon = get_object_or_404(Coupon, pk=pk)
        self.check_object_permissions(request, coupon)
        serializer = CouponSerializer(coupon, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'The Coupon is updated.'}, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        coupon = get_object_or_404(Coupon, pk=pk)
        self.check_object_permissions(request, coupon)
        coupon.delete()
        return Response({'message': 'The Coupon is deleted.'}, status=status.HTTP_204_NO_CONTENT)


class CartViewSet(ViewSet):
    permission_classes = [IsCartOwnerOrAdmin]
    
    def list(self, request):
        if request.user.is_staff:
            queryset = Cart.objects.all()
        else:
            queryset = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        cart = get_object_or_404(Cart, pk=pk)
        self.check_object_permissions(request, cart)
        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        if Cart.objects.filter(user=request.user).exists():
            return Response(
                {"detail": "User already has a cart."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        serializer = CartSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        cart = get_object_or_404(Cart, pk=pk)
        self.check_object_permissions(request, cart)
        serializer = CartSerializer(cart, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        cart = get_object_or_404(Cart, pk=pk)
        self.check_object_permissions(request, cart)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
