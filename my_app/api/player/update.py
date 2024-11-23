## /////////////////////////////////////////////////////////////////////////////
## YOU CAN FREELY MODIFY THE CODE BELOW IN ORDER TO COMPLETE THE TASK
## /////////////////////////////////////////////////////////////////////////////

from django.http.response import JsonResponse
from rest_framework.request import Request
from rest_framework import status
from typing import Any

from my_app.models import Player
from my_app.serializers.player import PlayerSerializer


def update_player_handler(request: Request, id: Any):
    try:
        player = Player.objects.get(pk=id)
    except Player.DoesNotExist:
        return JsonResponse({"message": f"Player with id {id} does not exist"}, status=status.HTTP_404_NOT_FOUND, safe=False)
    serializer = PlayerSerializer(player, data=request.data)
    if serializer.is_valid():
        updated_player = serializer.save()
        return JsonResponse(PlayerSerializer(updated_player).data, safe=False)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)
