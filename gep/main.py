"""
GEP – Simulación de un partido de fútbol completo.

Simula Peñarol vs Nacional en el Campeón del Siglo,
generando eventos realistas a través del EventDispatcher y la EventQueue.
"""

import sys
from pathlib import Path

# Asegurar que el directorio raíz del proyecto esté en sys.path
# para que los imports absolutos (gep.*) funcionen al ejecutar directamente.
_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import uuid
import time
import random
from datetime import datetime, timedelta

from gep.match.match import Match
from gep.dispatcher.event_dispatcher import EventDispatcher
from gep.queue.event_queue import EventQueue
from gep.events import (
    KickOff,
    Goal,
    PassEvent,
    Shot,
    Penalty,
    Foul,
    YellowCard,
    RedCard,
    FreeKick,
    CornerKick,
    ThrowIn,
    GoalKick,
    Offside,
    Substitution,
    Interception,
    Dribble,
    GoalkeeperSave,
    Injury,
    VarReview,
)

# ------------------------------------------------------------------ #
#  Datos del partido
# ------------------------------------------------------------------ #

SESSION_ID = str(uuid.uuid4())
MATCH_START = datetime(2026, 4, 30, 21, 0, 0)

TEAMS = {
    "penarol": {
        "id": "penarol",
        "name": "Peñarol",
        "formation": "4-3-3",
        "players": {
            "GK": "Aguerre",
            "DEF1": "Escobar",
            "DEF2": "Lemos",
            "DEF3": "Ferreira",
            "DEF4": "Olivera",
            "MID1": "Remedi",
            "MID2": "L. Fernandez",
            "MID3": "Trindade",
            "FWD1": "Angulo",
            "FWD2": "M. Fernandez",
            "FWD3": "Arezo",
            "SUB1": "Maxi Silvera",
            "SUB2": "Brian Rodriguez",
            "SUB3": "Facundo Torres",
        },
    },
    "nacional": {
        "id": "nacional",
        "name": "Nacional",
        "formation": "4-4-2",
        "players": {
            "GK": "Mejia",
            "DEF1": "N. Rodriguez",
            "DEF2": "Coates",
            "DEF3": "Rogel",
            "DEF4": "Candido",
            "MID1": "Boggio",
            "MID2": "L. Rodriguez",
            "MID3": "Lodeiro",
            "MID4": "Barcia",
            "FWD1": "Veron Lupi",
            "FWD2": "Gomez",
            "SUB1": "Santiago Rodriguez",
            "SUB2": "Leandro Lozano",
            "SUB3": "Christian Oliva",
        },
    },
}

ZONES = [
    "propio_arco", "defensa_central", "defensa_izquierda", "defensa_derecha",
    "mediocampo_centro", "mediocampo_izquierda", "mediocampo_derecha",
    "ataque_centro", "ataque_izquierda", "ataque_derecha", "area_rival",
]

PASS_TYPES = ["corto", "largo", "filtrado", "centro", "pared"]
GOAL_TYPES = ["open_play", "header", "free_kick", "volley"]
FOUL_SEVERITIES = ["leve", "moderada", "fuerte"]

# ------------------------------------------------------------------ #
#  Helpers
# ------------------------------------------------------------------ #

_event_counter = 0


def _eid() -> str:
    global _event_counter
    _event_counter += 1
    return f"evt-{_event_counter:04d}"


def _ts(minute: int) -> str:
    """Genera un timestamp ISO basado en el minuto de juego."""
    dt = MATCH_START + timedelta(minutes=minute, seconds=random.randint(0, 59))
    return dt.isoformat()


def _pick_player(team_key: str, roles: list[str] | None = None) -> str:
    """Elige un jugador al azar de un equipo (opcionalmente filtrado por roles)."""
    players = TEAMS[team_key]["players"]
    if roles:
        candidates = {k: v for k, v in players.items() if k in roles}
    else:
        # Excluir suplentes por defecto
        candidates = {k: v for k, v in players.items() if not k.startswith("SUB")}
    return random.choice(list(candidates.values()))


def _zone() -> str:
    return random.choice(ZONES)


def _team_id(team_key: str) -> str:
    return TEAMS[team_key]["id"]


# ------------------------------------------------------------------ #
#  Handlers de ejemplo (listeners)
# ------------------------------------------------------------------ #

