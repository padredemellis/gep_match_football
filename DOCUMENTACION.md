# GEP Match Football - Documentación Completa

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Visión General del Proyecto](#visión-general-del-proyecto)
3. [Arquitectura del Sistema](#arquitectura-del-sistema)
4. [Componentes Principales](#componentes-principales)
5. [Stack Tecnológico](#stack-tecnológico)
6. [Instalación y Setup](#instalación-y-setup)
7. [Uso del Sistema](#uso-del-sistema)
8. [Guía de Desarrollo](#guía-de-desarrollo)
9. [API de Eventos](#api-de-eventos)
10. [Comunicación WebSocket](#comunicación-websocket)
11. [Ejemplos Prácticos](#ejemplos-prácticos)
12. [Roadmap Futuro](#roadmap-futuro)

---

## Introducción

**GEP Match Football** es un simulador de partidos de fútbol en tiempo real desarrollado en **Python** con una arquitectura basada en **Eventos (Event-Driven Architecture)**. El sistema genera eventos estocásticos realistas (pases, tiros, goles, faltas) y los procesa a través de un patrón Pub/Sub, permitiendo que múltiples suscriptores reaccionen a cada evento de forma desacoplada.

El proyecto está diseñado para:
- ✅ Generar simulaciones completas de partidos de fútbol
- ✅ Comunicar eventos en tiempo real vía WebSocket a clientes frontend
- ✅ Mantener estadísticas y narrativa durante la simulación
- ✅ Escalar a una visualización interactiva (frontend React)

---

## Visión General del Proyecto

### Estado Actual (v1.0)
El proyecto es un **simulador backend puro** con:
- Motor de simulación de eventos estocásticos
- Arquitectura Pub/Sub desacoplada
- Servidor WebSocket básico (FastAPI + websockets)
- Soporte para comunicación en tiempo real

### Evolución Planeada
```
Fase 1: Backend + WebSocket (COMPLETADO)
   ↓
Fase 2: Frontend React con Canvas (EN DESARROLLO)
   ↓
Fase 3: Visualización 3D + Estadísticas Avanzadas
   ↓
Fase 4: Múltiples Simulaciones + Almacenamiento de Datos
```

---

## Arquitectura del Sistema

### Diagrama General

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                        │
│            - Cancha Visual (Canvas/WebGL)                   │
│            - Información del Partido                        │
│            - Estadísticas en Vivo                           │
└──────────────────┬──────────────────────────────────────────┘
                   │ WebSocket
                   │ (Eventos en tiempo real)
                   ↓
┌─────────────────────────────────────────────────────────────┐
│                   BACKEND (Python/FastAPI)                  │
│  ┌─────────────────────────────────────────────────────────┐
│  │              WebSocket Server (port 8080)              │
│  │              - Gestión de conexiones                   │
│  │              - Broadcast de eventos                    │
│  └──────────────────────┬────────────────────────────────┘
│                         │
│  ┌──────────────────────↓────────────────────────────────┐
│  │            Match Simulator (gep/main.py)             │
│  │  ┌─────────────────────────────────────────────────┐ │
│  │  │        EventQueue (FIFO)                        │ │
│  │  │  - Almacena eventos generados                   │ │
│  │  │  - Garantiza orden cronológico                  │ │
│  │  └────────────────┬────────────────────────────────┘ │
│  │                   ↓                                   │
│  │  ┌────────────────────────────────────────────────┐  │
│  │  │      EventDispatcher (Pub/Sub)                 │  │
│  │  │  - Registra handlers por tipo de evento        │  │
│  │  │  - Despacha a todos los suscriptores          │  │
│  │  │  - Mantiene historial de eventos              │  │
│  │  └────────┬───────────┬────────────┬─────────────┘  │
│  │           │           │            │                 │
│  │      ┌────↓───┐  ┌────↓───┐ ┌─────↓────┐            │
│  │      │Narrator│  │StatTracker│EventEmitter│         │
│  │      │(Console)│  │(Stats)   │(WebSocket) │         │
│  │      └────────┘  └────────┘ └──────────────┘         │
│  └─────────────────────────────────────────────────────┘
│
│  ┌──────────────────────────────────────────────────────┐
│  │           Componentes de Negocio                     │
│  │  ┌────────────────────────────────────────────────┐ │
│  │  │        Match (Estado del Partido)            │ │
│  │  │  - Marcador                                  │ │
│  │  │  - Tiempo                                    │ │
│  │  │  - Estadio, Árbitro, Formaciones            │ │
│  │  └────────────────────────────────────────────┘ │
│  │                                                   │
│  │  ┌────────────────────────────────────────────┐ │
│  │  │      Eventos (gep/events/)                 │ │
│  │  │  - Goal, PassEvent, Shot, Foul, ...       │ │
│  │  │  - Todos heredan de Event (base class)    │ │
│  │  └────────────────────────────────────────────┘ │
│  └──────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────┘
```

### Flujo de Datos

```
Generación de Eventos
      ↓
┌─────────────────────┐
│   Script Builder    │  build_match_script()
│   (gep/main.py)     │  → minuto + generador
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│   EventQueue        │  inqueue(event)
│   (FIFO)            │  → almacena en orden
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  EventDispatcher    │  dispatch(event)
│  (Pub/Sub)          │  → notifica suscriptores
└──────────┬──────────┘
           │
      ┌────┴────────┬────────────┬──────────────┐
      ↓             ↓            ↓              ↓
  ┌────────┐   ┌────────┐  ┌─────────┐  ┌─────────────┐
  │Narrator│   │StatTrk │  │on_goal  │  │EventEmitter │
  │(print) │   │(stats) │  │(update) │  │(WebSocket)  │
  └────────┘   └────────┘  └─────────┘  └─────────────┘
```

---

## Componentes Principales

### 1. **EventQueue** (`gep/queue/event_queue.py`)

Sistema de cola FIFO para garantizar orden de procesamiento.

**Métodos:**
```python
def inqueue(event: Event) -> None
    # Agrega un evento al final de la cola

def outqueue() -> Event
    # Extrae el primer evento (FIFO)

def is_empty() -> bool
    # Verifica si la cola está vacía

def size() -> int
    # Retorna cantidad de eventos en la cola
```

**Responsabilidades:**
- ✅ Almacenar eventos en orden cronológico
- ✅ Garantizar procesamiento FIFO
- ✅ Prevenir duplicados innecesarios

---

### 2. **EventDispatcher** (`gep/dispatcher/event_dispatcher.py`)

Núcleo del patrón Pub/Sub. Registra handlers y despacha eventos.

**Características:**
```python
def subscribe(event_type: str, handler: EventHandler) -> None
    # Registra un handler para un tipo de evento
    # Soporta wildcard "*" para escuchar todos los eventos

def dispatch(event: Event) -> int
    # Despacha un evento a todos los handlers suscritos
    # Retorna cantidad de handlers que procesaron el evento

def get_history() -> list[Event]
    # Retorna historial de todos los eventos despachados

def get_history_by_type(event_type: str) -> list[Event]
    # Retorna eventos filtrados por tipo
```

**Características Avanzadas:**
- 🎯 Wildcard (`*`) para handlers globales
- 📋 Historial completo de eventos
- 🔍 Introspección (listar suscriptores, verificar tipos)
- 🛡️ Manejo robusto de errores en handlers

---

### 3. **Event System** (`gep/events/`)

Jerarquía de clases que representan todos los eventos posibles.

**Clase Base:**
```python
class Event:
    event_id: str              # ID único del evento
    timestamp: str             # ISO 8601 timestamp
    event_type: str            # Tipo de evento (goal, pass, foul, etc)
    player_id: str             # Jugador involucrado
    team_id: str               # Equipo (penarol, nacional)
    minute: int                # Minuto del partido (0-120)
    game_session_id: str       # ID de sesión del partido
    location_in_the_field: str # Zona del campo
```

**Tipos de Eventos (por categoría):**

| Categoría | Eventos | Archivo |
|-----------|---------|---------|
| **Ataque** | Goal, PassEvent, Shot | `attack.py` |
| **Disciplina** | Foul, YellowCard, RedCard | `discipline.py` |
| **Set Pieces** | FreeKick, CornerKick, ThrowIn, GoalKick | `setpieces.py` |
| **Flujo de Juego** | KickOff, Offside, Substitution, Interception, Dribble | `special.py` |
| **Especiales** | GoalkeeperSave, Injury, VarReview, DisallowedGoal | `game_flow.py` |

**Ejemplo - Evento de Gol:**
```python
class Goal(Event):
    goal_type: str           # "open_play", "header", "free_kick", "volley"
    goal_scorer_id: str      # Quién marcó
    assister_id: Optional[str] # Quién asistió (opcional)
```

---

### 4. **Match** (`gep/match/match.py`)

Entidad que mantiene el estado actual del partido.

**Métodos:**
```python
class Match:
    def start_match()
        # Inicia el partido (status = "ongoing")

    def end_match(timestamp_end: str)
        # Finaliza el partido (status = "finished")

    def update_score(team: str, goal: int = 1) -> bool
        # Actualiza el marcador

    def add_extra_time(minutes: int)
        # Agrega tiempo adicional

    def to_dict() -> dict
        # Serializa el estado del partido
```

**Estado del Partido:**
```python
match_id: str              # ID único
stadium: str               # Estadio
climate: str               # Condiciones climáticas
league: str                # Liga
team_1, team_2: str        # Equipos
referee: str               # Árbitro
formation_team_1, formation_team_2: str # Formaciones (4-3-3, etc)
score_team_1, score_team_2: int    # Marcador
status: str                # "not_started", "ongoing", "finished"
timestamp_start, timestamp_end: str # Tiempos ISO
added_time_minutes: int    # Minutos de descuento
```

---

### 5. **Simulator Core** (`gep/main.py`)

Orquestador principal que configura y ejecuta la simulación.

**Funciones Clave:**

```python
def build_match_script() -> list[tuple[int, callable]]
    # Construye el guion minuto a minuto
    # Retorna lista de (minuto, generador_de_eventos)
    # Ejemplo:
    # - Minuto 0: Kickoff
    # - Minuto 28: Gol de Peñarol
    # - Minuto 55: Gol de Nacional
    # - Minuto 78: Gol de Peñarol (final 3-1)

def run_simulation_async(ws_manager=None)
    # Ejecuta la simulación completa
    # Opcional: envía eventos a WebSocket en tiempo real
```

**Generadores de Eventos:**
```python
generate_kickoff(team_key: str, minute: int)
    → [KickOff event]

generate_passing_sequence(team_key: str, minute: int)
    → [PassEvent, PassEvent, ...]

generate_shot_sequence(team_key: str, minute: int)
    → [PassEvent, ..., Shot, (optional) GoalkeeperSave]

generate_goal_sequence(team_key: str, minute: int, scorer: str)
    → [PassEvent, ..., Goal]

generate_foul_sequence(fouling_team: str, minute: int)
    → [Foul, (optional) YellowCard, FreeKick]

generate_corner_sequence(team_key: str, minute: int)
    → [CornerKick]

generate_misc_event(team_key: str, minute: int)
    → Offside | Interception | Dribble | ThrowIn | GoalKick
```

---

### 6. **WebSocket Server** (`gep/api/server.py`)

Servidor FastAPI + websockets para comunicación en tiempo real.

**Componentes:**

```python
class WebSocketManager:
    def __init__()
        # Inicializa manager
    
    async def connect(websocket)
        # Registra nueva conexión
    
    def disconnect(websocket)
        # Elimina conexión
    
    async def broadcast(message: dict)
        # Envía mensaje a TODOS los clientes conectados
    
    def broadcast_from_sync(message: dict)
        # Wrapper para enviar desde código síncrono
```

**Flujo de Comunicación:**

```
Cliente Frontend
      ↓
WebSocket Connect
      ↓
Handler escucha mensajes
      ↓
Recibe: {"type": "START_SIMULATION"}
      ↓
Lanza run_simulation_async en thread
      ↓
Simulación corre, genera eventos
      ↓
EventEmitter envía eventos vía WebSocket
      ↓
Frontend recibe eventos y visualiza
```

---

### 7. **EventEmitter** (`gep/api/event_emitter.py`)

Puente entre EventDispatcher y WebSocket.

```python
class EventEmitter:
    def __init__(ws_manager)
        # Inicializa con referencia al manager
    
    def handle_event(event: Event)
        # Recibe evento del dispatcher
        # Serializa a JSON
        # Envía a todos los clientes WebSocket
```

**Payload Enviado:**
```json
{
    "id": 42,
    "type": "goal",
    "timestamp": "2026-04-30T21:28:45.123456",
    "data": {
        "event_id": "evt-0042",
        "player_id": "Arezo",
        "team_id": "penarol",
        "minute": 28,
        "goal_type": "open_play",
        "goal_scorer_id": "Arezo",
        "assister_id": "L. Fernandez",
        ...
    }
}
```

---

## Stack Tecnológico

| Componente | Tecnología | Versión | Propósito |
|-----------|-----------|---------|----------|
| **Backend** | Python | 3.9+ | Simulación, lógica de negocio |
| **API** | FastAPI | 0.111.0 | Server HTTP/REST |
| **WebSocket** | websockets | 12.0 | Comunicación en tiempo real |
| **Serialización** | Pydantic | 2.7.1 | Validación de datos |
| **Server** | Uvicorn | 0.29.0 | ASGI app server |
| **Frontend** (Planeado) | React | 18+ | Interfaz de usuario |
| **Visualización** (Planeado) | Canvas/Konva | Latest | Rendering de cancha |

---

## Instalación y Setup

### Requisitos Previos
- Python 3.9 o superior
- pip (gestor de paquetes)
- Git

### Instalación

**1. Clonar el repositorio:**
```bash
git clone https://github.com/padredemellis/gep_match_football.git
cd gep_match_football
```

**2. Crear entorno virtual (recomendado):**
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**3. Instalar dependencias:**
```bash
pip install -r requirements.txt
```

**4. Verificar instalación:**
```bash
python -c "import gep; print('✅ GEP instalado correctamente')"
```

---

## Uso del Sistema

### Ejecución Básica (CLI)

**Ejecutar simulación en consola:**
```bash
python gep/main.py
```

**Salida esperada:**
```
============================================================
GEP - SIMULACION DE PARTIDO DE FUTBOL
============================================================

  Peñarol (4-3-3) vs Nacional (4-4-2)
  Estadio: Estadio Campeón del Siglo | Clima: Noche fresca, 14°C
  Arbitro: Esteban Ostojich
  Sesion: a1b2c3d4...

------------------------------------------------------------
PRIMER TIEMPO
------------------------------------------------------------
      [KICK OFF]  [0'] Event(id=evt-0001, ...)
       [PASE]     [2'] PassEvent(Remedi -> L. Fernandez, ...)
       [TIRO]     [15'] Shot(Arezo, on_target=True, ...)
      [CORNER]    [18'] CornerKick(...)
       [PASE]     [20'] PassEvent(...)

>>> GOOOL DE PEÑAROL !!!  Marca: 1 - 0

...
```

### Ejecución con WebSocket

**Iniciar servidor WebSocket:**
```bash
python gep/main.py
# O directamente:
python gep/api/server.py
```

**Salida:**
```
Iniciando servidor WebSocket en ws://0.0.0.0:8080
Aguardando conexiones de clientes...
```

**Cliente Frontend (JavaScript):**
```javascript
const socket = new WebSocket("ws://localhost:8080");

socket.onopen = () => {
    console.log("✅ Conectado al servidor");
    socket.send(JSON.stringify({ type: "START_SIMULATION" }));
};

socket.onmessage = (event) => {
    const payload = JSON.parse(event.data);
    console.log("Evento:", payload.type, payload.data);
    
    // Visualizar según tipo de evento
    if (payload.type === "goal") {
        updateScore(payload.data);
    } else if (payload.type === "pass") {
        animatePass(payload.data);
    }
};

socket.onerror = (error) => {
    console.error("Error WebSocket:", error);
};
```

---

## Guía de Desarrollo

### Crear un Nuevo Tipo de Evento

**1. Definir la clase en `gep/events/`:**
```python
# gep/events/attack.py
class YourNewEvent(Event):
    def __init__(
        self,
        event_id: str,
        timestamp: str,
        player_id: str,
        team_id: str,
        minute: int,
        game_session_id: str,
        location_in_the_field: str,
        your_custom_field: str,  # Campo personalizado
    ):
        super().__init__(
            event_id=event_id,
            timestamp=timestamp,
            event_type="your_event_type",  # Nombre único
            player_id=player_id,
            team_id=team_id,
            minute=minute,
            game_session_id=game_session_id,
            location_in_the_field=location_in_the_field,
        )
        self.your_custom_field = your_custom_field
    
    def to_dict(self) -> dict:
        data = super().to_dict()
        data["your_custom_field"] = self.your_custom_field
        return data
```

**2. Exportar en `gep/events/__init__.py`:**
```python
from .attack import YourNewEvent  # noqa: F401
```

**3. Usarlo en simulación:**
```python
# gep/main.py
from gep.events import YourNewEvent

def generate_your_event(team_key: str, minute: int) -> list:
    return [
        YourNewEvent(
            event_id=_eid(),
            timestamp=_ts(minute),
            player_id=_pick_player(team_key),
            team_id=_team_id(team_key),
            minute=minute,
            game_session_id=SESSION_ID,
            location_in_the_field=_zone(),
            your_custom_field="value",
        )
    ]
```

**4. Agregar al guion:**
```python
def build_match_script():
    script = []
    
    def evento_custom():
        return generate_your_event("penarol", 30)
    
    script.append((30, evento_custom))
    return script
```

---

### Crear un Handler Custom

```python
# Definir handler
def my_custom_handler(event: Event):
    print(f"✨ Evento personalizado: {event.event_type}")
    print(f"   Jugador: {event.player_id}")
    print(f"   Minuto: {event.minute}")

# Registrar en dispatcher
dispatcher.subscribe("your_event_type", my_custom_handler)

# O para escuchar TODOS los eventos:
dispatcher.subscribe("*", my_custom_handler)
```

---

### Personalizar Equipos y Alineaciones

```python
# gep/main.py
TEAMS = {
    "equipo_custom": {
        "id": "equipo_custom",
        "name": "Mi Equipo",
        "formation": "4-2-3-1",
        "players": {
            "GK": "Arquero",
            "DEF1": "Defensor 1",
            "DEF2": "Defensor 2",
            "DEF3": "Defensor 3",
            "DEF4": "Defensor 4",
            "MID1": "Mediocampista 1",
            "MID2": "Mediocampista 2",
            "FWD1": "Delantero 1",
            "FWD2": "Delantero 2",
            "FWD3": "Delantero 3",
            "SUB1": "Suplente 1",
            "SUB2": "Suplente 2",
        },
    }
}
```

---

## API de Eventos

### Estructura de Mensajes WebSocket

#### 1. Solicitar Inicio de Simulación
```json
{
    "type": "START_SIMULATION"
}
```

#### 2. Evento de Gol
```json
{
    "id": 42,
    "type": "goal",
    "timestamp": "2026-04-30T21:28:45.123456",
    "data": {
        "event_id": "evt-0042",
        "player_id": "Arezo",
        "team_id": "penarol",
        "minute": 28,
        "location_in_the_field": "area_rival",
        "goal_type": "open_play",
        "goal_scorer_id": "Arezo",
        "assister_id": "L. Fernandez"
    }
}
```

#### 3. Evento de Pase
```json
{
    "id": 10,
    "type": "pass",
    "timestamp": "2026-04-30T21:05:30.987654",
    "data": {
        "event_id": "evt-0010",
        "player_id": "Remedi",
        "team_id": "penarol",
        "minute": 5,
        "location_in_the_field": "mediocampo_centro",
        "passer_id": "Remedi",
        "receiver_id": "L. Fernandez",
        "pass_success": true,
        "pass_type": "corto",
        "distance": 12.5
    }
}
```

#### 4. Evento de Falta
```json
{
    "id": 15,
    "type": "foul",
    "timestamp": "2026-04-30T21:12:00.654321",
    "data": {
        "event_id": "evt-0015",
        "player_id": "Coates",
        "team_id": "nacional",
        "minute": 12,
        "location_in_the_field": "defensa_central",
        "fouled_player_id": "Arezo",
        "sanction_type": "falta",
        "sanction_severity": "moderada"
    }
}
```

#### 5. Fin del Partido
```json
{
    "type": "match_finished",
    "data": {
        "stats": {
            "penarol": {"goal": 3, "pass": 125, "foul": 8},
            "nacional": {"goal": 1, "pass": 98, "foul": 12}
        },
        "score_home": 3,
        "score_away": 1,
        "winner": "Peñarol"
    }
}
```

---

## Comunicación WebSocket

### Protocolo de Conexión

```
1. Cliente abre conexión WebSocket
   ws://localhost:8080

2. Server registra conexión
   → "Nuevo cliente conectado. Total: 1"

3. Cliente envía mensaje
   → {"type": "START_SIMULATION"}

4. Server inicia simulación en thread separado
   → Simulación corre sin bloquear el servidor

5. Durante la simulación, cada evento se transmite
   → {"id": 1, "type": "kick_off", "data": {...}}
   → {"id": 2, "type": "pass", "data": {...}}
   → {"id": 3, "type": "goal", "data": {...}}
   ...

6. Simulación termina
   → {"type": "match_finished", "data": {...}}

7. Cliente cierra conexión
   → Server desregistra y limpia
```

### Manejo de Errores

```javascript
socket.onerror = (error) => {
    console.error("Conexión WebSocket perdida:", error);
};

socket.onclose = () => {
    console.warn("Servidor desconectado");
    // Intentar reconectar
    setTimeout(connectWebSocket, 3000);
};
```

---

## Ejemplos Prácticos

### Ejemplo 1: Ejecutar Simulación y Capturar Estadísticas

```python
from gep.main import build_match_script
from gep.dispatcher.event_dispatcher import EventDispatcher
from gep.queue.event_queue import EventQueue
from gep.match.match import Match

# Crear componentes
dispatcher = EventDispatcher()
queue = EventQueue()
match = Match(...)

# Stats tracker personalizado
stats_custom = {}

def track_stats(event):
    key = event.event_type
    stats_custom[key] = stats_custom.get(key, 0) + 1

# Suscribir
dispatcher.subscribe("*", track_stats)

# Ejecutar simulación
script = build_match_script()
for minute, gen_fn in script:
    events = gen_fn()
    for event in events:
        queue.inqueue(event)
    
    while not queue.is_empty():
        evt = queue.outqueue()
        dispatcher.dispatch(evt)

# Mostrar resultados
print("Estadísticas finales:", stats_custom)
```

### Ejemplo 2: Filtrar Eventos por Equipo

```python
def on_penarol_event(event):
    if event.team_id == "penarol":
        print(f"🟡 Evento de Peñarol: {event.event_type}")

dispatcher.subscribe("*", on_penarol_event)
```

### Ejemplo 3: Crear Narración Detallada

```python
class VerboseNarrator:
    def narrate(self, event):
        narrations = {
            "goal": f"⚽ GOOOOOL de {event.player_id}! (min {event.minute}')",
            "pass": f"🎯 Pase de {event.passer_id} a {event.receiver_id}",
            "foul": f"⚠️  Falta de {event.player_id}",
            "yellow_card": f"🟨 Tarjeta amarilla para {event.player_id}",
            "red_card": f"🔴 Tarjeta roja para {event.player_id}",
        }
        
        msg = narrations.get(
            event.event_type,
            f"📝 {event.event_type.upper()}: {event.player_id}"
        )
        print(msg)

narrator = VerboseNarrator()
dispatcher.subscribe("*", narrator.narrate)
```

---

## Roadmap Futuro

### Fase 2: Frontend React (Q2 2026)
- [ ] Crear aplicación React con Vite
- [ ] Implementar Canvas con Konva.js
- [ ] Visualización de cancha 2D
- [ ] Posicionamiento de jugadores en tiempo real
- [ ] Animaciones de pase/gol
- [ ] Panel de información del partido

### Fase 3: Visualización 3D (Q3 2026)
- [ ] Integrar Three.js
- [ ] Modelado 3D de estadio
- [ ] Jugadores 3D animados
- [ ] Cámaras dinámicas
- [ ] Efectos visuales avanzados

### Fase 4: Almacenamiento y Análisis (Q4 2026)
- [ ] Base de datos (PostgreSQL)
- [ ] Persistencia de simulaciones
- [ ] Estadísticas históricas
- [ ] Comparativas entre partidos
- [ ] API REST completa
- [ ] Dashboard analítico

### Fase 5: Multijugador (2027)
- [ ] Múltiples simulaciones simultáneas
- [ ] Replays interactivos
- [ ] Compartir simulaciones
- [ ] Comentarios y análisis colaborativo

---

## Contribuciones

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## Licencia

Este proyecto está bajo la licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## Contacto

Para preguntas, sugerencias o reportes de bugs:
- 📧 Email: padredemellis@github.com
- 🐛 Issues: https://github.com/padredemellis/gep_match_football/issues
- 💬 Discussions: https://github.com/padredemellis/gep_match_football/discussions

---

**Última actualización:** 2 de mayo de 2026  
**Versión:** 1.0 (Beta)  
**Estado:** ✅ Funcional - WebSocket integrado, listo para frontend
