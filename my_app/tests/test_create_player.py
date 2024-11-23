## /////////////////////////////////////////////////////////////////////////////
## TESTING AREA
## THIS IS AN AREA WHERE YOU CAN TEST YOUR WORK AND WRITE YOUR TESTS
## /////////////////////////////////////////////////////////////////////////////
from rest_framework import status
from rest_framework.test import APITestCase, RequestsClient, APIClient
from django.urls import reverse
from django.test import TestCase

from ..models.player import Player
from ..models.player_skill import PlayerSkill
import json


class CreatePlayerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        cls.endpoint = '/api/player'

    def setUp(self):
        Player.objects.all().delete()
        PlayerSkill.objects.all().delete()

    def test_successful_player_creation(self):
        data = {
            "name": "test",
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
        response = self.client.post("http://testserver/api/player",
                                    data=data,
                                    content_type='application/json')
        self.assertEqual(response.content,
              b'{"id": 1, "name": "test", "position": "midfielder", "playerSkills": [{"id": 1, "skill": "defense", "value": 60, "playerId": 1}, {"id": 2, "skill": "attack", "value": 20, "playerId": 1}, {"id": 3, "skill": "speed", "value": 80, "playerId": 1}]}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Player.objects.count(), 1)
        self.assertEqual(PlayerSkill.objects.count(), 3)

    def test_unsuccessful_creation_no_skills(self):
        data = {
            "name": "test",
            "position": "midfielder",
            "playerSkills": []
        }
        response = self.client.post("http://testserver/api/player",
                                    data=data,
                                    content_type='application/json')
        self.assertEqual(response.content, b'{"message": "Player must have at least one skill"}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Player.objects.count(), 0)

    def test_unsuccessful_creation_duplicate_skills(self):
        data = {
            "name": "test",
            "position": "midfielder",
            "playerSkills": [
                {
                    "skill": "defense",
                    "value": 200
                },
                {
                    "skill": "defense",
                    "value": 20
                }
            ]
        }
        response = self.client.post("http://testserver/api/player",
                                    data=data,
                                    content_type='application/json')
        self.assertEqual(response.content, b'{"message": "Player cannot have duplicate skills"}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Player.objects.count(), 0)

    def test_unsuccessful_creation_invalid_position(self):
        data = {
            "name": "test",
            "position": "midfielder1",
            "playerSkills": [
                {
                    "skill": "defense",
                    "value": 200
                },
                {
                    "skill": "attack",
                    "value": 20
                },
                {
                    "skill": "speed",
                    "value": 20000
                }
            ]
        }
        response = self.client.post("http://testserver/api/player",
                                    data=data,
                                    content_type='application/json')
        self.assertEqual(response.content, b'{"message": "Invalid value for position: midfielder1"}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Player.objects.count(), 0)

    def test_unsuccessful_creation_invalid_skill(self):
        data = {
            "name": "test",
            "position": "midfielder",
            "playerSkills": [
                {
                    "skill": "defense1",
                    "value": 200
                },
                {
                    "skill": "attack",
                    "value": 20
                }
            ]
        }
        response = self.client.post("http://testserver/api/player",
                                    data=data,
                                    content_type='application/json')
        self.assertEqual(response.content, b'{"message": "Invalid value for skill: defense1"}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Player.objects.count(), 0)
