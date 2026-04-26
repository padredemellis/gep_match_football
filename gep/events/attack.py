from typing import Optional
from .base import Event


class Goal(Event):
    """Evento de Gol."""

    def __init__(
        self,
        event_id: str,
        timestamp: str,
        player_id: str,
        team_id: str,
        minute: int,
        game_session_id: str,
        location_in_the_field: str,
        goal_type: str,
        goal_scorer_id: str,
        assister_id: Optional[str] = None,
    ):
        super().__init__(
            event_id=event_id,
            timestamp=timestamp,
            event_type="goal",
            player_id=player_id,
            team_id=team_id,
            minute=minute,
            game_session_id=game_session_id,
            location_in_the_field=location_in_the_field,
        )

        self.goal_type = goal_type
        self.goal_scorer_id = goal_scorer_id
        self.assister_id = assister_id

    def is_valid(self) -> bool:
        if not super().is_valid():
            return False
        if not self.goal_type:
            return False
        if not self.goal_scorer_id:
            return False
        return True

    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()
        data.update(
            {
                "goal_type": self.goal_type,
                "goal_scorer_id": self.goal_scorer_id,
                "assister_id": self.assister_id,
            }
        )
        return data

    def __str__(self) -> str:
        assister_info = f" from {self.assister_id}" if self.assister_id else ""
        return (
            f"Goal(scorer={self.goal_scorer_id}{assister_info}, "
            f"type={self.goal_type}, minute={self.minute})"
        )


class PassEvent(Event):
    """Pase a un compañero."""

    def __init__(
        self,
        event_id: str,
        timestamp: str,
        player_id: str,
        team_id: str,
        minute: int,
        game_session_id: str,
        location_in_the_field: str,
        passer_id: str,
        receiver_id: str,
        pass_success: bool,
        pass_type: str,
        distance: float,
    ):
        super().__init__(
            event_id,
            timestamp,
            "pass",
            player_id,
            team_id,
            minute,
            game_session_id,
            location_in_the_field,
        )

        self.passer_id = passer_id
        self.receiver_id = receiver_id
        self.pass_success = pass_success
        self.pass_type = pass_type
        self.distance = distance

    def is_valid(self) -> bool:
        if not super().is_valid():
            return False
        if not self.passer_id:
            return False
        if not self.receiver_id:
            return False
        if not self.pass_type:
            return False
        if self.distance < 0:
            return False
        return True

    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()
        data.update(
            {
                "passer_id": self.passer_id,
                "receiver_id": self.receiver_id,
                "pass_success": self.pass_success,
                "pass_type": self.pass_type,
                "distance": self.distance,
            }
        )
        return data

    def __str__(self) -> str:
        return (
            f"PassEvent({self.passer_id} -> {self.receiver_id}, "
            f"type={self.pass_type}, success={self.pass_success}, "
            f"distance={self.distance}, minute={self.minute})"
        )


class Shot(Event):
    """Tiro que NO es gol."""

    def __init__(
        self,
        event_id: str,
        timestamp: str,
        player_id: str,
        team_id: str,
        minute: int,
        game_session_id: str,
        location_in_the_field: str,
        shooter_id: str,
        on_target: bool,
        blocked: bool,
        save_by_goalkeeper: bool,
    ):
        super().__init__(
            event_id,
            timestamp,
            "shot",
            player_id,
            team_id,
            minute,
            game_session_id,
            location_in_the_field,
        )

        self.shooter_id = shooter_id
        self.on_target = on_target
        self.blocked = blocked
        self.save_by_goalkeeper = save_by_goalkeeper

    def is_valid(self) -> bool:
        if not super().is_valid():
            return False
        if not self.shooter_id:
            return False
        return True

    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()
        data.update(
            {
                "shooter_id": self.shooter_id,
                "on_target": self.on_target,
                "blocked": self.blocked,
                "save_by_goalkeeper": self.save_by_goalkeeper,
            }
        )
        return data

    def __str__(self) -> str:
        return (
            f"Shot(shooter={self.shooter_id}, on_target={self.on_target}, "
            f"blocked={self.blocked}, save_by_goalkeeper={self.save_by_goalkeeper}, "
            f"minute={self.minute})"
        )


class Penalty(Event):
    """Tiro penal."""

    def __init__(
        self,
        event_id: str,
        timestamp: str,
        player_id: str,
        team_id: str,
        minute: int,
        game_session_id: str,
        location_in_the_field: str,
        opposing_goalkeeper: str,
    ):
        super().__init__(
            event_id,
            timestamp,
            "penalty",
            player_id,
            team_id,
            minute,
            game_session_id,
            location_in_the_field,
        )

        self.opposing_goalkeeper = opposing_goalkeeper

    def is_valid(self) -> bool:
        if not super().is_valid():
            return False
        if not self.opposing_goalkeeper:
            return False
        return True

    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()
        data.update({"opposing_goalkeeper": self.opposing_goalkeeper})
        return data

    def __str__(self) -> str:
        return (
            f"Penalty(player={self.player_id}, goalkeeper={self.opposing_goalkeeper}, "
            f"minute={self.minute})"
        )