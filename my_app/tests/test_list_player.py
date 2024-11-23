## /////////////////////////////////////////////////////////////////////////////
## TESTING AREA
## THIS IS AN AREA WHERE YOU CAN TEST YOUR WORK AND WRITE YOUR TESTS
## /////////////////////////////////////////////////////////////////////////////

from rest_framework.test import APITestCase, RequestsClient, APIClient
from django.test import TestCase

from ..models.player import Player
from ..models.player_skill import PlayerSkill
import json

class ListPlayerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()

    def setUp(self):
        Player.objects.all().delete()
        PlayerSkill.objects.all().delete()

    def test_sample(self):
        data = {
            "name": "stesting",
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
        self.client.post("http://testserver/api/player",
                         data=data,
                         content_type='application/json')
        self.client.post("http://testserver/api/player",
                                 data=data,
                                 content_type='application/json')
        self.client.post("http://testserver/api/player",
                                            data=data,
                                            content_type='application/json')
        self.assertEqual(Player.objects.count(), 3)
        response = self.client.get("http://testserver/api/player")
        self.assertEqual(response.content, b'[{"id": 1, "name": "stesting", "position": "midfielder", "playerSkills": [{"id": 1, "skill": "defense", "value": 60, "playerId": 1}, {"id": 2, "skill": "attack", "value": 20, "playerId": 1}, {"id": 3, "skill": "speed", "value": 80, "playerId": 1}]}, {"id": 2, "name": "stesting", "position": "midfielder", "playerSkills": [{"id": 4, "skill": "defense", "value": 60, "playerId": 2}, {"id": 5, "skill": "attack", "value": 20, "playerId": 2}, {"id": 6, "skill": "speed", "value": 80, "playerId": 2}]}, {"id": 3, "name": "stesting", "position": "midfielder", "playerSkills": [{"id": 7, "skill": "defense", "value": 60, "playerId": 3}, {"id": 8, "skill": "attack", "value": 20, "playerId": 3}, {"id": 9, "skill": "speed", "value": 80, "playerId": 3}]}]')


