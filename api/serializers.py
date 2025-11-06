from rest_framework import serializers
from .models import Card, Team, User

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        # Indico el modelo
        model = Card

        # Indico los campos que deben pasarse a JSON
        fields = [
            "id",
            "name",
            "country",
            "club",
            "league",
            "position",
            "pace",
            "shooting",
            "passing",
            "dribbling",
            "defending",
            "physical",
            "diving",
            "reflexes",
            "handling",
            "positioning",
            "kicking",
            "speed",
            "active",
            "overall_rating",
            "created_at",
        ]

        # Estos campos se mandan en el GET pero no se pueden recibir en el POST/PUT/PATCH
        read_only_fields = ["id", "overall_rating", "created_at"]

    def validate(self, data):
        """Ensure stats are within a reasonable range."""
        stats = [
            "pace",
            "shooting",
            "passing",
            "dribbling",
            "defending",
            "physical",
            "diving",
            "reflexes",
            "handling",
            "positioning",
            "kicking",
            "speed",
        ]
        for stat in stats:
            value = data.get(stat)
            if value is not None and (value < 0 or value > 99):
                raise serializers.ValidationError(
                    {stat: "Each stat must be between 0 and 99."}
                )
        return data


class TeamSerializer(serializers.ModelSerializer):
    # Indicamos el serializer de las cartas del equipo
    cards = CardSerializer(many=True, read_only=True)
    card_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Card.objects.all(),
        write_only=True,
        required=False,
        source="cards",
    )

    class Meta:
        # Indico el modelo
        model = Team

        # Indico los campos que deben pasarse a JSON
        fields = ["id", "name", "created_at", "cards", "card_ids"]

        # Estos campos se mandan en el GET pero no se pueden recibir en el POST/PUT/PATCH
        read_only_fields = ["id", "created_at"]

    # Override del update para poder pasar solo las ids al modificar las cartas que tiene un equipo
    def update(self, instance, validated_data):
        # Handle updating cards if provided
        cards = validated_data.pop("cards", None)
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        if cards is not None:
            instance.cards.set(cards)
        return instance


class UserSerializer(serializers.ModelSerializer):
    # Indicamos el serializer del equipo del usuario
    team = TeamSerializer(read_only=True)
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), write_only=True, required=False, source="team"
    )

    class Meta:
        model = User
        fields = ["id", "name", "email", "created_at", "team", "team_id"]
        read_only_fields = ["id", "created_at"]
