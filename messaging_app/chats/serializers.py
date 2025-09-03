from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['user_id', 'firstname', 'lastname', 'email', 'phone_number', 'role', 'created_at']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class MessageSerializer(serializers.ModelSerializer):
    sender_id = UserSerializer(read_only=True)
    message_body = serializers.CharField()
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender_id', 'conversation_id', 'message_body', 'sent_at']
        
    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value

        
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants_id', 'created_at']
    
    def get_message_count(self, obj):
        return obj.messages.count()