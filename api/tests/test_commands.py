import io
from contextlib import redirect_stdout
from django.core.management import call_command
from django.test import TestCase
from api.models import *



class CommandsTests(TestCase):
    def test_load_users_command(self):
        # Nos aseguramos que no hay usuarios
        self.assertEqual(User.objects.count(), 0)

        # Ejecutamos el comando pero no mostramos la salida
        f = io.StringIO()
        with redirect_stdout(f):
            call_command("load_users")

        # Comprueba que se han creado los 30 usuarios
        self.assertEqual(User.objects.count(), 30)

        # Comprueba que ninguno tiene equipo
        self.assertTrue(all(user.team is None for user in User.objects.all()))
        print(
            "✅ test_load_users_command: PASS - Comando load_users ejecutado correctamente"
        )


class CardCommandsTests(TestCase):
    def test_load_cards_command_creates_cards(self):
        # Ejecutamos el comando pero no mostramos la salida
        f = io.StringIO()
        with redirect_stdout(f):
            call_command("load_cards")

        # Verificar que se crearon las cartas
        self.assertEqual(Card.objects.count(), 600)
        print(
            "✅ test_load_cards_command_creates_cards: PASS - Comando load_cards creó 600 cartas correctamente"
        )
