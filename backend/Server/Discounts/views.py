from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ViewSet
from rest_framework.views import Response, APIView
from rest_framework import status

from .models import Coupon
from .serializers import CouponSerializer
from .permissions import IsCouponOwnerOrAdmin



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
    