from django.db import models

# Modelos del proyecto


class Card(models.Model):
    POSICIONES = [
        ("POR", "Portero"),
        ("LD", "Lateral Derecho"),
        ("DFC", "Defensa Central"),
        ("LI", "Lateral Izquierdo"),
        ("MCD", "Medio Centro Defensivo"),
        ("MC", "Medio Centro"),
        ("MCO", "Medio Centro Ofensivo"),
        ("MI", "Medio Izquierdo"),
        ("MD", "Medio Derecho"),
        ("SD", "Segundo Delantero"),
        ("EI", "Extremo Izquierdo"),
        ("ED", "Extremo Derecho"),
        ("DC", "Delantero Centro"),
    ]

    # Datos básicos
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    club = models.CharField(max_length=100)
    league = models.CharField(max_length=100)
    position = models.CharField(choices=POSICIONES)

    # Estadísticas
    pace = models.IntegerField()
    shooting = models.IntegerField()
    passing = models.IntegerField()
    dribbling = models.IntegerField()
    defending = models.IntegerField()
    physical = models.IntegerField()
    diving = models.IntegerField()
    reflexes = models.IntegerField()
    handling = models.IntegerField()
    positioning = models.IntegerField()
    kicking = models.IntegerField()
    speed = models.IntegerField()

    # Otros campos
    active = models.BooleanField(default=True)
    overall_rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.position})"

    def calculate_overall_rating(self):
        """
        Calcula la media general del jugador en función de su posición
        utilizando fórmulas específicas y realistas basadas en FIFA 16.
        """

        pos = self.position.upper()

        # Portero - usa todos los atributos de portero
        if pos in ["GK", "POR"]:
            return round(
                0.25 * self.diving +
                0.25 * self.reflexes +
                0.20 * self.handling +
                0.15 * self.positioning +
                0.10 * self.kicking +
                0.05 * self.speed
            )

        # Defensa Central - prioriza defending y physical
        elif pos in ["CB", "DFC"]:
            return round(
                0.35 * self.defending +
                0.25 * self.physical +
                0.15 * self.pace +
                0.10 * self.passing +
                0.08 * self.dribbling +
                0.07 * self.shooting
            )

        # Lateral Derecho / Izquierdo - balance entre ataque y defensa
        elif pos in ["RB", "LB", "LD", "LI"]:
            return round(
                0.25 * self.pace +
                0.20 * self.defending +
                0.18 * self.physical +
                0.15 * self.dribbling +
                0.12 * self.passing +
                0.10 * self.shooting
            )

        # Mediocentro Defensivo - defensa y distribución
        elif pos in ["CDM", "MCD"]:
            return round(
                0.25 * self.defending +
                0.20 * self.physical +
                0.18 * self.passing +
                0.15 * self.dribbling +
                0.12 * self.pace +
                0.10 * self.shooting
            )

        # Mediocentro - juego completo
        elif pos in ["CM", "MC"]:
            return round(
                0.22 * self.passing +
                0.20 * self.dribbling +
                0.18 * self.defending +
                0.15 * self.physical +
                0.13 * self.shooting +
                0.12 * self.pace
            )

        # Medio Derecho / Izquierdo - velocidad y técnica
        elif pos in ["RM", "LM", "MD", "MI"]:
            return round(
                0.25 * self.pace +
                0.22 * self.dribbling +
                0.20 * self.passing +
                0.15 * self.shooting +
                0.10 * self.physical +
                0.08 * self.defending
            )

        # Mediocentro Ofensivo - creación de juego
        elif pos in ["CAM", "MCO"]:
            return round(
                0.25 * self.dribbling +
                0.22 * self.passing +
                0.20 * self.shooting +
                0.15 * self.pace +
                0.10 * self.physical +
                0.08 * self.defending
            )

        # Extremo Derecho / Izquierdo - velocidad y regate
        elif pos in ["RW", "LW", "ED", "EI"]:
            return round(
                0.30 * self.pace +
                0.25 * self.dribbling +
                0.18 * self.shooting +
                0.15 * self.passing +
                0.12 * self.physical
            )

        # Segundo Delantero - técnica y definición
        elif pos in ["CF", "SD"]:
            return round(
                0.25 * self.dribbling +
                0.22 * self.shooting +
                0.20 * self.passing +
                0.15 * self.pace +
                0.10 * self.physical +
                0.08 * self.defending
            )

        # Delantero Centro - definición y físico
        elif pos in ["ST", "DC"]:
            return round(
                0.30 * self.shooting +
                0.20 * self.physical +
                0.18 * self.dribbling +
                0.15 * self.pace +
                0.12 * self.passing +
                0.05 * self.defending
            )

        # Por defecto: promedio de stats básicas
        stats = [
            self.pace,
            self.shooting,
            self.passing,
            self.dribbling,
            self.defending,
            self.physical,
        ]
        return round(sum(stats) / len(stats))

    def save(self, *args, **kwargs):
        self.overall_rating = self.calculate_overall_rating()
        super().save(*args, **kwargs)


class Team(models.Model):
    name = models.CharField(max_length=100)
    cards = models.ManyToManyField(Card, blank=True, related_name="teams")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    team = models.OneToOneField(Team, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
