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

        # 1️⃣ Comprobamos que devuelve 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 2️⃣ Comprobamos que el usuario se creó en la BD
        user = User.objects.get(email="testuser@example.com")
        self.assertEqual(user.name, "Test User")

        # 3️⃣ Comprobamos que no tiene equipo asignado
        self.assertIsNone(user.team)

        # 4️⃣ Comprobamos que la respuesta JSON no tenga team
        self.assertIsNone(response.data.get('team'))
    
    def test_list_users(self):
        url = reverse('user-list-create')
        response = self.client.get(url,format='json')

        # 1️⃣ Comprobamos que devuelve un 200 OK
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # 2️⃣ Comprobamos que se listan todos los usuarios
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)    #Pasamos a dict todos los usuarios de la BD
        self.assertEqual(response.data,serializer.data)  #Comprobamos los usuarios del setUp


    def test_retrieve_users(self):
        url = reverse('user-retrieve-update-destroy',args=[self.user1.id])
        response = self.client.get(url,format='json')
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)

        # 1️⃣ Comprobamos que devuelve un 200 OK
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # 2️⃣ Comprobamos que devuelve el usuario pedido
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

        # 1️⃣ Comprobamos que devuelve un 200 OK
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # 2️⃣ Comprobamos que devuelve el usuario pedido
        self.assertEqual(response.data,serializer.data[0])
        #self.assertEqual(response.data,data)       #No va porque el PUT no devuelve la ID, pero es normal


    def test_destroy_users(self):
        url = reverse('user-retrieve-update-destroy',args=[self.user1.id])
        response = self.client.delete(url,format='json')

        # 1️⃣ Comprobamos que devuelve un 204 NO CONTENT
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

        # 2️⃣ Comprobamos que devuelve el usuario pedido
        self.assertFalse(User.objects.filter(id=self.user1.id).exists())