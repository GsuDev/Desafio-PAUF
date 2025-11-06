from django.core.management.base import BaseCommand
from faker import Faker
from api.models import User


class Command(BaseCommand):
    help = "Carga 30 usuarios de ejemplo en la base de datos (sin equipo asignado)"

    def handle(self, *args, **kwargs):
        fake = Faker()
        users = []

        # Usamos _ porque no vamos a necesitar la variable de iteración
        for _ in range(30):
            users.append(
                User(name=fake.name(), email=fake.unique.email(), password=fake.password(length=10))
            )

        # Crea todos los users del array de golpe
        User.objects.bulk_create(users)

        # Enseña por terminal un mensaje de exito
        self.stdout.write(self.style.SUCCESS("✅ 30 users successfully created!"))
