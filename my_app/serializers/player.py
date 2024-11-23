from rest_framework import serializers 

from .player_skill import PlayerSkillSerializer
from ..models.player import Player
from ..models.player_skill import PlayerSkill

class PlayerSerializer(serializers.ModelSerializer):
    playerSkills = PlayerSkillSerializer(many=True)

    class Meta:
        model = Player
        fields = ['id', 'name', 'position', 'playerSkills']
        read_only_fields = ['id']

    def validate_position(self, value):
        valid_positions = dict(Player.POSITION_CHOICES).keys()
        if value not in valid_positions:
            raise serializers.ValidationError(f"Invalid value for position: {value}")
        return value

    def validate_playerSkills(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("Player must have at least one skill")

        skill_names = [skill['skill'] for skill in value]
        if len(skill_names) != len(set(skill_names)):
            raise serializers.ValidationError("Player cannot have duplicate skills")
        return value

    def create(self, validated_data):
        skills_data = validated_data.pop('playerSkills')
        player = Player.objects.create(**validated_data)
        for skill_data in skills_data:
            PlayerSkill.objects.create(player=player, **skill_data)
        return player

    def update(self, instance, validated_data):
        skills_data = validated_data.pop('playerSkills', [])
        instance = super().update(instance, validated_data)

        # Update or create skills
        existing_skills = list(instance.playerSkills.all())
        for skill_data in skills_data:
            if existing_skills:
                skill = existing_skills.pop(0)
                for attr, value in skill_data.items():
                    setattr(skill, attr, value)
                skill.save()
            else:
                PlayerSkill.objects.create(player=instance, **skill_data)

        # Delete any remaining existing skills
        for skill in existing_skills:
            skill.delete()

        return instance
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['playerSkills'] = PlayerSkillSerializer(instance.playerSkills.all(), many=True).data
        return representation

    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except serializers.ValidationError as e:
            error_dict = {"message": "Validation error"}
            if 'position' in e.detail:
                error_dict["message"] = e.detail['position'][0]
            elif 'playerSkills' in e.detail:
                playerSkills_errors = e.detail['playerSkills']
                for skill_error in playerSkills_errors:
                    if skill_error:  # Check if the error is not empty
                        if isinstance(skill_error, dict):
                            # If it's a dict, get the first error message
                            error_dict["message"] = str(next(iter(skill_error.values()))[0][0])
                        elif isinstance(skill_error, list):
                            error_dict["message"] = skill_error[0]
                        else:
                            # If it's not a dict, it's probably already a string
                            error_dict["message"] = str(skill_error)
                        break
            raise serializers.ValidationError(error_dict)

    def get_playerSkills(self, obj):
        main_skill = self.context.get('main_skill')
        if main_skill:
            playerSkills = obj.playerSkills.filter(skill_name=main_skill)
        else:
            playerSkills = obj.playerSkills.all().order_by('-value')[:1]
        return PlayerSkillSerializer(playerSkills, many=True).data