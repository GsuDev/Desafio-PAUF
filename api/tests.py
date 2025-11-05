from django.test import TestCase
from .models import *

# -------------------
# Test de los modelos
# -------------------

# Tests de Card
class CardModelTestCase(TestCase):

    def setUp(self):
        # Carta de ejemplo para el resto de tests
        self.card = Card.objects.create(
            name="Cristiano Ronaldo",
            country="Portugal",
            club="Al Nassr",
            league="Saudi Pro League",
            position="ST",
            pace=90,
            shooting=93,
            passing=82,
            dribbling=88,
            defending=35,
            physical=85,
        )

    def test_create_card(self):
        # Se comprueba que la carta de ejemplo se ha creado bien
        self.assertEqual(Card.objects.count(), 1)
        self.assertEqual(self.card.name, "Cristiano Ronaldo")
        self.assertTrue(self.card.active)
        self.assertIsNotNone(self.card.created_at)

    def test_card_string_representation(self):
        # Pruebo el toString
        self.assertEqual(str(self.card), "Cristiano Ronaldo (ST)")

    def test_card_can_be_deactivated(self):
        # Compruebo que funciona el borrado lógico
        self.card.active = False
        self.card.save()
        self.assertFalse(self.card.active)


# Tests de Team
class TeamModelTestCase(TestCase):
    def test_create_empty_team(self):
        team = Team.objects.create(name="Dream FC")

        # 1️⃣ El equipo se ha guardado
        self.assertEqual(Team.objects.count(), 1)

        # 2️⃣ El nombre del equipo es correcto
        self.assertEqual(team.name, "Dream FC")

        # 3️⃣ El equipo no tiene cartas
        self.assertEqual(team.cards.count(), 0)

        # 4️⃣ created_at se ha rellenado
        self.assertIsNotNone(team.created_at)

    def test_add_cards_to_team(self):
        # Compruebo que se pueden añadir cartas al equipo
        team = Team.objects.create(name="Legends United")

        # Cartas de ejemplo
        card1 = Card.objects.create(
            name="Messi",
            country="Argentina",
            club="Inter Miami",
            league="MLS",
            position="ST",
            pace=90,
            shooting=93,
            passing=92,
            dribbling=95,
            defending=38,
            physical=65,
        )
        card2 = Card.objects.create(
            name="Ramos",
            country="Spain",
            club="Sevilla FC",
            league="LaLiga",
            position="CB",
            pace=70,
            shooting=60,
            passing=75,
            dribbling=65,
            defending=90,
            physical=85,
        )

        # Añado las cartas al equipo
        team.cards.add(card1, card2)

        # 1️⃣ El equipo tiene 2 cartas
        self.assertEqual(team.cards.count(), 2)

        # 2️⃣ La primera carta es 'Messi'
        self.assertIn(card1, team.cards.all())

        # 3️⃣ La relación funciona en los dos sentidos
        self.assertIn(team, card1.teams.all())


# Tests de User
class UserModelTestCase(TestCase):
    def test_create_retrieve_user(self):
        name = 'villamaravilla'
        email = 'fake@mail.org'
        password = 'fakepass'

        user = User(name=name, email=email, password=password)
        user.save()
        userId = user.id

        # 1️⃣ Comprobar que se creó el usuario
        self.assertEqual(User.objects.count(), 1)

        # 2️⃣ El campo name, email y password son correctos
        self.assertEqual(user.name, name)
        self.assertEqual(user.email, email)
        self.assertEqual(user.password, password)

        # 3️⃣ El campo team debe ser None
        self.assertIsNone(user.team)

        # 4️⃣ El campo created_at se genera automáticamente
        self.assertIsNotNone(user.created_at)
        
        self.assertEqual(user,User.objects.get(pk=userId))
