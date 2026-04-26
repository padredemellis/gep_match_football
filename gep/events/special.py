from .base import Event


class KickOff(Event):
    """Inicio del partido."""

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
            event_id=event_id,
            timestamp=timestamp,
            event_type="kick_off",
            player_id=player_id,
            team_id=team_id,
            minute=minute,
            game_session_id=game_session_id,
            location_in_the_field=location_in_the_field,
        )


class Offside(Event):
    """Fuera de juego."""

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
            "offside",
            player_id,
            team_id,
            minute,
            game_session_id,
            location_in_the_field,
        )

    def __str__(self) -> str:
        return f"Offside(player={self.player_id}, minute={self.minute})"


class Substitution(Event):
    """Cambio de jugador."""

    def __init__(
        self,
        event_id: str,
        timestamp: str,
        player_id: str,
        team_id: str,
        minute: int,
        game_session_id: str,
        location_in_the_field: str,
        player_enters: str,
        player_exits: str,
        reason: str,
    ):
        super().__init__(
            event_id,
            timestamp,
            "substitution",
            player_id,
            team_id,
            minute,
            game_session_id,
            location_in_the_field,
        )

        self.player_enters = player_enters
        self.player_exits = player_exits
        self.reason = reason

    def is_valid(self) -> bool:
        if not super().is_valid():
            return False
        if not self.player_enters:
            return False
        if not self.player_exits:
            return False
        if not self.reason:
            return False
        return True

    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()
        data.update(
            {
                "player_enters": self.player_enters,
                "player_exits": self.player_exits,
                "reason": self.reason,
            }
        )
        return data

    def __str__(self) -> str:
        return (
            f"Substitution(in={self.player_enters}, out={self.player_exits}, "
            f"reason={self.reason}, minute={self.minute})"
        )


class Interception(Event):
    """Intercepción/Robo de balón."""

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
            "interception",
            player_id,
            team_id,
            minute,
            game_session_id,
            location_in_the_field,
        )

    def __str__(self) -> str:
        return f"Interception(player={self.player_id}, minute={self.minute})"


class Dribble(Event):
    """Regate de un jugador."""

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
            "dribble",
            player_id,
            team_id,
            minute,
            game_session_id,
            location_in_the_field,
        )

    def __str__(self) -> str:
        return f"Dribble(player={self.player_id}, minute={self.minute})"
