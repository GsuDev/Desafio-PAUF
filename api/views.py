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
    lookup_field = 'pk'

# Views para listar todas las tarjetas y crear una nueva
class CardListCreate(generics.ListCreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


# Views para obtener, actualizar o eliminar una tarjeta específica
class CardRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    lookup_field = 'pk'

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


# Views para listar todos los usuarios y crear uno nuevo
class TeamListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Views para obtener, actualizar o eliminar un usuario específico
class TeamRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"


# Crear equipo para un usuario concreto
class UserTeamCreate(generics.CreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer  # Se sigue usando para crear el Team

    def create(self, request, *args, **kwargs):
        user_id = self.kwargs.get("pk")

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        # Comprobamos que no tenga ya un equipo (relación OneToOne)
        if user.team:
            return Response(
                {"error": "Este usuario ya tiene un equipo asignado"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Crear el equipo con los datos enviados
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        team = serializer.save()

        # Asignarlo al usuario
        user.team = team
        user.save()

        # 💡 Serializamos el usuario completo (incluyendo su equipo)
        user_serializer = UserSerializer(user)

        return Response(user_serializer.data, status=status.HTTP_201_CREATED)
