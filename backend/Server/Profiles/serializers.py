from rest_framework import serializers

from .models import AdminProfile, StudentProfile, TeacherProfile, SupporterProfile
from Users.serializers import User







class AdminProfileSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = AdminProfile
        fields = "__all__"


    def update(self, instance, validated_data):
        instance.age = validated_data.get('age', instance.age)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.is_available = validated_data.get('is_available', instance.is_available)
        instance.profile_banner = validated_data.get('profile_banner', instance.profile_banner)

        instance.save()
        return instance