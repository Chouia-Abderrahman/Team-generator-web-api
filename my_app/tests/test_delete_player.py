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
class DeletePlayerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()


    def setUp(self):
        Player.objects.all().delete()
        PlayerSkill.objects.all().delete()
        self.player = Player.objects.create(name="Test Player", position="midfielder")
        self.valid_token = "Bearer SkFabTZibXE1aE14ckpQUUxHc2dnQ2RzdlFRTTM2NFE2cGI4d3RQNjZmdEFITmdBQkE="

    def test_delete_player(self):

        response = self.client.delete(f"http://testserver/api/player/{self.player.id}",
                         HTTP_AUTHORIZATION="Bearer SkFabTZibXE1aE14ckpQUUxHc2dnQ2RzdlFRTTM2NFE2cGI4d3RQNjZmdEFITmdBQkE=",
                         content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Player.objects.filter(id=self.player.id).exists())

    def test_delete_player_invalid_token(self):
        response = self.client.delete(
            f"http://testserver/api/player/{self.player.id}",
            HTTP_AUTHORIZATION="Bearer InvalidToken"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Invalid token.'})
        self.assertTrue(Player.objects.filter(id=self.player.id).exists())

    def test_delete_player_no_token(self):
        response = self.client.delete(f"http://testserver/api/player/{self.player.id}")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Invalid token.'})
        self.assertTrue(Player.objects.filter(id=self.player.id).exists())

    def test_delete_nonexistent_player(self):
        non_existent_id = self.player.id + 1
        url = f"/api/player/{non_existent_id}"
        response = self.client.delete(
            url,
            HTTP_AUTHORIZATION=self.valid_token
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"message": f"Player with id {non_existent_id} does not exist"})
