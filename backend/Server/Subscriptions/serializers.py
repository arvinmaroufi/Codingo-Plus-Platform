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

    plan_slug = serializers.CharField(write_only=True, required=False)


    class Meta:
        model = Subscription
        fields = "__all__"
        read_only_fields = ['user', 'plan', 'status']


    def update(self, instance, validated_data):

        plan_slug = validated_data.pop('plan_slug', None)
        if plan_slug is not None:
            try:
                plan =  SubscriptionPlan.objects.get(slug=plan_slug)
                instance.plan = plan
            except  SubscriptionPlan.DoesNotExist:
                raise serializers.ValidationError({'plan_slug': 'پلن پیدا نشد.'})
        
        instance.status = validated_data.get('status', instance.status)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.starts_at = validated_data.get('starts_at', instance.starts_at)
        instance.expires_at = validated_data.get('expires_at', instance.expires_at)

        instance.save()

        return instance
        

    def get_is_active(self, obj):
        return obj.is_active()