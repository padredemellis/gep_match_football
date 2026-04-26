from pathlib import Path
import sys

# Permite ejecutar este archivo directamente sin usar `-m`.
if __package__ is None or __package__ == "":
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

from gep.events import (
    CornerKick,
    DisallowedGoal,
    Dribble,
    Event,
    ExtraTimeOrPenaltyShootout,
    Foul,
    FreeKick,
    Goal,
    GoalKick,
    GoalkeeperSave,
    Injury,
    Interception,
    KickOff,
    Offside,
    PassEvent,
    Penalty,
    RedCard,
    Shot,
    Substitution,
    ThrowIn,
    VarReview,
    YellowCard,
)
from gep.match import Match


def main() -> None:
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
    partido.start_match()

    print("=" * 60)
    print("PARTIDO DE PRUEBA CON TODAS LAS CLASES DE EVENTOS")
    print("=" * 60)
    print(f"Partido: {partido}")
    print()

    eventos: list[Event] = [
        Event(
            event_id="evt_000",
            timestamp="2026-04-25T18:00:00Z",
            event_type="generic_event",
            player_id="player_ref",
            team_id="team_Uruguay",
            minute=0,
            game_session_id=partido.match_id,
            location_in_the_field="center",
        ),
        KickOff(
            event_id="evt_001",
            timestamp="2026-04-25T18:00:01Z",
            player_id="player_10",
            team_id="team_Uruguay",
            minute=0,
            game_session_id=partido.match_id,
            location_in_the_field="center",
        ),
        PassEvent(
            event_id="evt_002",
            timestamp="2026-04-25T18:03:10Z",
            player_id="player_10",
            team_id="team_Uruguay",
            minute=3,
            game_session_id=partido.match_id,
            location_in_the_field="middle_third",
            passer_id="player_10",
            receiver_id="player_8",
            pass_success=True,
            pass_type="short",
            distance=12.5,
        ),
        Dribble(
            event_id="evt_003",
            timestamp="2026-04-25T18:04:05Z",
            player_id="player_8",
            team_id="team_Uruguay",
            minute=4,
            game_session_id=partido.match_id,
            location_in_the_field="left_wing",
        ),
        Interception(
            event_id="evt_004",
            timestamp="2026-04-25T18:06:00Z",
            player_id="player_5_BR",
            team_id="team_Brazil",
            minute=6,
            game_session_id=partido.match_id,
            location_in_the_field="middle_third",
        ),
        Foul(
            event_id="evt_005",
            timestamp="2026-04-25T18:07:22Z",
            event_type="foul",
            player_id="player_5_BR",
            team_id="team_Brazil",
            minute=7,
            game_session_id=partido.match_id,
            location_in_the_field="middle_third",
            fouled_player_id="player_8",
            sanction_type="yellow_card",
            sanction_severity="minor",
        ),
        YellowCard(
            event_id="evt_006",
            timestamp="2026-04-25T18:07:30Z",
            player_id="player_5_BR",
            team_id="team_Brazil",
            minute=7,
            game_session_id=partido.match_id,
            location_in_the_field="middle_third",
            first_or_second=1,
            reason="late_tackle",
        ),
        FreeKick(
            event_id="evt_007",
            timestamp="2026-04-25T18:08:10Z",
            player_id="player_10",
            team_id="team_Uruguay",
            minute=8,
            game_session_id=partido.match_id,
            location_in_the_field="attacking_third",
        ),
        CornerKick(
            event_id="evt_008",
            timestamp="2026-04-25T18:09:01Z",
            player_id="player_7",
            team_id="team_Uruguay",
            minute=9,
            game_session_id=partido.match_id,
            location_in_the_field="right_corner",
            side="right",
        ),
        Shot(
            event_id="evt_009",
            timestamp="2026-04-25T18:09:25Z",
            player_id="player_9",
            team_id="team_Uruguay",
            minute=9,
            game_session_id=partido.match_id,
            location_in_the_field="penalty_area",
            shooter_id="player_9",
            on_target=True,
            blocked=False,
            save_by_goalkeeper=True,
        ),
        GoalkeeperSave(
            event_id="evt_010",
            timestamp="2026-04-25T18:09:26Z",
            player_id="player_gk_BR",
            team_id="team_Brazil",
            minute=9,
            game_session_id=partido.match_id,
            location_in_the_field="goal_area",
        ),
        ThrowIn(
            event_id="evt_011",
            timestamp="2026-04-25T18:12:00Z",
            player_id="player_2",
            team_id="team_Uruguay",
            minute=12,
            game_session_id=partido.match_id,
            location_in_the_field="right_side_line",
        ),
        GoalKick(
            event_id="evt_012",
            timestamp="2026-04-25T18:13:10Z",
            player_id="player_gk_BR",
            team_id="team_Brazil",
            minute=13,
            game_session_id=partido.match_id,
            location_in_the_field="goal_area",
        ),
        Penalty(
            event_id="evt_013",
            timestamp="2026-04-25T18:40:00Z",
            player_id="player_9",
            team_id="team_Uruguay",
            minute=40,
            game_session_id=partido.match_id,
            location_in_the_field="penalty_spot",
            opposing_goalkeeper="player_gk_BR",
        ),
        Goal(
            event_id="evt_014",
            timestamp="2026-04-25T18:40:20Z",
            player_id="player_9",
            team_id="team_Uruguay",
            minute=40,
            game_session_id=partido.match_id,
            location_in_the_field="penalty_area",
            goal_type="right_foot",
            goal_scorer_id="player_9",
            assister_id="player_10",
        ),
        Injury(
            event_id="evt_015",
            timestamp="2026-04-25T18:44:30Z",
            player_id="player_6",
            team_id="team_Uruguay",
            minute=44,
            game_session_id=partido.match_id,
            location_in_the_field="middle_third",
        ),
        Substitution(
            event_id="evt_016",
            timestamp="2026-04-25T18:46:00Z",
            player_id="player_coach_UY",
            team_id="team_Uruguay",
            minute=46,
            game_session_id=partido.match_id,
            location_in_the_field="technical_area",
            player_enters="player_14",
            player_exits="player_6",
            reason="injury",
        ),
        Offside(
            event_id="evt_017",
            timestamp="2026-04-25T19:10:00Z",
            player_id="player_11_BR",
            team_id="team_Brazil",
            minute=55,
            game_session_id=partido.match_id,
            location_in_the_field="attacking_third",
        ),
        VarReview(
            event_id="evt_018",
            timestamp="2026-04-25T19:11:00Z",
            player_id="player_ref",
            team_id="team_Uruguay",
            minute=56,
            game_session_id=partido.match_id,
            location_in_the_field="center",
        ),
        DisallowedGoal(
            event_id="evt_019",
            timestamp="2026-04-25T19:11:20Z",
            player_id="player_11_BR",
            team_id="team_Brazil",
            minute=56,
            game_session_id=partido.match_id,
            location_in_the_field="penalty_area",
        ),
        RedCard(
            event_id="evt_020",
            timestamp="2026-04-25T19:25:00Z",
            player_id="player_3_BR",
            team_id="team_Brazil",
            minute=70,
            game_session_id=partido.match_id,
            location_in_the_field="middle_third",
            direct_or_second_yellow="direct",
            reason="violent_conduct",
        ),
        ExtraTimeOrPenaltyShootout(
            event_id="evt_021",
            timestamp="2026-04-25T20:00:00Z",
            player_id="player_ref",
            team_id="team_Uruguay",
            minute=90,
            game_session_id=partido.match_id,
            location_in_the_field="center",
        ),
    ]

    partido.update_score("Uruguay", 1)
    partido.add_extra_time(5)

    print("EVENTOS CREADOS:")
    print("-" * 60)
    valid_count = 0
    for idx, evento in enumerate(eventos, start=1):
        is_ok = evento.is_valid()
        valid_count += int(is_ok)
        print(f"{idx:02d}. {evento}")
        print(f"    valido={is_ok} | tipo={evento.event_type}")

    partido.end_match("2026-04-25T20:05:00Z")

    print()
    print("RESUMEN FINAL:")
    print("-" * 60)
    print(f"Total de clases/eventos probados: {len(eventos)}")
    print(f"Eventos validos: {valid_count}/{len(eventos)}")
    print(f"Score final: {partido.score_team_1}-{partido.score_team_2}")
    print(f"Tiempo agregado: {partido.added_time_minutes} minutos")
    print(f"Estado partido: {partido.status}")
    print(f"Dict partido: {partido.to_dict()}")


if __name__ == "__main__":
    main()
