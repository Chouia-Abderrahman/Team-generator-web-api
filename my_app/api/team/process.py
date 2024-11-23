## /////////////////////////////////////////////////////////////////////////////
## YOU CAN FREELY MODIFY THE CODE BELOW IN ORDER TO COMPLETE THE TASK
## /////////////////////////////////////////////////////////////////////////////

from django.http.response import JsonResponse
from rest_framework.request import Request
from rest_framework import status
from django.db.models import Max, F

from my_app.models import Player
from my_app.serializers.player import PlayerSerializer


def team_process_handler(request: Request):
    requirements = request.data
    selected_players = []
    used_player_ids = set()

    # Track the skills already processed for each position
    skill_requirements = {}

    for req in requirements:
        position = req['position']
        main_skill = req['mainSkill']
        number_of_players = req['numberOfPlayers']

        if position not in skill_requirements:
            skill_requirements[position] = set()

        if main_skill in skill_requirements[position]:
            return JsonResponse({
                "message": f"Duplicate skill requirement for position: {position}"
            }, status=status.HTTP_400_BAD_REQUEST, safe=False)

        skill_requirements[position].add(main_skill)

        # Check if there are enough players for this position
        available_players = Player.objects.filter(position=position).exclude(id__in=used_player_ids)
        if available_players.count() < number_of_players:
            return JsonResponse({
                "message": f"Insufficient number of players for position: {position}"
            }, status=status.HTTP_400_BAD_REQUEST, safe=False)

        # Find players with the main skill
        players_with_skill = available_players.filter(playerSkills__skill=main_skill)

        if players_with_skill.exists():
            # If players with the main skill exist, select the best ones
            best_players = players_with_skill.annotate(
                skill_value=F('playerSkills__value')).order_by('-skill_value')[:number_of_players]
        else:
            # If no players with the main skill, select based on highest skill
            best_players = available_players.annotate(
                max_skill=Max('playerSkills__value')
            ).order_by('-max_skill')[:number_of_players]

        for player in best_players:
            selected_players.append(player)
            used_player_ids.add(player.id)

    # Serialize the selected players
    serializer = PlayerSerializer(selected_players, many=True, context={'main_skill': req['mainSkill']})
    return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
