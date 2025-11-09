import csv
import json

INPUT_FILE = "sofifa_players.csv"  # CSV original
OUTPUT_FILE = "cards_clean.json"  # JSON final (solo los 150 primeros válidos)

# Campos a conservar (csv_field -> model_field)
FIELDS = {
    "long_name": "name",
    "nationality_name": "country",
    "club_name": "club",
    "league_name": "league",
    "player_positions": "position",
    # para outfield: pace, shooting, passing, dribbling, defending, physic (physic -> physical)
    "pace": "pace",
    "shooting": "shooting",
    "passing": "passing",
    "dribbling": "dribbling",
    "defending": "defending",
    "physic": "physical",
    # campos de portero (se usan solo si es POR)
    "goalkeeping_diving": "diving",
    "goalkeeping_handling": "handling",
    "goalkeeping_kicking": "kicking",
    "goalkeeping_positioning": "positioning",
    "goalkeeping_reflexes": "reflexes",
    # movimiento / potencia (auxiliares)
    "movement_sprint_speed": "speed"
}

# Traducción posiciones FIFA -> tus códigos
POSITION_MAP = {
    "GK": "POR",
    "RB": "LD",
    "CB": "DFC",
    "LB": "LI",
    "CDM": "MCD",
    "CM": "MC",
    "CAM": "MCO",
    "LM": "MI",
    "RM": "MD",
    "CF": "SD",
    "LW": "EI",
    "RW": "ED",
    "ST": "DC",
}

POSICIONES_VALIDAS = set(POSITION_MAP.values())


def safe_int(value):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def map_position(raw_pos):
    """Convierte posiciones del CSV en inglés a tu formato español (solo la primera)."""
    if not raw_pos:
        return None
    pos = raw_pos.split(",")[0].strip().upper()
    return POSITION_MAP.get(pos)


def build_card_from_row(row):
    """Construye el diccionario completo con todos los campos del modelo."""
    card = {
        "name": row.get("long_name") or row.get("short_name") or "",
        "country": row.get("nationality_name") or "",
        "club": row.get("club_name") or "",
        "league": row.get("league_name") or "",
    }

    raw_pos = row.get("player_positions")
    mapped_pos = map_position(raw_pos)
    if not mapped_pos:
        return None
    card["position"] = mapped_pos

    # Stats base (jugadores de campo)
    card["pace"] = safe_int(
        row.get("pace")
        or row.get("movement_sprint_speed")
        or row.get("acceleration")
        or row.get("movement_acceleration")
        or 0
    )
    card["shooting"] = safe_int(
        row.get("shooting") or row.get("goalkeeping_kicking") or 0
    )
    card["passing"] = safe_int(
        row.get("passing")
        or row.get("attacking_short_passing")
        or row.get("goalkeeping_kicking")
        or 0
    )
    card["dribbling"] = safe_int(
        row.get("dribbling") or row.get("skill_dribbling") or 0
    )
    card["defending"] = safe_int(
        row.get("defending")
        or row.get("goalkeeping_reflexes")
        or row.get("goalkeeping_positioning")
        or 0
    )
    card["physical"] = safe_int(
        row.get("physic")
        or row.get("power_strength")
        or row.get("goalkeeping_diving")
        or 0
    )

    # Campos de portero siempre incluidos (aunque sea jugador)
    card["diving"] = safe_int(row.get("goalkeeping_diving") or 0)
    card["reflexes"] = safe_int(row.get("goalkeeping_reflexes") or 0)
    card["handling"] = safe_int(row.get("goalkeeping_handling") or 0)
    card["positioning"] = safe_int(row.get("goalkeeping_positioning") or 0)
    card["kicking"] = safe_int(row.get("goalkeeping_kicking") or 0)
    card["speed"] = safe_int(row.get("movement_sprint_speed") or 0)

    return card


def main():
    cards = []
    seen_names = set()

    with open(INPUT_FILE, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if len(cards) >= 600:
                break

            card = build_card_from_row(row)
            if not card:
                continue  # posición inválida o faltante

            # evitar duplicados por nombre exacto (simple heuristic)
            if card["name"] in seen_names:
                continue
            seen_names.add(card["name"])

            cards.append(card)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)

    print(f"✅ Exported {len(cards)} valid cards to {OUTPUT_FILE}")
    # resumen por posición
    from collections import Counter

    cnt = Counter(c["position"] for c in cards)
    print("Position counts:")
    for pos, n in cnt.most_common():
        print(f"  {pos}: {n}")


if __name__ == "__main__":
    main()
