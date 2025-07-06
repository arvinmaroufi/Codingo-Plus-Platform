from rest_framework import serializers

from .models import SubscriptionPlan, Subscription

from Users.serializers import UserSerializer




class SubscriptionPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscriptionPlan
        fields = "__all__"


    def create(self, validated_data):
        query = SubscriptionPlan.objects.create(**validated_data)
        query.save()
        return query


    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.description = validated_data.get('description', instance.description)
        instance.price_per_day = validated_data.get('price_per_day', instance.price_per_day)

        instance.save()

        return instance


class SubscriptionSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    plan = SubscriptionPlanSerializer(read_only=True)

    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = "__all__"
        read_only_fields = ['user', 'plan', 'status']
    
    
    def get_is_active(self, obj):
        return obj.is_active()