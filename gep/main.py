from gep.events import Event, Goal
from gep.match import Match


def main() -> None:
    print("=" * 50)
    print("PRUEBA 1: Crear evento base")
    print("=" * 50)

    evento1 = Event(
        event_id="evt_001",
        timestamp="2026-04-25T45:30.000Z",
        event_type="kickoff",
        player_id="player_1",
        team_id="team_Uruguay",
        minute=0,
        game_session_id="match_001",
        location_in_the_field="center",
    )

    print(f"Evento: {evento1}")
    print(f"¿Válido? {evento1.is_valid()}")
    print(f"Dict: {evento1.to_dict()}")
    print()

    print("=" * 50)
    print("PRUEBA 2: Crear un Goal")
    print("=" * 50)

    gol = Goal(
        event_id="evt_002",
        timestamp="2026-04-25T45:32.000Z",
        player_id="player_D.Nuñez",
        team_id="team_Uruguay",
        minute=45,
        game_session_id="match_001",
        location_in_the_field="penalty_area",
        goal_type="right_foot",
        goal_scorer_id="player_D.Nuñez",
        assister_id="player_F.Valverde",
    )

    print(f"Gol: {gol}")
    print(f"¿Válido? {gol.is_valid()}")
    print(f"Dict: {gol.to_dict()}")
    print()

    print("=" * 50)
    print("PRUEBA 3: Crear un Match")
    print("=" * 50)

    partido = Match(
        match_id="match_001",
        stadium="Maracanã",
        climate="sunny",
        league="Copa America",
        team_1="Uruguay",
        team_2="Brazil",
        referee="Pierluigi Collina",
        timestamp_start="2026-04-25T18:00.000Z",
        formation_team_1="4-3-3",
        formation_team_2="4-2-4",
    )

    print(f"Partido: {partido}")
    print(f"Status: {partido.status}")

    partido.start_match()
    print(f"Status después de start: {partido.status}")

    partido.update_score("Uruguay", 1)
    print(f"Score después de gol: {partido.score_team_1}-{partido.score_team_2}")

    partido.end_match("2026-04-25T20:00.000Z")
    print(f"Status final: {partido.status}")
    print(f"Dict: {partido.to_dict()}")


if __name__ == "__main__":
    main()
