from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ViewSet
from rest_framework.views import Response, APIView
from rest_framework import status

from .models import Wallet
from .serializers import WalletSerializer
from .permissions import IsWalletOwnerOrAdmin



class WalletViewSet(ViewSet):
    
    permission_classes = [IsWalletOwnerOrAdmin]
    
    def list(self, request):
        if request.user.is_staff:
            queryset = Wallet.objects.all()
        else:
            queryset = Wallet.objects.filter(user=request.user)
        serializer = WalletSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        wallet = get_object_or_404(Wallet, pk=pk)
        self.check_object_permissions(request, wallet)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)

    def create(self, request):
        if Wallet.objects.filter(user=request.user).exists():
            return Response(
                {"detail": "User already has a wallet."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        serializer = WalletSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        wallet = get_object_or_404(Wallet, pk=pk)
        self.check_object_permissions(request, wallet)
        serializer = WalletSerializer(wallet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        wallet = get_object_or_404(Wallet, pk=pk)
        self.check_object_permissions(request, wallet)
        wallet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def my_wallet(self, request):
        wallet = get_object_or_404(Wallet, user=request.user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data, status=status.HTTP_200_OK)
