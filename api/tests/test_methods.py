from django.test import TestCase
from api.models import *


class CardCalculateOverallRatingTestCase(TestCase):
    # Test para los casos de la función Card.calculate_overall_rating()

    def test_calculate_overall_rating_por(self):
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

        result = card.calculate_overall_rating()
        # Cálculo real: 0.25*85 + 0.25*86 + 0.20*87 + 0.15*90 + 0.10*91 + 0.05*61
        # = 21.25 + 21.5 + 17.4 + 13.5 + 9.1 + 3.05 = 85.8 ≈ 86
        expected_ovr = 86
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_ld(self):
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

        result = card.calculate_overall_rating()
        # Cálculo real: 0.25*86 + 0.20*78 + 0.18*69 + 0.15*83 + 0.12*76 + 0.10*70
        # = 21.5 + 15.6 + 12.42 + 12.45 + 9.12 + 7.0 = 78.09 ≈ 78
        expected_ovr = 78
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_dfc(self):
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

        result = card.calculate_overall_rating()
        # Cálculo real: 0.35*86 + 0.25*80 + 0.15*76 + 0.10*56 + 0.08*57 + 0.07*49
        # = 30.1 + 20.0 + 11.4 + 5.6 + 4.56 + 3.43 = 75.09 ≈ 75
        expected_ovr = 75
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_li(self):
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

        result = card.calculate_overall_rating()
        # Cálculo real: 0.25*92 + 0.20*80 + 0.18*75 + 0.15*82 + 0.12*75 + 0.10*69
        # = 23.0 + 16.0 + 13.5 + 12.3 + 9.0 + 6.9 = 80.7 ≈ 81
        expected_ovr = 81
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_mcd(self):
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

        result = card.calculate_overall_rating()
        # Cálculo real: 0.25*82 + 0.20*88 + 0.18*77 + 0.15*75 + 0.12*67 + 0.10*70
        # = 20.5 + 17.6 + 13.86 + 11.25 + 8.04 + 7.0 = 78.25 ≈ 78
        expected_ovr = 78
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_mco(self):
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

        result = card.calculate_overall_rating()
        # Cálculo real: 0.25*88 + 0.22*81 + 0.20*73 + 0.15*72 + 0.10*62 + 0.08*32
        # = 22.0 + 17.82 + 14.6 + 10.8 + 6.2 + 2.56 = 73.98 ≈ 74
        expected_ovr = 74
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_mi(self):
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

        result = card.calculate_overall_rating()
        # Cálculo real: 0.25*81 + 0.22*86 + 0.20*83 + 0.15*76 + 0.10*58 + 0.08*38
        # = 20.25 + 18.92 + 16.6 + 11.4 + 5.8 + 3.04 = 76.01 ≈ 76
        expected_ovr = 76
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_mco(self):
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

        result = card.calculate_overall_rating()
        # Cálculo real: 0.25*82 + 0.22*81 + 0.20*77 + 0.15*74 + 0.10*70 + 0.08*58
        # = 20.5 + 17.82 + 15.4 + 11.1 + 7.0 + 4.64 = 76.46 ≈ 76
        expected_ovr = 76
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_sd(self):
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

        result = card.calculate_overall_rating()
        # Cálculo real: 0.25*85 + 0.22*78 + 0.20*87 + 0.15*53 + 0.10*59 + 0.08*18
        # = 21.25 + 17.16 + 17.4 + 7.95 + 5.9 + 1.44 = 71.1 ≈ 71
        expected_ovr = 71
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_ei(self):
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

        result = card.calculate_overall_rating()
        # Cálculo real: 0.30*90 + 0.25*85 + 0.18*78 + 0.15*73 + 0.12*75
        # = 27.0 + 21.25 + 14.04 + 10.95 + 9.0 = 82.24 ≈ 82
        expected_ovr = 82
        self.assertEqual(result, expected_ovr)

    def test_calculate_overall_rating_dc(self):
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

        result = card.calculate_overall_rating()
        # Cálculo real: 0.30*83 + 0.20*69 + 0.18*83 + 0.15*70 + 0.12*75 + 0.05*31
        # = 24.9 + 13.8 + 14.94 + 10.5 + 9.0 + 1.55 = 74.69 ≈ 75
        expected_ovr = 75
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
        
        result = card.calculate_overall_rating()
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
        
        result = card.calculate_overall_rating()
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
        
        result = card.calculate_overall_rating()
        self.assertIsInstance(result, int)