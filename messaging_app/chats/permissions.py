from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """
    
    def has_permission(self, request, view):
        """" Allow access only to authenticated users """
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        
        write_methods = ['PUT', 'PATCH', 'DELETE']
        
        # For Conversation objects
        if hasattr(obj, 'participants_id'):
            if request.method in SAFE_METHODS:
                return request.user in obj.participants_id.all()
            if request.method in write_methods:
                return request.user in obj.participants_id.all()
            return False
        
        # For Message objects
        if hasattr(obj, 'conversation_id'):
            if request.method in SAFE_METHODS:
                return request.user in obj.conversation_id.participants_id.all()
            if request.method in write_methods:
                return request.user in obj.conversation_id.participants_id.all()
            return False
        
        return False