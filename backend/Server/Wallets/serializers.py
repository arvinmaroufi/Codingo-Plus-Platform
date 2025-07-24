from rest_framework import serializers
from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Wallet
        fields = [
            'id',
            'user',
            'user_email',
            'user_username',
            'value',
        ]
        read_only_fields = ['user']
