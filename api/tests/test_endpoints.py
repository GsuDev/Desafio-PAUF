from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import *
from api.serializers import *


class UserEndpointsTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(name="Messi", email="messi@example.com")
        self.user2 = User.objects.create(name="Cristiano", email="cr7@example.com")

    def test_create_user(self):
        url = reverse('user-list-create')  
        data = {
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "testpassword"
        }

        response = self.client.post(url, data, format='json')

        # 1️ Comprobamos que devuelve 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 2️ Comprobamos que el usuario se creó en la BD
        user = User.objects.get(email="testuser@example.com")
        self.assertEqual(user.name, "Test User")

        # 3️ Comprobamos que no tiene equipo asignado
        self.assertIsNone(user.team)

        # 4️ Comprobamos que la respuesta JSON no tenga team
        self.assertIsNone(response.data.get('team'))
    
    def test_list_users(self):
        url = reverse('user-list-create')
        response = self.client.get(url,format='json')

        # 1️ Comprobamos que devuelve un 200 OK
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # 2️ Comprobamos que se listan todos los usuarios
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)    #Pasamos a dict todos los usuarios de la BD
        self.assertEqual(response.data,serializer.data)  #Comprobamos los usuarios del setUp


    def test_retrieve_users(self):
        url = reverse('user-retrieve-update-destroy',args=[self.user1.id])
        response = self.client.get(url,format='json')
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)

        # 1️ Comprobamos que devuelve un 200 OK
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # 2️ Comprobamos que devuelve el usuario pedido
        self.assertEqual(response.data,serializer.data[0])

    def test_update_users(self):
        url = reverse('user-retrieve-update-destroy',args=[self.user1.id])
        data = {
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "testpassword"
        }
        response = self.client.put(url,data,format='json')
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)

        # 1️ Comprobamos que devuelve un 200 OK
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # 2️ Comprobamos que devuelve el usuario pedido
        self.assertEqual(response.data,serializer.data[0])
        #self.assertEqual(response.data,data)       #No va porque el PUT no devuelve la ID, pero es normal


    def test_destroy_users(self):
        url = reverse('user-retrieve-update-destroy',args=[self.user1.id])
        response = self.client.delete(url,format='json')

        # 1️ Comprobamos que devuelve un 204 NO CONTENT
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

        # 2️ Comprobamos que devuelve el usuario pedido
        self.assertFalse(User.objects.filter(id=self.user1.id).exists())

class CardEndpointsTestCase(APITestCase):
    def setUp(self):
        # Creamos 2 cartas de prueba
        self.card1 = Card.objects.create(
            name="Lionel Messi",
            country="Argentina",
            club="Inter Miami",
            league="MLS",
            position="ED",
            pace=85,
            shooting=92,
            passing=91,
            dribbling=95,
            defending=38,
            physical=65,
        )

        self.card2 = Card.objects.create(
            name="Cristiano Ronaldo",
            country="Portugal",
            club="Al Nassr",
            league="Saudi Pro League",
            position="DC",
            pace=84,
            shooting=93,
            passing=82,
            dribbling=88,
            defending=35,
            physical=77,
        )

    def test_list_cards(self):
        url = reverse('card-list-create')
        response = self.client.get(url,format='json')

        # 1️ Comprobamos que devuelve un 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 2️ Comprobamos que se listan todos los cartas
        cards = Card.objects.all()
        serializer = CardSerializer(cards,many=True)    #Pasamos a dict todos los cartas de la BD
        self.assertEqual(response.data,serializer.data)  #Comprobamos los cartas del setUp

    def test_create_card(self):
        data = {
            "name": "Kylian Mbappé",
            "country": "Francia",
            "club": "PSG",
            "league": "Ligue 1",
            "position": "DC",
            "pace": 97,
            "shooting": 89,
            "passing": 80,
            "dribbling": 92,
            "defending": 36,
            "physical": 78,
        }
        url = reverse('card-list-create')
        response = self.client.post(url, data, format='json')

        # 1️ Comprobamos que devuelve 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 2️ Comprobamos que el carta se creó en la BD
        self.assertEqual(Card.objects.count(), 3)

    def test_retrieve_card(self):
        url = reverse('card-retrieve-update-destroy', args=[self.card1.id])
        response = self.client.get(url)

        # 1️ Comprobamos que devuelve un 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 2️ Comprobamos que devuelve la carta correcta
        self.assertEqual(response.data['name'], "Lionel Messi")

    def test_update_card(self):
        data = {
            "name": "Leo Messi",
            "country": "Argentina",
            "club": "Inter Miami",
            "league": "MLS",
            "position": "ED",
            "pace": 86,
            "shooting": 93,
            "passing": 92,
            "dribbling": 96,
            "defending": 38,
            "physical": 66,
        }
        url = reverse('card-retrieve-update-destroy', args=[self.card1.id])
        response = self.client.put(url, data, format='json')
        cards = Card.objects.all()
        serializer = CardSerializer(cards,many=True)

        # 1️ Comprobamos que devuelve un 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 2️ Comprobamos que la carta se actualizó en la BD
        self.assertEqual(response.data,serializer.data[0])

    
    def test_destroy_card(self):
        url = reverse('card-retrieve-update-destroy', args=[self.card1.id])
        response = self.client.delete(url)

        # 1️ Comprobamos que devuelve un 204 NO CONTENT
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # 2️ Comprobamos que la carta se eliminó de la BD
        self.assertFalse(Card.objects.filter(id=self.card1.id).exists())
        

