## /////////////////////////////////////////////////////////////////////////////
## TESTING AREA
## THIS IS AN AREA WHERE YOU CAN TEST YOUR WORK AND WRITE YOUR TESTS
## /////////////////////////////////////////////////////////////////////////////

from rest_framework.test import APITestCase, RequestsClient, APIClient
from django.test import TestCase
from rest_framework import status
from ..models.player import Player
from ..models.player_skill import PlayerSkill
import json
class UpdatePlayerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()

    def setUp(self):
        Player.objects.all().delete()
        PlayerSkill.objects.all().delete()
        self.data = {
            "name": "testing",
            "position": "midfielder",
            "playerSkills": [
                {
                    "skill": "defense",
                    "value": 60
                },
                {
                    "skill": "attack",
                    "value": 20
                },
                {
                    "skill": "speed",
                    "value": 80
                }
            ]
        }

    def test_update_player(self):

        response = self.client.post("http://testserver/api/player",
                                    data=self.data,
                                    content_type='application/json')
        id = json.loads(response.content.decode('utf-8'))['id']
        modified_data = {
            "name": "Modified",
            "position": "midfielder",
            "playerSkills": [
                {
                    "skill": "defense",
                    "value": 60
                }
            ]
        }
        response = self.client.put(f"http://testserver/api/player/{id}",
                         data=modified_data,
                         content_type='application/json')
        self.assertEqual(response.content, b'{"id": 1, "name": "Modified", "position": "midfielder", "playerSkills": [{"id": 1, "skill": "defense", "value": 60, "playerId": 1}]}')

    def test_update_nonexistent_player(self):
        url = f"/api/player/{1000}"
        response = self.client.put(url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)