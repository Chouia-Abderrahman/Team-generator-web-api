## /////////////////////////////////////////////////////////////////////////////
## TESTING AREA
## THIS IS AN AREA WHERE YOU CAN TEST YOUR WORK AND WRITE YOUR TESTS
## /////////////////////////////////////////////////////////////////////////////
from rest_framework import status
from rest_framework.test import APITestCase, RequestsClient, APIClient

from ..models.player import Player
from ..models.player_skill import PlayerSkill

class ProcessTeamTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()

    def setUp(self):
        Player.objects.all().delete()
        PlayerSkill.objects.all().delete()


        # Create sample players
        self.player1 = Player.objects.create(name='Player 1', position='defender')
        self.player2 = Player.objects.create(name='Player 2', position='defender')
        self.player3 = Player.objects.create(name='Player 3', position='midfielder')

        # Create sample skills for the players
        PlayerSkill.objects.create(player=self.player1, skill='speed', value=90)
        PlayerSkill.objects.create(player=self.player1, skill='strength', value=20)
        PlayerSkill.objects.create(player=self.player2, skill='speed', value=70)
        PlayerSkill.objects.create(player=self.player3, skill='speed', value=85)

        self.url = 'http://testserver/api/team/process'

    def test_sufficient_players_for_position(self):
        data = [
            {'position': 'defender', 'mainSkill': 'speed', 'numberOfPlayers': 2}
        ]
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_insufficient_players_for_position(self):
        data = [
            {'position': 'defender', 'mainSkill': 'speed', 'numberOfPlayers': 3}
        ]
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], 'Insufficient number of players for position: defender')

    def test_no_players_with_required_skill(self):
        data = [
            {'position': 'midfielder', 'mainSkill': 'defense', 'numberOfPlayers': 1}
        ]
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], 'Player 3')

    def test_select_based_on_highest_skill_when_no_main_skill(self):
        data = [
            {'position': 'defender', 'mainSkill': 'defense', 'numberOfPlayers': 1}
        ]
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'],
                         'Player 1')  # The player with the highest skill value in the 'defender' position

    def test_duplicate_skill_requirement_for_position(self):
        data = [
            {'position': 'defender', 'mainSkill': 'speed', 'numberOfPlayers': 1},
            {'position': 'defender', 'mainSkill': 'speed', 'numberOfPlayers': 1}
        ]
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], 'Duplicate skill requirement for position: defender')

    def test_different_skills_for_same_position(self):
        data = [
            {'position': 'defender', 'mainSkill': 'speed', 'numberOfPlayers': 1},
            {'position': 'defender', 'mainSkill': 'strength', 'numberOfPlayers': 1}
        ]
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        names = [player['name'] for player in response.json()]
        self.assertIn('Player 1', names)
        self.assertIn('Player 2', names)
