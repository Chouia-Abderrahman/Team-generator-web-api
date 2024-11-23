## /////////////////////////////////////////////////////////////////////////////
## YOU CAN FREELY MODIFY THE CODE BELOW IN ORDER TO COMPLETE THE TASK
## /////////////////////////////////////////////////////////////////////////////

from django.http.response import JsonResponse
from rest_framework.request import Request
from rest_framework import status

from my_app.models import Player
from my_app.serializers.player import PlayerSerializer


def get_player_list_handler(request: Request):
    players = Player.objects.all()
    serializer = PlayerSerializer(players, many=True)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
