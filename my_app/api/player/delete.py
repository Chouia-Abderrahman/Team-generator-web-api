## /////////////////////////////////////////////////////////////////////////////
## YOU CAN FREELY MODIFY THE CODE BELOW IN ORDER TO COMPLETE THE TASK
## /////////////////////////////////////////////////////////////////////////////

from django.http.response import JsonResponse
from rest_framework.request import Request
from rest_framework import status
from typing import Any
from rest_framework.permissions import BasePermission

from my_app.models import Player


class HasValidToken(BasePermission):
    def has_permission(self, request, view):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            return token == 'SkFabTZibXE1aE14ckpQUUxHc2dnQ2RzdlFRTTM2NFE2cGI4d3RQNjZmdEFITmdBQkE='
        return False

def delete_player_handler(request: Request, id: Any):
    try:
        player = Player.objects.get(pk=id)
    except Player.DoesNotExist:
        return JsonResponse({"message": f"Player with id {id} does not exist"}, status=status.HTTP_404_NOT_FOUND, safe=False)
    auth_header = request.headers.get('Authorization')
    if auth_header != 'Bearer SkFabTZibXE1aE14ckpQUUxHc2dnQ2RzdlFRTTM2NFE2cGI4d3RQNjZmdEFITmdBQkE=':
        return JsonResponse({'detail': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED, safe=False)

    player.delete()
    return JsonResponse("", status=status.HTTP_204_NO_CONTENT, safe=False)