class MatchNarrator:
    """Narrador en tiempo real del partido."""

    LABELS = {
        "kick_off": "[KICK OFF]",
        "goal": "[GOL]",
        "shot": "[TIRO]",
        "pass": "[PASE]",
        "foul": "[FALTA]",
        "yellow_card": "[AMARILLA]",
        "red_card": "[ROJA]",
        "free_kick": "[T.LIBRE]",
        "corner_kick": "[CORNER]",
        "throw_in": "[LATERAL]",
        "goal_kick": "[S.ARCO]",
        "offside": "[OFFSIDE]",
        "substitution": "[CAMBIO]",
        "interception": "[INTERC.]",
        "dribble": "[REGATE]",
        "goalkeeper_save": "[ATAJADA]",
        "injury": "[LESION]",
        "var_review": "[VAR]",
        "penalty": "[PENAL]",
    }

    def narrate(self, event):
        label = self.LABELS.get(event.event_type, "[EVENTO]")
        print(f"  {label:>12}  [{event.minute}'] {event}")


class StatTracker:
    """Acumula estadísticas simples del partido."""

    def __init__(self):
        self.stats: dict[str, dict[str, int]] = {
            "penarol": {},
            "nacional": {},
        }

    def track(self, event):
        team = event.team_id
        etype = event.event_type
        if team in self.stats:
            self.stats[team][etype] = self.stats[team].get(etype, 0) + 1

    def print_summary(self):
        print("\n" + "=" * 60)
        print("ESTADISTICAS DEL PARTIDO")
        print("=" * 60)
        all_types = sorted(
            set().union(*(s.keys() for s in self.stats.values()))
        )
        header = f"{'Evento':<22} {'Peñarol':>10} {'Nacional':>10}"
        print(header)
        print("-" * len(header))
        for t in all_types:
            p = self.stats["penarol"].get(t, 0)
            n = self.stats["nacional"].get(t, 0)
            print(f"{t:<22} {p:>10} {n:>10}")


# ------------------------------------------------------------------ #
#  Generadores de secuencias de eventos
# ------------------------------------------------------------------ #

def generate_kickoff(team_key: str, minute: int) -> list:
    return [
        KickOff(
            event_id=_eid(), timestamp=_ts(minute),
            player_id=_pick_player(team_key, ["MID1", "MID2"]),
            team_id=_team_id(team_key), minute=minute,
            game_session_id=SESSION_ID, location_in_the_field="mediocampo_centro",
        )
    ]


def generate_passing_sequence(team_key: str, minute: int) -> list:
    """Genera 2-4 pases consecutivos."""
    events = []
    n_passes = random.randint(2, 4)
    for i in range(n_passes):
        passer = _pick_player(team_key)
        receiver = _pick_player(team_key)
        while receiver == passer:
            receiver = _pick_player(team_key)
        events.append(
            PassEvent(
                event_id=_eid(), timestamp=_ts(minute),
                player_id=passer, team_id=_team_id(team_key),
                minute=minute, game_session_id=SESSION_ID,
                location_in_the_field=_zone(),
                passer_id=passer, receiver_id=receiver,
                pass_success=random.random() < 0.80,
                pass_type=random.choice(PASS_TYPES),
                distance=round(random.uniform(5, 45), 1),
            )
        )
    return events


def generate_shot_sequence(team_key: str, minute: int) -> list:
    """Genera pases + tiro (sin gol)."""
    opp = "nacional" if team_key == "penarol" else "penarol"
    events = generate_passing_sequence(team_key, minute)
    shooter = _pick_player(team_key, ["FWD1", "FWD2", "FWD3", "MID3"])
    on_target = random.random() < 0.45
    events.append(
        Shot(
            event_id=_eid(), timestamp=_ts(minute),
            player_id=shooter, team_id=_team_id(team_key),
            minute=minute, game_session_id=SESSION_ID,
            location_in_the_field="area_rival",
            shooter_id=shooter, on_target=on_target,
            blocked=random.random() < 0.3,
            save_by_goalkeeper=on_target and random.random() < 0.6,
        )
    )
    # Posible atajada
    if events[-1].save_by_goalkeeper:
        events.append(
            GoalkeeperSave(
                event_id=_eid(), timestamp=_ts(minute),
                player_id=_pick_player(opp, ["GK"]),
                team_id=_team_id(opp), minute=minute,
                game_session_id=SESSION_ID, location_in_the_field="propio_arco",
            )
        )
    return events


