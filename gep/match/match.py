from typing import Optional


class Match:
    """
    Clase que representa un partido de futbol.
    Contiene información del contexto del partido.
    """

    def __init__(
        self,
        match_id: str,
        stadium: str,
        climate: str,
        league: str,
        team_1: str,
        team_2: str,
        referee: str,
        timestamp_start: str,
        formation_team_1: str,
        formation_team_2: str,
    ):
        self.match_id = match_id
        self.stadium = stadium
        self.climate = climate
        self.league = league
        self.team_1 = team_1
        self.team_2 = team_2
        self.referee = referee
        self.timestamp_start = timestamp_start
        self.timestamp_end: Optional[str] = None
        self.formation_team_1 = formation_team_1
        self.formation_team_2 = formation_team_2
        self.added_time_minutes: int = 0
        self.status = "not_started"
        self.score_team_1 = 0
        self.score_team_2 = 0

    def start_match(self):
        """Inicia el partido."""
        self.status = "ongoing"
    
    def add_extra_time(self, minutes: int):
        self.added_time_minutes = minutes

    def end_match(self, timestamp_end: str):
        """Termina el partido."""
        self.status = "finished"
        self.timestamp_end = timestamp_end

    def update_score(self, team: str, goal: int = 1) -> bool:
        """Actualiza el score. Retorna True si fue exitoso."""
        if team == self.team_1:
            self.score_team_1 += goal
            return True
        if team == self.team_2:
            self.score_team_2 += goal
            return True

        print(f"Error: Team {team} not found in match")
        return False

    def to_dict(self) -> dict[str, object]:
        """Convierte Match a diccionario."""
        return {
            "match_id": self.match_id,
            "stadium": self.stadium,
            "climate": self.climate,
            "league": self.league,
            "team_1": self.team_1,
            "team_2": self.team_2,
            "referee": self.referee,
            "timestamp_start": self.timestamp_start,
            "timestamp_end": self.timestamp_end,
            "formation_team_1": self.formation_team_1,
            "formation_team_2": self.formation_team_2,
            "status": self.status,
            "score_team_1": self.score_team_1,
            "score_team_2": self.score_team_2,
        }

    def __str__(self) -> str:
        """Representación legible de Match."""
        return (
            f"Match({self.team_1} vs {self.team_2}, "
            f"score {self.score_team_1}-{self.score_team_2}, "
            f"status={self.status})"
        )
