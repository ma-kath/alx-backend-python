from rest_framework import permissions


class IsParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """

    def has_object_permission(self, request, view, obj):
        # For Conversation objects
        if hasattr(obj, 'participants_id'):
            return request.user in obj.participants_id.all()
        
        # For Message objects
        if hasattr(obj, 'conversation_id'):
            return request.user in obj.conversation_id.participants_id.all()
        
        return False