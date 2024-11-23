from rest_framework import serializers 

from ..models.player_skill import PlayerSkill

class PlayerSkillSerializer(serializers.ModelSerializer):

    value = serializers.IntegerField()
    playerId = serializers.SerializerMethodField()

    def validate_skill(self, value):
        valid_skills = dict(PlayerSkill.skill_choices).keys()
        if value not in valid_skills:
            raise serializers.ValidationError(f"Invalid value for skill: {value}")
        return value

    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except serializers.ValidationError as e:
            if 'skill' in e.detail:
                raise serializers.ValidationError(f"Invalid value for skill: {data.get('skill', '')}")
            elif 'value' in e.detail:
                raise serializers.ValidationError(f"Invalid value for skill level: {data.get('value', '')}")
            raise
    class Meta:
        model = PlayerSkill
        fields = ['id', 'skill', 'value', 'playerId']
        read_only_fields = ['id', 'playerId']

    def get_playerId(self, obj):
        return obj.player.id if obj.player else None