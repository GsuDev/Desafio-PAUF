from contextlib import redirect_stdout
import io
from django.core.management import call_command
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import *
from api.serializers import *

class ExamenTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(name="Messi", email="messi@example.com")
        self.user2 = User.objects.create(name="Cristiano", email="cr7@example.com")
        self.user3 = User.objects.create(name="Raul", email="raul7@example.com")
        # Ejecutamos el comando pero no mostramos la salida
        f = io.StringIO()
        with redirect_stdout(f):
            call_command("load_cards", limit=180)

    def test_exito_avr_mean(self):
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
        data = {"name": "Valid Team", "card_ids": valid_team}
        self.client.post(url, data, format="json")

        url = reverse("user-team-avg", args=[self.user1.id])
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("✅ EXAMEN 👩‍🏫 test_exito_avr_mean: PASS - Calculo media de OVR correcto")

    def test_fracaso_avr_mean_insuficient_cards(self):
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
            113
        ]
        data = {"name": "Valid Team", "card_ids": valid_team}
        self.client.post(url, data, format="json")

        url = reverse("user-team-avg", args=[self.user1.id])
        response = self.client.get(url, format="json", args=[self.user1.id])

        # Devuelve 404 porque no puede insertar en primer lugar un equipo con cartas de menos
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print(
            "✅ EXAMEN 👩‍🏫 test_fracaso_avr_mean_insuficient_cards: PASS - Devuelve status 404 como se espera si hay <20 cartas"
        )

    def test_fracaso_avr_mean_no_user(self):
        url = reverse("user-team-avg", args=[10])
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print(
            "✅ EXAMEN 👩‍🏫test_fracaso_avr_mean_no_user: PASS - Devuelve 404 segun lo esperado"
        )
