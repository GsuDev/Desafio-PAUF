from django.shortcuts import render
from rest_framework import generics, status
from .serializers import *
from .models import *
from rest_framework.response import Response


# Views para listar todos los usuarios y crear uno nuevo
class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Views para obtener, actualizar o eliminar un usuario específico
class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"


# Views para listar todas las tarjetas y crear una nueva
class CardListCreate(generics.ListCreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


# Views para obtener, actualizar o eliminar una tarjeta específica
class CardRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        card = self.get_object()

        # Comprobamos si la carta está en algún equipo
        is_used = card.teams.exists()
        # De ser así no la borra
        if is_used:
            return Response(
                {"detail": "Cannot delete card because it is used in a team."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        card.active = False
        card.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Views para listar todos los equipos y crear uno nuevo
class TeamListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Views para obtener, actualizar o eliminar un equipo específico
class TeamRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"


class UserTeamView(generics.GenericAPIView):
    """
    Gestiona el equipo de un usuario:
    - GET: devuelve el equipo completo del usuario (con cartas)
    - POST: crea un equipo si no tiene
    - PATCH: actualiza el equipo (nombre o cartas)
    """

    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def get_user(self):
        user_id = self.kwargs.get("pk")
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    # GET → obtener el equipo del usuario
    def get(self, request, *args, **kwargs):
        user = self.get_user()
        if not user:
            return Response(
                {"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        if not user.team:
            return Response(
                {"error": "Este usuario no tiene equipo"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TeamSerializer(user.team)
        return Response(serializer.data)

    # POST → crear un nuevo equipo si no tiene
    def post(self, request, *args, **kwargs):
        user = self.get_user()
        if not user:
            return Response(
                {"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        if user.team:
            return Response(
                {"error": "Este usuario ya tiene un equipo asignado"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Verificar que el equipo no tenga más de 25 cartas
        cards_data = serializer.validated_data.get("cards", [])
        if len(cards_data) > 25:
            return Response(
                {"error": "Un equipo no puede tener más de 25 cartas."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Evitar duplicados en las cartas
        card_ids = [c.id for c in cards_data]
        if len(card_ids) != len(set(card_ids)):
            return Response(
                {"error": "El equipo contiene cartas duplicadas."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # TODO HU8 Lugar reservado para límites por tipo de jugador
        # self.check_position_limits(cards_data)

        team = serializer.save()

        user.team = team
        user.save()

        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)

    # PATCH → actualizar el equipo existente
    def patch(self, request, *args, **kwargs):
        user = self.get_user()
        if not user:
            return Response(
                {"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        if not user.team:
            return Response(
                {"error": "Este usuario no tiene equipo para actualizar"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(user.team, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Verificar que el equipo no tenga más de 25 cartas
        cards_data = serializer.validated_data.get("cards", [])
        if len(cards_data) > 25:
            return Response(
                {"error": "Un equipo no puede tener más de 25 cartas."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Evitar duplicados en las cartas
        card_ids = [c.id for c in cards_data]
        if len(card_ids) != len(set(card_ids)):
            return Response(
                {"error": "El equipo contiene cartas duplicadas."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # TODO HU8 Lugar reservado para límites por tipo de jugador
        # self.check_position_limits(cards_data)

        team = serializer.save()

        user.team = team
        user.save()

        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    # DELETE → eliminar el equipo del usuario
    def delete(self, request, *args, **kwargs):
        user = self.get_user()
        if not user:
            return Response(
                {"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        if not user.team:
            return Response(
                {"error": "Este usuario no tiene equipo para eliminar"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Guardamos el equipo antes de romper la relación
        team = user.team
        user.team = None
        user.save()

        # Eliminamos el equipo (y opcionalmente sus cartas, si lo deseas)
        team.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
