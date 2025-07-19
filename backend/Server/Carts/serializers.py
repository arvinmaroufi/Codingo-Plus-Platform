from rest_framework import serializers
from .models import Coupon, CourseItem, Cart


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


class CartSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    coupon_code = serializers.CharField(source='coupon.code', read_only=True)
    items = CourseItemSerializer(many=True, read_only=True, source='course_items')
    total_price = serializers.IntegerField(read_only=True)
    final_price = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'user_email',
            'user_username',
            'coupon',
            'coupon_code',
            'coupon_discount',
            'items',
            'total_price',
            'final_price',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['coupon_discount', 'created_at', 'updated_at']

    def validate_coupon(self, value):
        if value and not value.is_valid(self.context['request'].user):
            raise serializers.ValidationError("This coupon is not valid.")
        return value

    def update(self, instance, validated_data):
        coupon = validated_data.get('coupon', None)
        
        if coupon:
            if coupon.is_valid(instance.user):
                instance.coupon = coupon
                instance.coupon_discount = coupon.discount_value
            else:
                raise serializers.ValidationError({"coupon": "This coupon is not valid."})
        elif 'coupon' in validated_data and coupon is None:
            instance.coupon = None
            instance.coupon_discount = 0
            
        instance.save()
        return instance
