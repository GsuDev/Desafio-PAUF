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