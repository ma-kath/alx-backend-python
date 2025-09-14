from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'user_id', 'first_name', 'last_name', 
            'email', 'phone_number', 'role', 'created_at',
            'full_name',
        ]
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(source='sender_id', read_only=True)
    message_body = serializers.CharField()
    
    class Meta:
        model = Message
        fields = [
            'message_id', 'sender', 'conversation_id', 
            'message_body', 'sent_at'
        ]
        
    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value

        
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(source='participants_id', many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants_id', 
            'created_at', 'messages', 'message_count', 'participants'
        ]
    
    def get_message_count(self, obj):
        return obj.messages.count()