def generate_goal_sequence(team_key: str, minute: int, scorer: str | None = None) -> list:
    """Genera pases + gol."""
    events = generate_passing_sequence(team_key, minute)
    scorer = scorer or _pick_player(team_key, ["FWD1", "FWD2", "FWD3"])
    assister = _pick_player(team_key, ["MID1", "MID2", "MID3"])
    events.append(
        Goal(
            event_id=_eid(), timestamp=_ts(minute),
            player_id=scorer, team_id=_team_id(team_key),
            minute=minute, game_session_id=SESSION_ID,
            location_in_the_field="area_rival",
            goal_type=random.choice(GOAL_TYPES),
            goal_scorer_id=scorer, assister_id=assister,
        )
    )
    return events


def generate_foul_sequence(fouling_team: str, minute: int) -> list:
    """Genera falta + posible tarjeta + tiro libre."""
    fouled_team = "nacional" if fouling_team == "penarol" else "penarol"
    events = []
    fouler = _pick_player(fouling_team)
    fouled = _pick_player(fouled_team)
    severity = random.choice(FOUL_SEVERITIES)

    events.append(
        Foul(
            event_id=_eid(), timestamp=_ts(minute),
            event_type="foul", player_id=fouler,
            team_id=_team_id(fouling_team), minute=minute,
            game_session_id=SESSION_ID, location_in_the_field=_zone(),
            fouled_player_id=fouled,
            sanction_type="falta", sanction_severity=severity,
        )
    )

    # Tarjeta amarilla en faltas moderadas/fuertes
    if severity in ("moderada", "fuerte") and random.random() < 0.6:
        events.append(
            YellowCard(
                event_id=_eid(), timestamp=_ts(minute),
                player_id=fouler, team_id=_team_id(fouling_team),
                minute=minute, game_session_id=SESSION_ID,
                location_in_the_field=_zone(),
                first_or_second=1, reason="falta táctica",
            )
        )

    # Tiro libre para el equipo fouled
    events.append(
        FreeKick(
            event_id=_eid(), timestamp=_ts(minute),
            player_id=_pick_player(fouled_team),
            team_id=_team_id(fouled_team), minute=minute,
            game_session_id=SESSION_ID, location_in_the_field=_zone(),
        )
    )
    return events


def generate_corner_sequence(team_key: str, minute: int) -> list:
    side = random.choice(["left", "right"])
    return [
        CornerKick(
            event_id=_eid(), timestamp=_ts(minute),
            player_id=_pick_player(team_key), team_id=_team_id(team_key),
            minute=minute, game_session_id=SESSION_ID,
            location_in_the_field=f"ataque_{side}", side=side,
        )
    ]


def generate_substitution(team_key: str, minute: int) -> list:
    return [
        Substitution(
            event_id=_eid(), timestamp=_ts(minute),
            player_id=_pick_player(team_key, ["SUB1", "SUB2", "SUB3"]),
            team_id=_team_id(team_key), minute=minute,
            game_session_id=SESSION_ID, location_in_the_field="mediocampo_centro",
            player_enters=_pick_player(team_key, ["SUB1", "SUB2", "SUB3"]),
            player_exits=_pick_player(team_key, ["MID1", "MID2", "FWD2"]),
            reason=random.choice(["táctico", "fatiga", "lesión"]),
        )
    ]


def generate_misc_event(team_key: str, minute: int) -> list:
    """Genera un evento variado: offside, intercepción, dribble, saque, etc."""
    choice = random.choice(["offside", "interception", "dribble", "throw_in", "goal_kick"])
    opp = "nacional" if team_key == "penarol" else "penarol"
    if choice == "offside":
        return [Offside(
            event_id=_eid(), timestamp=_ts(minute),
            player_id=_pick_player(team_key, ["FWD1", "FWD2"]),
            team_id=_team_id(team_key), minute=minute,
            game_session_id=SESSION_ID, location_in_the_field="ataque_centro",
        )]
    elif choice == "interception":
        return [Interception(
            event_id=_eid(), timestamp=_ts(minute),
            player_id=_pick_player(team_key, ["DEF1", "DEF2", "DEF3", "MID1"]),
            team_id=_team_id(team_key), minute=minute,
            game_session_id=SESSION_ID, location_in_the_field=_zone(),
        )]
    elif choice == "dribble":
        return [Dribble(
            event_id=_eid(), timestamp=_ts(minute),
            player_id=_pick_player(team_key, ["FWD1", "FWD2", "MID3"]),
            team_id=_team_id(team_key), minute=minute,
            game_session_id=SESSION_ID, location_in_the_field=_zone(),
        )]
    elif choice == "throw_in":
        return [ThrowIn(
            event_id=_eid(), timestamp=_ts(minute),
            player_id=_pick_player(team_key),
            team_id=_team_id(team_key), minute=minute,
            game_session_id=SESSION_ID, location_in_the_field=_zone(),
        )]
    else:
        return [GoalKick(
            event_id=_eid(), timestamp=_ts(minute),
            player_id=_pick_player(opp, ["GK"]),
            team_id=_team_id(opp), minute=minute,
            game_session_id=SESSION_ID, location_in_the_field="propio_arco",
        )]


