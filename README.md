# GEP Match Football (Python)

Modelo de eventos para simulacion de partidos de futbol.

Este proyecto organiza los eventos del partido en modulos, con una clase base comun y clases concretas para cada tipo de accion (goles, faltas, corners, cambios, etc.).

## Estructura

```
gep_python/
├── gep/
│   ├── __init__.py
│   ├── main.py
│   ├── events/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── attack.py
│   │   ├── discipline.py
│   │   ├── setpieces.py
│   │   ├── special.py
│   │   └── game_flow.py
│   └── match/
│       ├── __init__.py
│       └── match.py
├── events.py        # shim de compatibilidad
├── match.py         # shim de compatibilidad
└── main.py          # entrypoint simple
```

## Requisitos

- Python 3.11+ (probado en versiones recientes)

No se requieren dependencias externas.

## Ejecutar demo

Desde la carpeta `gep_python`:

```bash
python main.py
```

O ejecutando el main interno del paquete:

```bash
python -m gep.main
```

## Como funciona

1. `Event` en `gep/events/base.py` define la interfaz comun:
	- `is_valid()`
	- `to_dict()`
	- `__str__()`
2. Cada modulo agrega eventos por dominio:
	- `attack.py`: acciones ofensivas (Goal, Shot, PassEvent, etc.)
	- `discipline.py`: tarjetas y faltas
	- `setpieces.py`: balones parados
	- `special.py`: eventos especiales de flujo de partido
3. `Match` en `gep/match/match.py` modela el estado del partido y score.

## Ejemplo rapido

```python
from gep.events import Goal

goal = Goal(
	 event_id="evt_10",
	 timestamp="2026-04-26T19:05:00Z",
	 player_id="player_9",
	 team_id="team_A",
	 minute=33,
	 game_session_id="match_01",
	 location_in_the_field="penalty_area",
	 goal_type="right_foot",
	 goal_scorer_id="player_9",
	 assister_id="player_8",
)

print(goal.is_valid())
print(goal.to_dict())
```
