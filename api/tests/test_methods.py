from django.test import TestCase
from api.models import *


class CardCalculateOverallRatingTestCase(TestCase):
    # Test para los casos de la función Card.calculate_overall_rating()

    def test_calculate_overall_rating_portero(self):
        card = Card.objects.create(
            name="Manuel Peter Neuer",
            country="Germany",
            club="FC Bayern München",
            league="German 1. Bundesliga",
            position="POR",
            pace=61,
            shooting=91,
            passing=48,
            dribbling=16,
            defending=86,
            physical=83,
            diving=85,
            reflexes=86,
            handling=87,
            positioning=90,
            kicking=91,
            speed=61
        )

        # Resultado de la función con la carta de arriba
        result = card.calculate_overall_rating()

        # Para POR se priorizan: Diving (Atajadas/Estiradas) y Reflexes (Reflejos)
        expected_ovr = 85  # (85 + 86) / 2 = 85.5 ≈ 85
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_lateral_derecho(self):
        card = Card.objects.create(
            name="Daniel Alves da Silva",
            country="Brazil",
            club="FC Barcelona",
            league="Spain Primera Division",
            position="LD",
            pace=86,
            shooting=70,
            passing=76,
            dribbling=83,
            defending=78,
            physical=69,
            diving=5,
            reflexes=7,
            handling=11,
            positioning=6,
            kicking=9,
            speed=88
        )

        # Resultado de la función con la carta de arriba
        result = card.calculate_overall_rating()

        # Para LD se priorizan: Pace (Ritmo) y Defending (Defensa)
        expected_ovr = 82  # (86 + 78) / 2 = 82
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_defensa_central(self):
        card = Card.objects.create(
            name="João Miranda de Souza Filho",
            country="Brazil",
            club="Inter",
            league="Italian Serie A",
            position="DFC",
            pace=76,
            shooting=49,
            passing=56,
            dribbling=57,
            defending=86,
            physical=80,
            diving=12,
            reflexes=12,
            handling=6,
            positioning=13,
            kicking=10,
            speed=77
        )

        # Resultado de la función con la carta de arriba
        result = card.calculate_overall_rating()

        # Para DFC se priorizan: Defending (Defensa) y Physical (Físico)
        expected_ovr = 83  # (86 + 80) / 2 = 83
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_lateral_izquierdo(self):
        card = Card.objects.create(
            name="Jordi Alba Ramos",
            country="Spain",
            club="FC Barcelona",
            league="Spain Primera Division",
            position="LI",
            pace=92,
            shooting=69,
            passing=75,
            dribbling=82,
            defending=80,
            physical=75,
            diving=13,
            reflexes=13,
            handling=15,
            positioning=6,
            kicking=13,
            speed=92
        )

        # Resultado de la función con la carta de arriba
        result = card.calculate_overall_rating()

        # Para LI se priorizan: Pace (Ritmo) y Defending (Defensa)
        expected_ovr = 86  # (92 + 80) / 2 = 86
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_medio_centro_defensivo(self):
        card = Card.objects.create(
            name="Nemanja Matić",
            country="Serbia",
            club="Chelsea",
            league="English Premier League",
            position="MCD",
            pace=67,
            shooting=70,
            passing=77,
            dribbling=75,
            defending=82,
            physical=88,
            diving=7,
            reflexes=9,
            handling=15,
            positioning=14,
            kicking=12,
            speed=68
        )

        # Resultado de la función con la carta de arriba
        result = card.calculate_overall_rating()

        # Para MCD se priorizan: Defending (Defensa) y Physical (Físico)
        expected_ovr = 85  # (82 + 88) / 2 = 85
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_medio_centro_ofensivo_gotze(self):
        card = Card.objects.create(
            name="Mario Götze",
            country="Germany",
            club="FC Bayern München",
            league="German 1. Bundesliga",
            position="MCO",
            pace=72,
            shooting=73,
            passing=81,
            dribbling=88,
            defending=32,
            physical=62,
            diving=14,
            reflexes=10,
            handling=7,
            positioning=6,
            kicking=12,
            speed=68
        )

        # Resultado de la función con la carta de arriba
        result = card.calculate_overall_rating()

        # Para MCO se priorizan: Pace (Ritmo) y Dribbling (Regate)
        expected_ovr = 80  # (72 + 88) / 2 = 80
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_medio_izquierdo(self):
        card = Card.objects.create(
            name="Samir Nasri",
            country="France",
            club="Manchester City",
            league="English Premier League",
            position="MI",
            pace=81,
            shooting=76,
            passing=83,
            dribbling=86,
            defending=38,
            physical=58,
            diving=1,
            reflexes=1,
            handling=1,
            positioning=1,
            kicking=1,
            speed=79
        )

        # Resultado de la función con la carta de arriba
        result = card.calculate_overall_rating()

        # Para MI se priorizan: Shooting (Tiro) y Dribbling (Regate)
        expected_ovr = 81  # (76 + 86) / 2 = 81
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_medio_centro_ofensivo_hamsik(self):
        card = Card.objects.create(
            name="Marek Hamšík",
            country="Slovakia",
            club="Napoli",
            league="Italian Serie A",
            position="MCO",
            pace=74,
            shooting=77,
            passing=81,
            dribbling=82,
            defending=58,
            physical=70,
            diving=8,
            reflexes=14,
            handling=6,
            positioning=14,
            kicking=4,
            speed=73
        )

        # Resultado de la función con la carta de arriba
        result = card.calculate_overall_rating()

        # Para MCO se priorizan: Pace (Ritmo) y Dribbling (Regate)
        expected_ovr = 78  # (74 + 82) / 2 = 78
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_segundo_delantero(self):
        card = Card.objects.create(
            name="Antonio Cassano",
            country="Italy",
            club="U.C. Sampdoria",
            league="Italian Serie A",
            position="SD",
            pace=53,
            shooting=78,
            passing=87,
            dribbling=85,
            defending=18,
            physical=59,
            diving=4,
            reflexes=8,
            handling=10,
            positioning=13,
            kicking=6,
            speed=52
        )

        # Resultado de la función con la carta de arriba
        result = card.calculate_overall_rating()

        # Para SD se priorizan: Dribbling (Regate) y Shooting (Tiro)
        expected_ovr = 81  # (85 + 78) / 2 = 81.5 ≈ 81
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_extremo_izquierdo(self):
        card = Card.objects.create(
            name="Memphis Depay",
            country="Netherlands",
            club="Manchester United",
            league="English Premier League",
            position="EI",
            pace=90,
            shooting=78,
            passing=73,
            dribbling=85,
            defending=29,
            physical=75,
            diving=8,
            reflexes=10,
            handling=14,
            positioning=12,
            kicking=6,
            speed=90
        )

        # Resultado de la función con la carta de arriba
        result = card.calculate_overall_rating()

        # Para EI se priorizan: Pace (Ritmo) y Dribbling (Regate)
        expected_ovr = 87  # (90 + 85) / 2 = 87.5 ≈ 87
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_delantero_centro(self):
        card = Card.objects.create(
            name="Robbie Keane",
            country="Republic of Ireland",
            club="LA Galaxy",
            league="USA Major League Soccer",
            position="DC",
            pace=70,
            shooting=83,
            passing=75,
            dribbling=83,
            defending=31,
            physical=69,
            diving=11,
            reflexes=16,
            handling=9,
            positioning=14,
            kicking=13,
            speed=68
        )

        # Resultado de la función con la carta de arriba
        result = card.calculate_overall_rating()

        # Para DC se priorizan: Shooting (Tiro) y Dribbling (Regate)
        expected_ovr = 83  # (83 + 83) / 2 = 83
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_maximum_stats(self):
        card = Card.objects.create(
            name="Jugador Máximo",
            country="Test",
            club="Test Club",
            league="Test League",
            position="DC",
            pace=99,
            shooting=99,
            passing=99,
            dribbling=99,
            defending=99,
            physical=99,
            diving=99,
            reflexes=99,
            handling=99,
            positioning=99,
            kicking=99,
            speed=99
        )
        
        # Resultado de la función con stats máximas
        result = card.calculate_overall_rating()
        
        # Con todas las stats al máximo debe dar 99
        expected_ovr = 99
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_minimum_stats(self):
        card = Card.objects.create(
            name="Jugador Mínimo",
            country="Test",
            club="Test Club",
            league="Test League",
            position="DC",
            pace=1,
            shooting=1,
            passing=1,
            dribbling=1,
            defending=1,
            physical=1,
            diving=1,
            reflexes=1,
            handling=1,
            positioning=1,
            kicking=1,
            speed=1
        )
        
        # Resultado de la función con stats mínimas
        result = card.calculate_overall_rating()
        
        # Con stats mínimas debe estar entre 1 y 99
        self.assertGreaterEqual(result, 1)
        self.assertLessEqual(result, 99)

    def test_calculate_overall_rating_returns_integer(self):
        card = Card.objects.create(
            name="Test Player",
            country="Test",
            club="Test Club",
            league="Test League",
            position="MC",
            pace=75,
            shooting=80,
            passing=85,
            dribbling=82,
            defending=65,
            physical=78,
            diving=1,
            reflexes=1,
            handling=1,
            positioning=1,
            kicking=1,
            speed=1
        )
        
        # Resultado de la función
        result = card.calculate_overall_rating()
        
        # El resultado debe ser un número entero
        self.assertIsInstance(result, int)