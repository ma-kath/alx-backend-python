from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """
    
    def has_permission(self, request, view):
        # Allow access only to authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # For Conversation objects
        if hasattr(obj, 'participants_id'):
            return request.user in obj.participants_id.all()
        
        # For Message objects
        if hasattr(obj, 'conversation_id'):
            return request.user in obj.conversation_id.participants_id.all()
        
        return False