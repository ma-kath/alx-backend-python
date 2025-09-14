from rest_framework.exceptions import PermissionDenied
from .models import Conversation


def get_authenticated_user(request):
    """Retrieve the authenticated user from the request."""
    user = request.user
    if not user or not user.is_authenticated:
        raise PermissionDenied("Authentication credentials were not provided.")
    return user

def check_user_is_participant(request, conversation_id):
    """
    Raises PermissionDenied if the user is not a participant in the conversation.
    """
    user = get_authenticated_user(request)
    try:
        conversation = Conversation.objects.get(conversation_id=conversation_id)
    except Conversation.DoesNotExist:
        raise PermissionDenied("Conversation not found.")
    if not conversation.participants_id.filter(user_id=user.user_id).exists():
        raise PermissionDenied("You are not a participant in this conversation.")
    
    return conversation