# ------------------------------------------------------------------ #
#  Guion del partido (minuto a minuto)
# ------------------------------------------------------------------ #

def build_match_script() -> list[tuple[int, callable]]:
    """
    Retorna una lista de (minuto, generador_de_eventos).
    Mezcla acciones predefinidas con acciones aleatorias.
    Peñarol gana 3-1.
    """
    script: list[tuple] = []

    # ---- PRIMER TIEMPO ---- #
    script.append((0, lambda: generate_kickoff("penarol", 0)))

    # Primeros minutos — pases y tanteo
    for m in range(2, 10, 2):
        team = random.choice(["penarol", "nacional"])
        script.append((m, lambda t=team, mm=m: generate_passing_sequence(t, mm)))

    # Falta de Nacional min 12
    script.append((12, lambda: generate_foul_sequence("nacional", 12)))

    # Tiro de Peñarol min 15
    script.append((15, lambda: generate_shot_sequence("penarol", 15)))

    # Corner de Peñarol min 18
    script.append((18, lambda: generate_corner_sequence("penarol", 18)))

    # Más pases / misceláneos
    for m in range(20, 30, 3):
        team = random.choice(["penarol", "nacional"])
        script.append((m, lambda t=team, mm=m: random.choice([
            generate_passing_sequence, generate_misc_event
        ])(t, mm)))

    # GOL de Peñarol — minuto 28 (Arezo abre el marcador)
    script.append((28, lambda: generate_goal_sequence("penarol", 28, "Arezo")))

    # Falta de Peñarol min 33
    script.append((33, lambda: generate_foul_sequence("penarol", 33)))

    # Tiro de Nacional min 37
    script.append((37, lambda: generate_shot_sequence("nacional", 37)))

    # GOL de Peñarol — minuto 41 (L. Fernandez de tiro libre)
    script.append((41, lambda: generate_goal_sequence("penarol", 41, "L. Fernandez")))

    # Offside / misc min 43
    script.append((43, lambda: generate_misc_event("nacional", 43)))

    # Tiempo añadido primer tiempo
    script.append((45, lambda: generate_foul_sequence("nacional", 45)))

    # ---- SEGUNDO TIEMPO ---- #
    script.append((46, lambda: generate_kickoff("nacional", 46)))

    # Ataque Nacional
    script.append((50, lambda: generate_shot_sequence("nacional", 50)))

    # GOL de Nacional — minuto 55 (descuento de Veron Lupi)
    script.append((55, lambda: generate_goal_sequence("nacional", 55, "Veron Lupi")))

    # Cambio en Peñarol min 60
    script.append((60, lambda: generate_substitution("penarol", 60)))

    # Falta fuerte de Nacional min 63
    script.append((63, lambda: generate_foul_sequence("nacional", 63)))

    # Misc events
    for m in range(65, 75, 3):
        team = random.choice(["penarol", "nacional"])
        script.append((m, lambda t=team, mm=m: random.choice([
            generate_shot_sequence, generate_misc_event, generate_passing_sequence
        ])(t, mm)))

    # Cambio en Nacional min 72
    script.append((72, lambda: generate_substitution("nacional", 72)))

    # GOL de Peñarol — minuto 78 (Arezo sentencia el clasico con doblete)
    script.append((78, lambda: generate_goal_sequence("penarol", 78, "Arezo")))

    # Lesión min 82
    script.append((82, lambda: [
        Injury(
            event_id=_eid(), timestamp=_ts(82),
            player_id="Remedi", team_id="penarol",
            minute=82, game_session_id=SESSION_ID,
            location_in_the_field="mediocampo_centro",
        ),
        *generate_substitution("penarol", 82),
    ]))

    # VAR Review min 85 — se anula posible gol de Nacional
    script.append((85, lambda: [
        VarReview(
            event_id=_eid(), timestamp=_ts(85),
            player_id="Veron Lupi", team_id="nacional",
            minute=85, game_session_id=SESSION_ID,
            location_in_the_field="area_rival",
        )
    ]))

    # Últimos minutos tensos
    script.append((87, lambda: generate_foul_sequence("nacional", 87)))
    script.append((89, lambda: generate_shot_sequence("nacional", 89)))

    # Tiempo añadido — Peñarol aguanta
    script.append((90, lambda: generate_misc_event("penarol", 90)))
    script.append((92, lambda: generate_foul_sequence("penarol", 92)))

    script.sort(key=lambda x: x[0])
    return script


