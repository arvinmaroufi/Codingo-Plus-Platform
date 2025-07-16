from rest_framework import serializers

from .models import User





class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['password', 'groups', 'user_permissions']
    
    
    def update(self, instance, validated_data):

        request = self.context.get('request')
        
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.username = validated_data.get('username', instance.username)

        if request.user.is_staff:
            instance.email = validated_data.get('email', instance.email)
            instance.phone = validated_data.get('phone', instance.phone)
            instance.status = validated_data.get('status', instance.status)
            instance.is_admin = validated_data.get('is_admin', instance.is_admin)
            instance.is_active = validated_data.get('is_active', instance.is_active)
            instance.user_type = validated_data.get('user_type', instance.user_type)
        
        instance.save()
        return instance
