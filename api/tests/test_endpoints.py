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
        url = reverse("user-list-create")
        data = {
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "testpassword",
        }

        response = self.client.post(url, data, format="json")

        # 1️⃣ Comprobamos que devuelve 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 2️⃣ Comprobamos que el usuario se creó en la BD
        user = User.objects.get(email="testuser@example.com")
        self.assertEqual(user.name, "Test User")

        # 3️⃣ Comprobamos que no tiene equipo asignado
        self.assertIsNone(user.team)

        # 4️⃣ Comprobamos que la respuesta JSON no tenga team
        self.assertIsNone(response.data.get("team"))

    def test_list_users(self):
        url = reverse("user-list-create")
        response = self.client.get(url, format="json")

        # 1️⃣ Comprobamos que devuelve un 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 2️⃣ Comprobamos que se listan todos los usuarios
        users = User.objects.all()
        serializer = UserSerializer(
            users, many=True
        )  # Pasamos a dict todos los usuarios de la BD
        self.assertEqual(
            response.data, serializer.data
        )  # Comprobamos los usuarios del setUp

    def test_retrieve_users(self):
        url = reverse("user-retrieve-update-destroy", args=[self.user1.id])
        response = self.client.get(url, format="json")
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        # 1️⃣ Comprobamos que devuelve un 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 2️⃣ Comprobamos que devuelve el usuario pedido
        self.assertEqual(response.data, serializer.data[0])

    def test_update_users(self):
        url = reverse("user-retrieve-update-destroy", args=[self.user1.id])
        data = {
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "testpassword",
        }
        response = self.client.put(url, data, format="json")
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        # 1️⃣ Comprobamos que devuelve un 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 2️⃣ Comprobamos que devuelve el usuario pedido
        self.assertEqual(response.data, serializer.data[0])
        # self.assertEqual(response.data,data)       #No va porque el PUT no devuelve la ID, pero es normal

    def test_destroy_users(self):
        url = reverse("user-retrieve-update-destroy", args=[self.user1.id])
        response = self.client.delete(url, format="json")

        # 1️⃣ Comprobamos que devuelve un 204 NO CONTENT
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # 2️⃣ Comprobamos que devuelve el usuario pedido
        self.assertFalse(User.objects.filter(id=self.user1.id).exists())


class CardEndpointsTestCase(APITestCase):
    def setUp(self):
        # Creamos 2 cartas de prueba
        self.card1 = Card.objects.create(
            name="Neymar da Silva Santos Júnior",
            country="Brazil",
            club="FC Barcelona",
            league="Spain Primera Division",
            position="EI",
            pace=90,
            shooting=80,
            passing=72,
            dribbling=92,
            defending=30,
            physical=57,
            diving=9,
            reflexes=11,
            handling=9,
            positioning=15,
            kicking=15,
            speed=90,
        )

        self.card2 = Card.objects.create(
            name="Neymar da Silva Santos Júnior",
            country="Brazil",
            club="FC Barcelona",
            league="Spain Primera Division",
            position="EI",
            pace=90,
            shooting=80,
            passing=72,
            dribbling=92,
            defending=30,
            physical=57,
            diving=9,
            reflexes=11,
            handling=9,
            positioning=15,
            kicking=15,
            speed=90,
        )

    def test_list_cards(self):
        url = reverse("card-list-create")
        response = self.client.get(url, format="json")

        # 1️⃣ Comprobamos que devuelve un 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 2️⃣ Comprobamos que se listan todos los cartas
        cards = Card.objects.all()
        serializer = CardSerializer(
            cards, many=True
        )  # Pasamos a dict todos los cartas de la BD
        self.assertEqual(
            response.data, serializer.data
        )  # Comprobamos los cartas del setUp

    def test_create_card(self):
        data = {
            "name": "Neymar da Silva Santos Júnior",
            "country": "Brazil",
            "club": "FC Barcelona",
            "league": "Spain Primera Division",
            "position": "EI",
            "pace": 90,
            "shooting": 80,
            "passing": 72,
            "dribbling": 92,
            "defending": 30,
            "physical": 57,
            "diving": 9,
            "reflexes": 11,
            "handling": 9,
            "positioning": 15,
            "kicking": 15,
            "speed": 90,
        }
        url = reverse("card-list-create")
        response = self.client.post(url, data, format="json")

        # 1️⃣ Comprobamos que devuelve 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 2️⃣ Comprobamos que el carta se creó en la BD
        self.assertEqual(Card.objects.count(), 3)

    def test_retrieve_card(self):
        url = reverse("card-retrieve-update-destroy", args=[self.card1.id])
        response = self.client.get(url)

        # 1️⃣ Comprobamos que devuelve un 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 2️⃣ Comprobamos que devuelve la carta correcta
        self.assertEqual(response.data["name"], "Neymar da Silva Santos Júnior")

    def test_update_card(self):
        data = {
            "name": "Neymar da Silva Santos Júnior",
            "country": "Brazil",
            "club": "FC Barcelona",
            "league": "Spain Primera Division",
            "position": "EI",
            "pace": 90,
            "shooting": 80,
            "passing": 72,
            "dribbling": 92,
            "defending": 30,
            "physical": 57,
            "diving": 9,
            "reflexes": 11,
            "handling": 9,
            "positioning": 15,
            "kicking": 15,
            "speed": 90,
        }
        url = reverse("card-retrieve-update-destroy", args=[self.card1.id])
        response = self.client.put(url, data, format="json")
        cards = Card.objects.all()
        serializer = CardSerializer(cards, many=True)

        # 1️⃣ Comprobamos que devuelve un 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 2️⃣ Comprobamos que la carta se actualizó en la BD
        self.assertEqual(response.data, serializer.data[0])

    def test_destroy_card(self):
        url = reverse("card-retrieve-update-destroy", args=[self.card1.id])
        response = self.client.delete(url)

        # 1️⃣ Comprobamos que devuelve un 204 NO CONTENT
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # 2️⃣ Comprobamos que la carta se eliminó (soft delete) de la BD
        self.assertFalse(Card.objects.get(id=self.card1.id).active)
