from django.urls import path
from . import views

urlpatterns = [
    # Endpoints
    path('users/', views.UserListCreate.as_view(), name='user-list-create'),
    path('users/<int:pk>/', views.UserRetrieveUpdateDestroy.as_view(), name='user-retrieve-update-destroy'),
    path('cards/', views.CardListCreate.as_view(), name='card-list-create'),
    path('cards/<int:pk>/', views.CardRetrieveUpdateDestroy.as_view(), name='card-retrieve-update-destroy'),
]