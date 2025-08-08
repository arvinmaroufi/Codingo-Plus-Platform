from rest_framework import serializers
from .models import Coupon


class CouponSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Coupon
        fields = [
            'id',
            'code',
            'discount_value',
            'max_usage',
            'usage_count',
            'valid_from',
            'valid_to',
            'type_status',
            'user',
            'user_email',
            'user_username',
            'is_active',
        ]
        read_only_fields = ['usage_count', 'type_status', 'is_active']

    def validate(self, data):
        if 'valid_from' in data and 'valid_to' in data:
            if data['valid_from'] >= data['valid_to']:
                raise serializers.ValidationError(
                    {"valid_to": "End date must be after start date."}
                )
        return data
