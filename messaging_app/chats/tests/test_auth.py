from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from chats.models import User, Conversation, Message
import uuid

class AuthAndAccessTests(APITestCase):

    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            password='password123',
            first_name='User ',
            last_name='One'
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            password='password123',
            first_name='User ',
            last_name='Two'
        )

        # Create a conversation with user1 and user2
        self.conversation = Conversation.objects.create()
        self.conversation.participants_id.set([self.user1, self.user2])
        self.conversation.save()

        # Create a message from user1
        self.message = Message.objects.create(
            sender_id=self.user1,
            conversation_id=self.conversation,
            message_body="Hello from user1"
        )

        # Obtain JWT token for user1
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'email': 'user1@example.com', 'password': 'password123'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1_token = response.data['access']

        # Obtain JWT token for user2
        response = self.client.post(url, {'email': 'user2@example.com', 'password': 'password123'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user2_token = response.data['access']

    def test_user_can_list_own_conversations(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user1_token)
        url = reverse('conversation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should include the conversation created
        self.assertTrue(any(conv['conversation_id'] == str(self.conversation.conversation_id) for conv in response.data))

    def test_user_cannot_see_others_conversations(self):
        # Create a conversation with only user2
        conv2 = Conversation.objects.create()
        conv2.participants_id.set([self.user2])
        conv2.save()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user1_token)
        url = reverse('conversation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # user1 should NOT see conv2
        self.assertFalse(any(conv['conversation_id'] == str(conv2.conversation_id) for conv in response.data))

    def test_user_can_send_message_in_own_conversation(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user1_token)
        url = reverse('message-list')
        data = {
            'conversation_id': str(self.conversation.conversation_id),
            'message_body': 'New message from user1'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message_body'], 'New message from user1')
        self.assertEqual(response.data['sender']['user_id'], str(self.user1.user_id))

    def test_user_cannot_send_message_in_others_conversation(self):
        # Create a conversation with only user2
        conv2 = Conversation.objects.create()
        conv2.participants_id.set([self.user2])
        conv2.save()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user1_token)
        url = reverse('message-list')
        data = {
            'conversation_id': str(conv2.conversation_id),
            'message_body': 'Trying to send message in others conversation'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_unauthenticated_user_cannot_access(self):
        url = reverse('conversation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    