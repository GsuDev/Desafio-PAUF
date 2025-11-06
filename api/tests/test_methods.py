from django.test import TestCase
from api.models import *


class CardCalculateOverallRatingTestCase(TestCase):
    # Test para los casos de la función Card.calculate_overall_rating()

    def test_calculate_overall_rating_portero(self):
        card = Card.objects.create(
            name="Thibaut Courtois",
            country="Bélgica",
            club="Real Madrid",
            league="La Liga",
            position="POR",
            diving=90,
            handling=92,
            reflexes=91,
            positioning=92,
            kicking=78,
            speed=46,
        )

        # Resultado de la función con la carta de arriba
        result = card.calculate_overall_rating()

        # Para POR se priorizan: Diving (Atajadas/Estiradas) y Reflexes (Reflejos)
        expected_ovr = 90
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_lateral_derecho(self):
        card = Card.objects.create(
            name="Achraf Hakimi",
            country="Marruecos",
            club="Paris Saint-Germain",
            league="Ligue 1",
            position="LD",
            pace=94,
            shooting=75,
            passing=80,
            dribbling=84,
            defending=80,
            physical=81,
        )

        # Resultado de la función con la carta de arriba
        result = card.calculate_overall_rating()

        # Para LD se priorizan: Pace (Ritmo) y Defending (Defensa)
        expected_ovr = 85
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_defensa_central(self):
        card = Card.objects.create(
            name="Virgil van Dijk",
            country="Países Bajos",
            club="Liverpool",
            league="Premier League",
            position="DFC",
            pace=75,
            shooting=60,
            passing=74,
            dribbling=72,
            defending=92,
            physical=88,
        )

        # Resultado de la función con la carta de arriba
        result = card.calculate_overall_rating()

        # Para DFC se priorizan: Defending (Defensa) y Physical (Físico)
        expected_ovr = 89
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_lateral_izquierdo(self):
        card = Card.objects.create(
            name="Theo Hernández",
            country="Francia",
            club="AC Milan",
            league="Serie A",
            position="LI",
            pace=95,
            shooting=72,
            passing=77,
            dribbling=82,
            defending=80,
            physical=86,
        )

        # Resultado de la función con la carta de arriba
        result = card.calculate_overall_rating()

        # Para LI se priorizan: Pace (Ritmo) y Defending (Defensa)
        expected_ovr = 84
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_medio_centro_defensivo(self):
        card = Card.objects.create(
            name="Rodri",
            country="España",
            club="Manchester City",
            league="Premier League",
            position="MCD",
            pace=68,
            shooting=77,
            passing=86,
            dribbling=82,
            defending=87,
            physical=85,
        )

        # Resultado de la función con la carta de arriba
        result = card.calculate_overall_rating()

        # Para MCD se priorizan: Defending (Defensa) y Physical (Físico)
        expected_ovr = 89
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_medio_centro(self):
        card = Card.objects.create(
            name="Kevin De Bruyne",
            country="Bélgica",
            club="Manchester City",
            league="Premier League",
            position="MC",
            pace=76,
            shooting=88,
            passing=95,
            dribbling=89,
            defending=66,
            physical=80,
        )

        # Resultado de la función con la carta de arriba
        result = card.calculate_overall_rating()

        # Para MC se priorizan: Passing (Pase) y Dribbling (Regate)
        expected_ovr = 91
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_medio_centro_ofensivo(self):
        card = Card.objects.create(
            name="Bruno Fernandes",
            country="Portugal",
            club="Manchester United",
            league="Premier League",
            position="MCO",
            pace=76,
            shooting=85,
            passing=91,
            dribbling=85,
            defending=72,
            physical=80,
        )

        # Resultado de la función con la carta de arriba
        result = card.calculate_overall_rating()

        # Para MCO se priorizan: Pace (Ritmo) y Dribbling (Regate)
        expected_ovr = 88
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_medio_izquierdo(self):
        card = Card.objects.create(
            name="Rafa Leão",
            country="Portugal",
            club="AC Milan",
            league="Serie A",
            position="MI",
            pace=92,
            shooting=84,
            passing=80,
            dribbling=90,
            defending=32,
            physical=79,
        )

        # Resultado de la función con la carta de arriba
        result = card.calculate_overall_rating()

        # Para MI se priorizan: Shooting (Tiro) y Dribbling (Regate)
        expected_ovr = 86
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_medio_derecho(self):
        card = Card.objects.create(
            name="Bukayo Saka",
            country="Inglaterra",
            club="Arsenal",
            league="Premier League",
            position="MD",
            pace=86,
            shooting=84,
            passing=84,
            dribbling=88,
            defending=65,
            physical=72,
        )

        # Resultado de la función con la carta de arriba
        result = card.calculate_overall_rating()

        # Para MD se priorizan: Shooting (Tiro) y Dribbling (Regate)
        expected_ovr = 86
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_segundo_delantero(self):
        card = Card.objects.create(
            name="Christopher Nkunku",
            country="Francia",
            club="Chelsea",
            league="Premier League",
            position="SD",
            pace=89,
            shooting=84,
            passing=85,
            dribbling=91,
            defending=50,
            physical=70,
        )

        # Resultado de la función con la carta de arriba
        result = card.calculate_overall_rating()

        # Para SD se priorizan: Dribbling (Regate) y Shooting (Tiro)
        expected_ovr = 86
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_extremo_izquierdo(self):
        card = Card.objects.create(
            name="Vinícius Jr.",
            country="Brasil",
            club="Real Madrid",
            league="La Liga",
            position="EI",
            pace=97,
            shooting=83,
            passing=81,
            dribbling=94,
            defending=33,
            physical=69,
        )

        # Resultado de la función con la carta de arriba
        result = card.calculate_overall_rating()

        # Para EI se priorizan: Pace (Ritmo) y Dribbling (Regate)
        expected_ovr = 89
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_extremo_derecho(self):
        card = Card.objects.create(
            name="Mohamed Salah",
            country="Egipto",
            club="Liverpool",
            league="Premier League",
            position="ED",
            pace=91,
            shooting=88,
            passing=88,
            dribbling=92,
            defending=45,
            physical=78,
        )

        # Resultado de la función con la carta de arriba
        result = card.calculate_overall_rating()

        # Para ED se priorizan: Pace (Ritmo) y Dribbling (Regate)
        expected_ovr = 91
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_delantero_centro(self):
        card = Card.objects.create(
            name="Kylian Mbappé",
            country="Francia",
            club="Paris Saint-Germain",
            league="Ligue 1",
            position="DC",
            pace=98,
            shooting=94,
            passing=86,
            dribbling=95,
            defending=37,
            physical=81,
        )

        # Resultado de la función con la carta de arriba
        result = card.calculate_overall_rating()

        # Para DC se priorizan: Shooting (Tiro) y Dribbling (Regate)
        expected_ovr = 91
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
            physical=99
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
            physical=1
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
            physical=78
        )
        
        # Resultado de la función
        result = card.calculate_overall_rating()
        
        # El resultado debe ser un número entero
        self.assertIsInstance(result, int)