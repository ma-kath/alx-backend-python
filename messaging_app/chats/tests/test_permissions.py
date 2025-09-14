# chats/tests/test_permissions.py
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from chats.models import User, Conversation, Message

class PermissionTests(APITestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(email='user1@example.com', password='pass1234')
        self.user2 = User.objects.create_user(email='user2@example.com', password='pass1234')
        self.user3 = User.objects.create_user(email='user3@example.com', password='pass1234')  # Not a participant

        # Create conversation with user1 and user2 as participants
        self.conversation = Conversation.objects.create()
        self.conversation.participants_id.set([self.user1, self.user2])
        self.conversation.save()

        # Create a message in the conversation by user1
        self.message = Message.objects.create(
            conversation_id=self.conversation,
            sender_id=self.user1,
            message_body="Hello"
        )

        # URLs (adjust according to your router setup)
        self.conversation_url = reverse('conversation-detail', args=[self.conversation.conversation_id])
        self.message_url = reverse('message-detail', args=[self.message.message_id])
        self.message_list_url = reverse('message-list')

        # Clients for each user
        self.client1 = APIClient()
        self.client1.force_authenticate(user=self.user1)

        self.client2 = APIClient()
        self.client2.force_authenticate(user=self.user2)

        self.client3 = APIClient()
        self.client3.force_authenticate(user=self.user3)

    def test_participant_can_view_conversation(self):
        response = self.client1.get(self.conversation_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_participant_cannot_view_conversation(self):
        response = self.client3.get(self.conversation_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_participant_can_view_message(self):
        response = self.client2.get(self.message_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_participant_cannot_view_message(self):
        response = self.client3.get(self.message_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_participant_can_update_message(self):
        data = {'message_body': 'Updated message'}
        response = self.client1.patch(self.message_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.message.refresh_from_db()
        self.assertEqual(self.message.message_body, 'Updated message')

    def test_non_participant_cannot_update_message(self):
        data = {'message_body': 'Hacked message'}
        response = self.client3.put(self.message_url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_participant_can_delete_message(self):
        response = self.client2.delete(self.message_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Message.objects.filter(pk=self.message.pk).exists())

    def test_non_participant_cannot_delete_message(self):
        # Recreate message for this test
        message = Message.objects.create(
            conversation_id=self.conversation,
            sender_id=self.user1,
            message_body="Another message"
        )
        url = reverse('message-detail', args=[message.message_id])
        response = self.client3.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_participant_can_create_message(self):
        data = {
            'conversation_id': str(self.conversation.conversation_id),
            'message_body': 'New message'
        }
        response = self.client1.post(self.message_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_non_participant_cannot_create_message(self):
        data = {
            'conversation_id': str(self.conversation.conversation_id),
            'message_body': 'Intruder message'
        }
        response = self.client3.post(self.message_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
