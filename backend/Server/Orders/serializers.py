from rest_framework import serializers
from .models import Order, OrderCourseItem


class OrderCourseItemSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_slug = serializers.CharField(source='course.slug', read_only=True)
    formatted_price = serializers.CharField(read_only=True)

    class Meta:
        model = OrderCourseItem
        fields = [
            'id',
            'order',
            'course',
            'course_title',
            'course_slug',
            'price',
            'formatted_price',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['price', 'formatted_price', 'created_at', 'updated_at']


class OrderSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    course_items = OrderCourseItemSerializer(many=True, read_only=True)
    formatted_final_price = serializers.CharField(read_only=True)
    formatted_tax = serializers.CharField(read_only=True)
    formatted_discount = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'order_id',
            'user',
            'user_email',
            'user_username',
            'cart',
            'total_price',
            'tax',
            'discount',
            'final_price',
            'formatted_final_price',
            'formatted_tax',
            'formatted_discount',
            'course_items',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'order_id',
            'total_price',
            'tax',
            'discount',
            'final_price',
            'formatted_final_price',
            'formatted_tax',
            'formatted_discount',
            'created_at',
            'updated_at',
        ]

    def validate_cart(self, value):
        if value.user != self.context['request'].user:
            raise serializers.ValidationError("This cart does not belong to you.")
        
        if hasattr(value, 'order'):
            raise serializers.ValidationError("This cart has already been ordered.")
            
        return value

    def create(self, validated_data):
        order = super().create(validated_data)
        cart = order.cart
        
        for item in cart.course_items.all():
            OrderCourseItem.objects.create(
                order=order,
                course=item.course,
                price=item.price
            )
            
        return order
