from rest_framework import serializers

from .models import SubscriptionPlan, Subscription

from Users.serializers import UserSerializer




class SubscriptionPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscriptionPlan
        fields = "__all__"



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