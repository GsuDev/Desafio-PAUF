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

    # Otros campos
    active = models.BooleanField(default=True)
    overall_rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.position})"

    # Función del calculo de OVR
    def calculate_overall_rating(self):
        """
        Calcula la media general del jugador en función de su posición
        utilizando fórmulas específicas y realistas basadas en estadísticas.
        """

        pos = self.position.upper()

        # Portero
        if pos in ["GK", "POR"]:
            return round(
                0.118 * self.diving
                + 0.120 * self.reflexes
                + 0.080 * self.handling
                + 0.070 * self.positioning
                + 0.056 * self.kicking
                + 0.050 * self.speed
            )

        # Defensa Central
        elif pos in ["CB", "DFC"]:
            return round(
                0.48 * self.defending
                + 0.34 * self.physical
                + 0.10 * self.pace
                + 0.05 * self.passing
                + 0.03 * self.dribbling
            )

        # Lateral Derecho / Izquierdo
        elif pos in ["RB", "LB", "LD", "LI"]:
            return round(
                0.30 * self.pace
                + 0.25 * self.defending
                + 0.20 * self.physical
                + 0.15 * self.passing
                + 0.10 * self.dribbling
            )

        # Mediocentro Defensivo
        elif pos in ["CDM", "MCD"]:
            return round(
                0.26 * self.defending
                + 0.22 * self.physical
                + 0.20 * self.passing
                + 0.15 * self.dribbling
                + 0.10 * self.pace
                + 0.07 * self.shooting
            )

        # Mediocentro
        elif pos in ["CM", "MC"]:
            return round(
                0.28 * self.passing
                + 0.24 * self.dribbling
                + 0.18 * self.defending
                + 0.14 * self.physical
                + 0.10 * self.shooting
                + 0.06 * self.pace
            )

        # Medio Derecho / Izquierdo
        elif pos in ["RM", "LM", "MD", "MI"]:
            return round(
                0.52 * self.dribbling
                + 0.27 * self.shooting
                + 0.23 * self.passing
                + 0.12 * self.pace
                + 0.07 * self.physical
                + 0.03 * self.defending
            )

        # Mediocentro Ofensivo
        elif pos in ["CAM", "MCO"]:
            return round(
                0.54 * self.dribbling
                + 0.20 * self.pace
                + 0.18 * self.passing
                + 0.15 * self.shooting
                + 0.08 * self.defending
                + 0.07 * self.physical
            )

        # Extremo Derecho / Izquierdo
        elif pos in ["RW", "LW", "ED", "EI"]:
            return round(
                0.35 * self.pace
                + 0.30 * self.dribbling
                + 0.15 * self.shooting
                + 0.10 * self.passing
                + 0.10 * self.physical
            )

        # Segundo Delantero
        elif pos in ["CF", "SS", "SD"]:
            return round(
                0.38 * self.dribbling
                + 0.27 * self.shooting
                + 0.20 * self.pace
                + 0.10 * self.passing
                + 0.05 * self.physical
            )

        # Delantero Centro
        elif pos in ["ST", "DC"]:
            return round(
                0.42 * self.shooting
                + 0.25 * self.dribbling
                + 0.18 * self.physical
                + 0.12 * self.pace
                + 0.10 * self.passing
                + 0.05 * self.defending
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
