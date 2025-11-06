import json
from django.core.management.base import BaseCommand
from api.models import Card


class Command(BaseCommand):
    help = "Carga 150 cartas de un JSON (api/data/cards.json)"

    def handle(self, *args, **kwargs):
        file_path = "api/data/cards.json"

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            cards = []
            for item in data:
                card = Card(
                    name=item.get("name"),
                    country=item.get("country"),
                    club=item.get("club"),
                    league=item.get("league"),
                    position=item.get("position"),
                    pace=item.get("pace", 0),
                    shooting=item.get("shooting", 0),
                    passing=item.get("passing", 0),
                    dribbling=item.get("dribbling", 0),
                    defending=item.get("defending", 0),
                    physical=item.get("physical", 0),
                    diving=item.get("diving", 0),
                    reflexes=item.get("reflexes", 0),
                    handling=item.get("handling", 0),
                    positioning=item.get("positioning", 0),
                    kicking=item.get("kicking", 0),
                    speed=item.get("speed", 0),
                )
                cards.append(card)
                card.save()

            self.stdout.write(
                self.style.SUCCESS(f"✅ {len(cards)} cartas cargadas satisfactoriamente!")
            )

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR("❌ Archivo no encontrado: api/data/cards.json")
            )
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("❌ Formato JSON invalido"))
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f"❌ Faltan campos en el JSON: {e}"))
