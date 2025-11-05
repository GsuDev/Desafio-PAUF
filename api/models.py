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

    # TODO - HU5
    def calculate_overall_rating(self):
        return 50

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
