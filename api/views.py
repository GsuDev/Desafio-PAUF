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

        # Verificar que el equipo no tenga más de 25 cartas ni menos de 23
        cards_data = serializer.validated_data.get("cards", [])
        if len(cards_data) != 0 and len(cards_data) not in range(23, 26):
            return Response(
                {"error": "Un equipo no puede tener más de 25 cartas."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif len(cards_data) != 0:
            # LIMITES DE JUGADORES POR POSICION
            position_limits = self.check_position_limits(cards_data)
            if position_limits["success"] == False:
                return Response(
                    {"error": position_limits["message"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Evitar duplicados en las cartas
        card_ids = [c.id for c in cards_data]
        if len(card_ids) != len(set(card_ids)):
            return Response(
                {"error": "El equipo contiene cartas duplicadas."},
                status=status.HTTP_400_BAD_REQUEST,
            )

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
        if len(cards_data) not in range(23, 26):
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

        # LIMITES DE JUGADORES POR POSICION
        position_limits = self.check_position_limits(cards_data)
        if position_limits["success"] == False:
            return Response(
                {"error": position_limits["message"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

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

    # Método preparado para implementar límites por tipo de jugador
    def check_position_limits(self, cards):
        """
        Aquí se podrá controlar que haya un máximo de jugadores por posición:
        - Entre 2 y 3 porteros
        - Entre 8 y 10 defensas
        - Entre 6 y 9 centrocampistas
        - Entre 5 y 6 delanteros
        """

        gk = 0
        df = 0
        mc = 0
        st = 0
        success = True
        message = ""

        for card in cards:
            pos = card.position

            if pos == "POR":
                gk += 1
            elif pos in ["DFC", "LI", "LD"]:
                df += 1
            elif pos in ["MC", "MCD", "MCO", "MI", "MD"]:
                mc += 1
            elif pos in ["EI", "ED", "DC", "SD"]:
                st += 1

        if gk not in range(2, 4):
            success = False
            message = "Tiene que tener entre 2 y 3 porteros"

        if df not in range(8, 11):
            success = False
            message = "Tiene que tener entre 8 y 10 defensas"

        if mc not in range(6, 10):
            success = False
            message = "Tiene que tener entre 6 y 9 centrocampistas"

        if st not in range(5, 7):
            success = False
            message = "Tiene que tener entre 5 y 6 delantero"

        return {"success": success, "message": message}


class UserTeamMeanView(generics.GenericAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def get_user(self):
        user_id = self.kwargs.get("pk")
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

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
        team = user.team
        # Extraigo las OVR a una lista
        cards_ovr_list = list((c.overall_rating for c in team.cards.all()))

        cards_number = len(cards_ovr_list)

        # En mi codigo es imposible que exista un equipo con <2 "POR" ni con <20 cartas
        # Pero te lo implemento igual porque lo se hacer
        gk_number = team.cards.filter(position="POR").count()

        if cards_number < 20 or gk_number < 2:
            return Response(
                {"error": "Este usuario no tiene un equipo completo"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Hago la media
        team_avg = sum(cards_ovr_list) / cards_number

        # Ajusto por si sale de los limites por la formula de calculo AVR (a veces se pasa de 100)
        if team_avg < 0:
            team_avg = 0
        elif team_avg > 100:
            team_avg = 100

        stars = 0.0
        team_avg_int = int(team_avg)
        if team_avg_int in range(0, 10):
            stars = 0.5
        elif team_avg_int in range(10, 20):
            stars = 1
        elif team_avg_int in range(20, 30):
            stars = 1.5
        elif team_avg_int in range(30, 40):
            stars = 2
        elif team_avg_int in range(40, 50):
            stars = 2.5
        elif team_avg_int in range(50, 60):
            stars = 3
        elif team_avg_int in range(60, 70):
            stars = 3.5
        elif team_avg_int in range(70, 80):
            stars = 4
        elif team_avg_int in range(80, 90):
            stars = 4.5
        elif team_avg_int in range(90, 100):
            stars = 5

        return Response(
            {
                "team_avg": team_avg, 
                "cards_number": cards_number, 
                "stars": stars
            },
            status=status.HTTP_200_OK,
        )
