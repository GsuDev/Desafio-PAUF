from contextlib import redirect_stdout
import io
from django.core.management import call_command
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import *
from api.serializers import *


class UserEndpointsTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(name="Messi", email="messi@example.com")
        self.user2 = User.objects.create(name="Cristiano", email="cr7@example.com")
        self.user3 = User.objects.create(name="Raul", email="raul7@example.com")
        # Ejecutamos el comando pero no mostramos la salida
        f = io.StringIO()
        with redirect_stdout(f):
            call_command("load_cards", limit=180)

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
        print("✅ test_create_user: PASS - Usuario creado via endpoint correctamente")

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
        print(
            "✅ test_list_users: PASS - Listado de usuarios funcionando correctamente"
        )

    def test_retrieve_users(self):
        url = reverse("user-retrieve-update-destroy", args=[self.user1.id])
        response = self.client.get(url, format="json")
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        # 1️⃣ Comprobamos que devuelve un 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 2️⃣ Comprobamos que devuelve el usuario pedido
        self.assertEqual(response.data, serializer.data[0])
        print(
            "✅ test_retrieve_users: PASS - Recuperación de usuario específico correcta"
        )

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
        print(
            "✅ test_update_users: PASS - Actualización de usuario funcionando correctamente"
        )

    def test_destroy_users(self):
        url = reverse("user-retrieve-update-destroy", args=[self.user1.id])
        response = self.client.delete(url, format="json")

        # 1️⃣ Comprobamos que devuelve un 204 NO CONTENT
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # 2️⃣ Comprobamos que devuelve el usuario pedido
        self.assertFalse(User.objects.filter(id=self.user1.id).exists())
        print("✅ test_destroy_users: PASS - Eliminación de usuario exitosa")

    def test_create_team_for_user(self):
        url = reverse("user-team-view", args=[self.user1.id])
        data = {"name": "Test Ticles Team"}
        response = self.client.post(url, data, format="json")

        # 1 Comprobamos que devuelve un 204 NO CONTENT
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 2 Comprobamos que le ha asociado el equipo
        self.assertIsNotNone(User.objects.get(id=self.user1.id).team)

        # 3 Comprobamos que devuelve
        self.assertEqual(response.data["team"]["name"], data["name"])

        # 4 Comprobamos que no acepta mas de 25 de cartas
        card_ids = ids = list(Card.objects.values_list("id", flat=True))
        data = {"name": "Test Ticles Team", "cards": card_ids}
        response = self.client.post(url, data, format="json", args=[self.user2.id])

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 5 Comprobamos que no acepta duplicados de cartas
        data = {"name": "Test Ticles Team", "cards": [1, 1, 2, 2, 3]}
        response = self.client.post(url, data, format="json", args=[self.user3.id])

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print(
            "✅ test_create_team_for_user: PASS - Creación de equipo para usuario funcionando correctamente"
        )

    def test_patch_team_for_user(self):
        # Primero le creamos un equipo al user1
        url = reverse("user-team-view", args=[self.user1.id])
        valid_team = [
            42,
            53,
            51,
            15,
            22,
            43,
            64,
            69,
            79,
            89,
            12,
            34,
            97,
            33,
            113,
            10,
            44,
            50,
            65,
            1,
            2,
            11,
            48,
            180,
        ]
        data = {"name": "Initial Team", "card_ids": valid_team}
        self.client.post(url, data, format="json")

        # Ahora hacemos PATCH para actualizar nombre y cartas
        update_data = {
            "name": "Updated Team",
            "card_ids": [
                42,
                53,
                51,
                15,
                22,
                43,
                45,
                64,
                69,
                79,
                89,
                12,
                34,
                97,
                33,
                113,
                10,
                44,
                50,
                65,
                1,
                2,
                11,
                48,
                180,
            ],  # otras cartas
        }
        response = self.client.patch(url, update_data, format="json")

        # 1 Comprobamos el codigo 200 ok
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 2 Comprobamos que ha modificado las cartas
        team = User.objects.get(id=self.user1.id).team
        self.assertEqual(team.name, update_data["name"])
        self.assertSetEqual(
            set(team.cards.values_list("id", flat=True)), set(update_data["card_ids"])
        )  # Set para que no importe el orden

        # 3 Comprobamos límite de 25 cartas
        too_many_cards = {"card_ids": [c.id for c in Card.objects.all()[:26]]}
        response = self.client.patch(url, too_many_cards, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 4 Comprobamos duplicados
        duplicate_cards = {"card_ids": [1, 1, 2, 2, 3]}
        response = self.client.patch(url, duplicate_cards, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print(
            "✅ test_patch_team_for_user: PASS - Actualización parcial de equipo funcionando correctamente"
        )


def test_delete_team_for_user(self):
    # Primero le creamos un equipo al user2
    url = reverse("user-team-view", args=[self.user2.id])
    data = {
        "name": "Team To Delete",
        "card_ids": [c.id for c in Card.objects.all()[:5]],
    }
    self.client.post(url, data, format="json")

    # DELETE
    response = self.client.delete(url)
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Comprobamos que user2 ya no tiene equipo
    self.assertIsNone(User.objects.get(id=self.user2.id).team)

    # Comprobamos que el equipo fue eliminado
    self.assertFalse(Team.objects.filter(name="Team To Delete").exists())

    # DELETE en usuario sin equipo → 400
    url_no_team = reverse("user-team-view", args=[self.user3.id])
    response = self.client.delete(url_no_team)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    print(
        "✅ test_delete_team_for_user: PASS - Eliminación de equipo funcionando correctamente"
    )
    

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
        print("✅ test_list_cards: PASS - Listado de cartas funcionando correctamente")

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
        print("✅ test_create_card: PASS - Creación de carta via endpoint exitosa")

    def test_retrieve_card(self):
        url = reverse("card-retrieve-update-destroy", args=[self.card1.id])
        response = self.client.get(url)

        # 1️⃣ Comprobamos que devuelve un 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 2️⃣ Comprobamos que devuelve la carta correcta
        self.assertEqual(response.data["name"], "Neymar da Silva Santos Júnior")
        print("✅ test_retrieve_card: PASS - Recuperación de carta específica correcta")

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
        print("✅ test_update_card: PASS - Actualización de carta exitosa")

    def test_destroy_card(self):
        url = reverse("card-retrieve-update-destroy", args=[self.card1.id])
        response = self.client.delete(url)

        # 1️⃣ Comprobamos que devuelve un 204 NO CONTENT
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # 2️⃣ Comprobamos que la carta se eliminó (soft delete) de la BD
        self.assertFalse(Card.objects.get(id=self.card1.id).active)
        print(
            "✅ test_destroy_card: PASS - Eliminación lógica de carta funcionando correctamente"
        )
        

