from .base import Event


class GoalkeeperSave(Event):
    """Atajada del arquero."""

    def __init__(
        self,
        event_id: str,
        timestamp: str,
        player_id: str,
        team_id: str,
        minute: int,
        game_session_id: str,
        location_in_the_field: str,
    ):
        super().__init__(
            event_id,
            timestamp,
            "goalkeeper_save",
            player_id,
            team_id,
            minute,
            game_session_id,
            location_in_the_field,
        )

    def __str__(self) -> str:
        return f"GoalkeeperSave(player={self.player_id}, minute={self.minute})"


class Injury(Event):
    """Lesión de un jugador."""

    def __init__(
        self,
        event_id: str,
        timestamp: str,
        player_id: str,
        team_id: str,
        minute: int,
        game_session_id: str,
        location_in_the_field: str,
    ):
        super().__init__(
            event_id,
            timestamp,
            "injury",
            player_id,
            team_id,
            minute,
            game_session_id,
            location_in_the_field,
        )

    def __str__(self) -> str:
        return f"Injury(player={self.player_id}, minute={self.minute})"


class VarReview(Event):
    """Revisión por VAR."""

    def __init__(
        self,
        event_id: str,
        timestamp: str,
        player_id: str,
        team_id: str,
        minute: int,
        game_session_id: str,
        location_in_the_field: str,
    ):
        super().__init__(
            event_id,
            timestamp,
            "var_review",
            player_id,
            team_id,
            minute,
            game_session_id,
            location_in_the_field,
        )

    def __str__(self) -> str:
        return f"VarReview(player={self.player_id}, minute={self.minute})"


class DisallowedGoal(Event):
    """Gol anulado."""

    def __init__(
        self,
        event_id: str,
        timestamp: str,
        player_id: str,
        team_id: str,
        minute: int,
        game_session_id: str,
        location_in_the_field: str,
    ):
        super().__init__(
            event_id,
            timestamp,
            "disallowed_goal",
            player_id,
            team_id,
            minute,
            game_session_id,
            location_in_the_field,
        )

    def __str__(self) -> str:
        return f"DisallowedGoal(player={self.player_id}, minute={self.minute})"



class ExtraTimeOrPenaltyShootout(Event):
    """Tiempo extra o tanda de penales."""

    def __init__(
        self,
        event_id: str,
        timestamp: str,
        player_id: str,
        team_id: str,
        minute: int,
        game_session_id: str,
        location_in_the_field: str,
    ):
        super().__init__(
            event_id,
            timestamp,
            "extra_time_or_penalty_shootout",
            player_id,
            team_id,
            minute,
            game_session_id,
            location_in_the_field,
        )

    def __str__(self) -> str:
        return f"ExtraTimeOrPenaltyShootout(minute={self.minute})"