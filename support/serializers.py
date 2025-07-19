from rest_framework import serializers
from .models import SupportTicket, SupportMessage, SupportFAQ
from users.serializers import UsersSerializer


class SupportMessageSerializer(serializers.ModelSerializer):
    sender = UsersSerializer(read_only=True)
    sender_name = serializers.CharField(source='sender.name', read_only=True)
    
    class Meta:
        model = SupportMessage
        fields = [
            'id', 'ticket', 'sender', 'sender_name', 'message_type', 
            'content', 'attachment', 'created_at', 'is_read'
        ]
        read_only_fields = ['sender', 'created_at']


class SupportTicketSerializer(serializers.ModelSerializer):
    user = UsersSerializer(read_only=True)
    assigned_to = UsersSerializer(read_only=True)
    messages = SupportMessageSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.name', read_only=True)
    unread_messages_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SupportTicket
        fields = [
            'id', 'user', 'user_name', 'title', 'category', 'priority', 
            'status', 'created_at', 'updated_at', 'resolved_at', 
            'assigned_to', 'assigned_to_name', 'messages', 'unread_messages_count'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def get_unread_messages_count(self, obj):
        return obj.messages.filter(is_read=False, message_type='support').count()


class SupportTicketCreateSerializer(serializers.ModelSerializer):
    initial_message = serializers.CharField(write_only=True, help_text="الرسالة الأولى")
    
    class Meta:
        model = SupportTicket
        fields = ['title', 'category', 'priority', 'initial_message']
    
    def create(self, validated_data):
        initial_message = validated_data.pop('initial_message')
        # للاختبار نستخدم المستخدم رقم 5
        from users.models import Users
        user = Users.objects.get(id=5)
        
        ticket = SupportTicket.objects.create(user=user, **validated_data)
        
        # إنشاء الرسالة الأولى
        SupportMessage.objects.create(
            ticket=ticket,
            sender=user,
            message_type='user',
            content=initial_message
        )
        
        return ticket


class SupportMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportMessage
        fields = ['ticket', 'content', 'attachment']
    
    def create(self, validated_data):
        # للاختبار نستخدم المستخدم رقم 5
        from users.models import Users
        user = Users.objects.get(id=5)
        
        # تحديد نوع الرسالة بناءً على المستخدم
        if hasattr(user, 'is_staff') and user.is_staff:
            message_type = 'support'
        else:
            message_type = 'user'
        
        return SupportMessage.objects.create(
            sender=user,
            message_type=message_type,
            **validated_data
        )


class SupportFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportFAQ
        fields = ['id', 'question', 'answer', 'category', 'order']