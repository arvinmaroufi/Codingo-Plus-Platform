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
