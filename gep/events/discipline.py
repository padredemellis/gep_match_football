from .base import Event


class Foul(Event):
    """
    Evento de Falta.
    """

    def __init__(
        self,
        event_id: str,
        timestamp: str,
        event_type: str,
        player_id: str,
        team_id: str,
        minute: int,
        game_session_id: str,
        location_in_the_field: str,
        fouled_player_id: str,
        sanction_type: str,
        sanction_severity: str,
    ):
        super().__init__(
            event_id,
            timestamp,
            "foul",
            player_id,
            team_id,
            minute,
            game_session_id,
            location_in_the_field,
        )

        self.fouled_player_id = fouled_player_id
        self.sanction_type = sanction_type
        self.sanction_severity = sanction_severity

    def is_valid(self) -> bool:
        if not super().is_valid():
            return False
        if not self.sanction_type:
            return False
        return True

    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()
        data.update(
            {
                "fouled_player_id": self.fouled_player_id,
                "sanction_type": self.sanction_type,
                "sanction_severity": self.sanction_severity,
            }
        )
        return data

    def __str__(self) -> str:
        return (
            f"Foul({self.player_id} fouled {self.fouled_player_id}, "
            f"sanction={self.sanction_type}, minute={self.minute})"
        )


class YellowCard(Event):
    def __init__(
        self,
        event_id: str,
        timestamp: str,
        player_id: str,
        team_id: str,
        minute: int,
        game_session_id: str,
        location_in_the_field: str,
        first_or_second: int,
        reason: str,
    ):
        super().__init__(
            event_id,
            timestamp,
            "yellow_card",
            player_id,
            team_id,
            minute,
            game_session_id,
            location_in_the_field,
        )

        self.first_or_second = first_or_second
        self.reason = reason

    def is_valid(self) -> bool:
        if not super().is_valid():
            return False
        if self.first_or_second not in (1, 2):
            return False
        if not self.reason:
            return False
        return True

    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()
        data.update(
            {
                "first_or_second": self.first_or_second,
                "reason": self.reason,
            }
        )
        return data

    def __str__(self) -> str:
        return (
            f"YellowCard({self.player_id} reason {self.reason}, "
            f"number={self.first_or_second}, minute={self.minute})"
        )


class RedCard(Event):
    def __init__(
        self,
        event_id: str,
        timestamp: str,
        player_id: str,
        team_id: str,
        minute: int,
        game_session_id: str,
        location_in_the_field: str,
        direct_or_second_yellow: str,
        reason: str,
    ):
        super().__init__(
            event_id,
            timestamp,
            "red_card",
            player_id,
            team_id,
            minute,
            game_session_id,
            location_in_the_field,
        )

        self.direct_or_second_yellow = direct_or_second_yellow
        self.reason = reason

    def is_valid(self) -> bool:
        if not super().is_valid():
            return False
        if not self.direct_or_second_yellow:
            return False
        if not self.reason:
            return False
        return True

    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()
        data.update(
            {
                "direct_or_second_yellow": self.direct_or_second_yellow,
                "reason": self.reason,
            }
        )
        return data

    def __str__(self) -> str:
        return (
            f"RedCard({self.player_id} reason {self.reason}, "
            f"type={self.direct_or_second_yellow}, minute={self.minute})"
        )
