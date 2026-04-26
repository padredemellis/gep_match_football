from .base import Event


class FreeKick(Event):
    """
    Tiro Libre
    """

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
            "free_kick",
            player_id,
            team_id,
            minute,
            game_session_id,
            location_in_the_field,
        )

    def __str__(self) -> str:
        return f"FreeKick(player={self.player_id}, minute={self.minute})"


class CornerKick(Event):
    """
    Tiro de esquina
    """
    def __init__(
        self,
        event_id: str,
        timestamp: str,
        player_id: str,
        team_id: str,
        minute: int,
        game_session_id: str,
        location_in_the_field: str,
        side: str,
    ):
        super().__init__(
            event_id,
            timestamp,
            "corner_kick",
            player_id,
            team_id,
            minute,
            game_session_id,
            location_in_the_field,
        )

        self.side = side

    def is_valid(self) -> bool:
        if not super().is_valid():
            return False
        if self.side not in ("left", "right", "izquierda", "derecha"):
            return False
        return True

    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()
        data.update({"side": self.side})
        return data

    def __str__(self) -> str:
        return f"CornerKick(player={self.player_id}, side={self.side}, minute={self.minute})"


class ThrowIn(Event):
    """
    Saque de banda
    """

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
            "throw_in",
            player_id,
            team_id,
            minute,
            game_session_id,
            location_in_the_field,
        )

    def __str__(self) -> str:
        return f"ThrowIn(player={self.player_id}, minute={self.minute})"


class GoalKick(Event):
    """
    Saque de arco
    """

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
            "goal_kick",
            player_id,
            team_id,
            minute,
            game_session_id,
            location_in_the_field,
        )

    def __str__(self) -> str:
        return f"GoalKick(player={self.player_id}, minute={self.minute})"
