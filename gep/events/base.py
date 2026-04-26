class Event:
    """
    Clase base para todos los eventos de futbol.
    Define la estructura común que todos los eventos heredan.
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
    ):
        self.event_id = event_id
        self.timestamp = timestamp
        self.event_type = event_type
        self.player_id = player_id
        self.team_id = team_id
        self.minute = minute
        self.game_session_id = game_session_id
        self.location_in_the_field = location_in_the_field

    def is_valid(self) -> bool:
        if not self.event_id:
            return False
        if not self.timestamp:
            return False
        if not self.event_type:
            return False
        if not self.player_id:
            return False
        if not self.team_id:
            return False
        if self.minute < 0 or self.minute > 120:
            return False
        if not self.game_session_id:
            return False
        if not self.location_in_the_field:
            return False

        return True

    def to_dict(self) -> dict[str, object]:
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "player_id": self.player_id,
            "team_id": self.team_id,
            "minute": self.minute,
            "game_session_id": self.game_session_id,
            "location_in_the_field": self.location_in_the_field,
        }

    def __str__(self) -> str:
        return (
            f"Event(id={self.event_id}, type={self.event_type}, "
            f"player={self.player_id}, minute={self.minute})"
        )