# ------------------------------------------------------------------ #
#  Simulación principal
# ------------------------------------------------------------------ #

def main():
    print("=" * 60)
    print("GEP - SIMULACION DE PARTIDO DE FUTBOL")
    print("=" * 60)

    # 1. Crear el partido
    match = Match(
        match_id=str(uuid.uuid4()),
        stadium="Estadio Campeón del Siglo",
        climate="Noche fresca, 14°C",
        league="Primera División Uruguay",
        team_1="penarol",
        team_2="nacional",
        referee="Esteban Ostojich",
        timestamp_start=MATCH_START.isoformat(),
        formation_team_1=TEAMS["penarol"]["formation"],
        formation_team_2=TEAMS["nacional"]["formation"],
    )

    # 2. Crear dispatcher y queue
    dispatcher = EventDispatcher()
    queue = EventQueue()

    # 3. Registrar listeners
    narrator = MatchNarrator()
    stats = StatTracker()

    dispatcher.subscribe("*", narrator.narrate)
    dispatcher.subscribe("*", stats.track)

    # Handler especial para goles: actualiza el score del partido
    def on_goal(event):
        match.update_score(event.team_id)
        team_name = (
            TEAMS["penarol"]["name"] if event.team_id == "penarol"
            else TEAMS["nacional"]["name"]
        )
        print(
            f"\n  >>> GOOOL DE {team_name.upper()} !!!  "
            f"Marca: {match.score_team_1} - {match.score_team_2}\n"
        )

    dispatcher.subscribe("goal", on_goal)

    # 4. Generar guion y encolar eventos
    script = build_match_script()

    print(f"\n  {TEAMS['penarol']['name']} ({TEAMS['penarol']['formation']}) "
          f"vs {TEAMS['nacional']['name']} ({TEAMS['nacional']['formation']})")
    print(f"  Estadio: {match.stadium} | Clima: {match.climate}")
    print(f"  Arbitro: {match.referee}")
    print(f"  Sesion: {SESSION_ID[:8]}...")

    # ---- PRIMER TIEMPO ---- #
    print("\n" + "-" * 60)
    print("PRIMER TIEMPO")
    print("-" * 60)
    match.start_match()

    for minute, gen_fn in script:
        if minute == 46:
            # Entretiempo
            match.add_extra_time(2)
            print("\n" + "-" * 60)
            print(f"ENTRETIEMPO  |  {match.score_team_1} - {match.score_team_2}")
            print("-" * 60)
            time.sleep(0.3)
            print("\n" + "-" * 60)
            print("SEGUNDO TIEMPO")
            print("-" * 60)

        events = gen_fn()
        for event in events:
            queue.inqueue(event)

        # Procesar la cola
        while not queue.is_empty():
            evt = queue.outqueue()
            dispatcher.dispatch(evt)
            time.sleep(1)

    # ---- FIN DEL PARTIDO ---- #
    match.add_extra_time(4)
    match.end_match((MATCH_START + timedelta(minutes=96)).isoformat())

    print("\n" + "-" * 60)
    print("FINAL DEL PARTIDO")
    print("-" * 60)
    print(f"\n  {TEAMS['penarol']['name']} {match.score_team_1}"
          f" - {match.score_team_2} {TEAMS['nacional']['name']}")

    if match.score_team_1 > match.score_team_2:
        winner = TEAMS["penarol"]["name"]
    elif match.score_team_2 > match.score_team_1:
        winner = TEAMS["nacional"]["name"]
    else:
        winner = None

    if winner:
        print(f"  Ganador: {winner}")
    else:
        print("  Empate")

    # 5. Estadísticas
    stats.print_summary()

    # 6. Resumen del dispatcher
    print(f"\n  {dispatcher}")
    history = dispatcher.get_history()
    print(f"  Total de eventos registrados: {len(history)}")
    print(f"  Goles: {len(dispatcher.get_history_by_type('goal'))}")
    print(f"  Amarillas: {len(dispatcher.get_history_by_type('yellow_card'))}")
    print(f"  Faltas: {len(dispatcher.get_history_by_type('foul'))}")
    print(f"  Tiros: {len(dispatcher.get_history_by_type('shot'))}")
    print(f"  Pases: {len(dispatcher.get_history_by_type('pass'))}")


if __name__ == "__main__":
    main()
