from rest_framework import serializers
from .models import Department, Ticket, TicketMessage, TicketAttachment, CourseDepartment, CourseTicket
from Courses.serializers import CourseSerializer


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            'name',
            'description',
        ]
        
    
    def create(self, validated_data):
        return Department.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        
        return instance
        
        
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            'subject',
            'user',
            'department',
            'priority',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']
    
        
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Ticket.objects.create(**validated_data)


class TicketMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketMessage
        fields = [
            'id',
            'ticket',
            'user',
            'message',
            'created_at',
        ]
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return TicketMessage.objects.create(**validated_data)
    
    
class TicketAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketAttachment
        fields = [
            'id',
            'message',
            'file',
            'uploaded_at',
        ]
        read_only_fields = ['uploaded_at']


class CourseDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDepartment
        fields = [
            'name',
            'description',
        ]
        
    
    def create(self, validated_data):
        return CourseDepartment.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        
        return instance
        

class CourseTicketSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    department = CourseDepartmentSerializer(read_only=True)
    
    class Meta:
        model = CourseTicket
        fields = [
            'id',
            'subject',
            'user',
            'course',
            'department',
            'priority',
            'status',
            'created_at',
            'updated_at',
            'closed_at',
        ]
        read_only_fields = ['user', 'created_at', 'updated_at', 'closed_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return CourseTicket.objects.create(**validated_data)
    
