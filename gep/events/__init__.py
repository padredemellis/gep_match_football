"""
Módulo de eventos para GEP (Game Events Provider).
Exporta todas las clases de eventos.
"""

from .base import Event
from .attack import Goal, PassEvent, Shot, Penalty
from .discipline import Foul, YellowCard, RedCard
from .setpieces import FreeKick, CornerKick, ThrowIn, GoalKick
from .special import (
    KickOff,
    Offside,
    Substitution,
    Interception,
    Dribble,
)
from .game_flow import (
    GoalkeeperSave,
    Injury,
    VarReview,
    DisallowedGoal,
    ExtraTimeOrPenaltyShootout,
)

__all__ = [
    "Event",
    # Attack
    "Goal",
    "PassEvent",
    "Shot",
    "Penalty",
    # Discipline
    "Foul",
    "YellowCard",
    "RedCard",
    # Set Pieces
    "FreeKick",
    "CornerKick",
    "ThrowIn",
    "GoalKick",
    # Special
    "KickOff",
    "Offside",
    "Substitution",
    "Interception",
    "Dribble",
    # Game Flow
    "GoalkeeperSave",
    "Injury",
    "VarReview",
    "DisallowedGoal",
    "ExtraTimeOrPenaltyShootout",
]