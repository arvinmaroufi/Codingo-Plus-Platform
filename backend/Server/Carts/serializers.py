from rest_framework import serializers
from .models import Coupon, CourseItem


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


class CourseItemSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_slug = serializers.CharField(source='course.slug', read_only=True)
    
    class Meta:
        model = CourseItem
        fields = [
            'id',
            'cart',
            'course',
            'course_title',
            'course_slug',
            'price',
            'created_at',
        ]
        read_only_fields = ['price', 'created_at']

    def create(self, validated_data):
        if 'price' not in validated_data or validated_data['price'] == 0:
            validated_data['price'] = validated_data['course'].price
        return super().create(validated_data)
