from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing conversations."""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    #permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants_id__email', 'conversation_id']
    ordering_fields = ['created_at']
    
    def create(self, request, *args, **kwargs):
        """Create a new conversation."""
        participants_ids = request.data.get('participants_id', [])
        if not participants_ids or not isinstance(participants_ids, list):
            return Response(
                {"Error": "Participants list is required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        #Fetch users and create conversation
        participants = User.objects.filter(user_id__in=participants_ids)
        if participants.count() != len(participants_ids):
            return Response(
                {"Error": "One or more participants not found."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        conversation = Conversation.objects.create()
        conversation.participants_id.set(participants)
        conversation.save()
        
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for managing messages."""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    #permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['message_body', 'sender_id__email']
    ordering_fields = ['sent_at']
    
    def create(self, request, *args, **kwargs):
        """Send a message to an existing conversation."""
        conversation_id = request.data.get("conversation_id")
        message_body = request.data.get("message_body")
        
        if not conversation_id or not message_body:
            return Response(
                {"detail": "conversation and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"detail": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        # Check if the sender is a participant in the conversation
        if not conversation.participants_id.filter(user_id=request.user.user_id).exists():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
        message = Message.objects.create(
            sender_id=request.user,
            conversation_id=conversation,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)