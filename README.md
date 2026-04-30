# GEP (Game Events Provider) - Football Match Simulation

GEP es un simulador de partidos de fútbol desarrollado en Python que utiliza una arquitectura orientada a eventos (Event-Driven Architecture). 

El sistema genera eventos estocásticos (como pases, tiros, goles, faltas) para recrear un partido completo entre dos equipos (por defecto, Peñarol vs Nacional), procesándolos a través de un sistema de colas y despachándolos a distintos *handlers* (narradores en consola, rastreadores de estadísticas, actualizaciones de marcador).

---

## 🏗️ Arquitectura del Sistema

La aplicación está diseñada usando un patrón de Publicador/Suscriptor (Pub/Sub) para desacoplar la generación de los eventos de su procesamiento.

### Diagrama de Flujo Principal

```mermaid
flowchart TD
    subgraph Generación
        A[Script de Simulación / main.py] -->|Crea Eventos| B(Generadores Estocásticos)
        B -->|Produce: Pases, Goles, Faltas| C
    end

    subgraph Procesamiento Core
        C[(EventQueue)] -->|FIFO| D{EventDispatcher}
    end

    subgraph Suscriptores (Handlers)
        D -->|Despacha| E[MatchNarrator]
        D -->|Despacha| F[StatTracker]
        D -->|Despacha| G[Actualizador de Marcador]
    end

    E -.->|Salida Consola| H((Terminal))
    F -.->|Acumula Stats| I((Estadísticas))
```

### Componentes Principales

1. **Eventos (`gep/events/`)**: Estructuras de datos (Data Classes) que representan lo que sucede en el juego (ej: `Goal`, `PassEvent`, `Foul`). Todos heredan de una clase base `Event`.
2. **EventQueue (`gep/queue/event_queue.py`)**: Una cola FIFO que almacena los eventos generados antes de ser procesados, asegurando orden cronológico.
3. **EventDispatcher (`gep/dispatcher/event_dispatcher.py`)**: El motor de Pub/Sub. Permite registrar funciones (handlers) que se ejecutarán cuando ocurra un evento específico o cualquier evento (usando el comodín `*`).
4. **Match (`gep/match/match.py`)**: Entidad que mantiene el estado actual del partido (marcador, tiempo, estadio).
5. **Main (`gep/main.py`)**: Script orquestador que configura los equipos, arma el guion del partido y procesa el bucle principal.

---

## 🚀 Manual de Uso

### Requisitos Previos
- Python 3.9 o superior.
- No requiere dependencias externas (solo usa la biblioteca estándar de Python).

### Ejecución de la Simulación

Para iniciar la simulación del partido, simplemente ejecuta el script principal desde la raíz del proyecto o desde cualquier directorio:

```bash
python gep/main.py
```

*Nota:* El script configura automáticamente el entorno (como el `sys.path` y el encoding a UTF-8) para que se ejecute correctamente en Windows/PowerShell.

### Lo que verás en pantalla
- **Narrativa en vivo**: El partido se narrará minuto a minuto (con una espera de 5 segundos entre eventos) mostrando pases, faltas, tiros y goles con etiquetas claras.
- **Entretiempo y Final**: El partido detecta automáticamente las pausas reglamentarias.
- **Resumen Estadístico**: Al finalizar, se imprimirá un resumen con la posesión, tiros, tarjetas y goles de ambos equipos, seguido de métricas internas del `EventDispatcher`.

---

## 🛠️ Cómo Extender y Personalizar

### 1. Cambiar los Equipos y Alineaciones
Puedes editar el diccionario `TEAMS` dentro de `gep/main.py` para definir nuevos equipos, cambiar los nombres, formaciones y jugadores titulares/suplentes.

### 2. Ajustar el Guion del Partido (Script)
Dentro de `gep/main.py`, la función `build_match_script()` define en qué minuto ocurre qué tipo de secuencia. Puedes agregar o quitar eventos modificando esta lista:
```python
# Ejemplo: Forzar un gol en el minuto 10
def evento_10():
    return generate_goal_sequence("penarol", 10, "Arezo")
script.append((10, evento_10))
```

### 3. Crear Nuevos Tipos de Eventos
1. Crea una clase que herede de `Event` en el paquete `gep.events`.
2. Emite ese evento usando `queue.inqueue()`.
3. Registra un handler específico si deseas lógica particular:
```python
def mi_handler(event):
    print(f"Ocurrió algo nuevo: {event}")

dispatcher.subscribe("mi_nuevo_evento", mi_handler)
```

### 4. Ajustar la Velocidad de Simulación
Para acelerar o ralentizar la salida de la narración, modifica la línea en el bucle principal de `gep/main.py`:
```python
time.sleep(5)  # Cambiar 5 por el número de segundos deseado
```

---

## 📄 Estructura de Directorios

```text
gep_match_football/
├── gep/
│   ├── __init__.py
│   ├── main.py                     # Script principal de simulación
│   ├── dispatcher/
│   │   ├── __init__.py
│   │   └── event_dispatcher.py     # Lógica Pub/Sub
│   ├── events/
│   │   ├── __init__.py
│   │   ├── base.py                 # Clase base Event
│   │   ├── attack.py               # Goles, Tiros, Pases
│   │   ├── discipline.py           # Faltas, Tarjetas
│   │   ├── game_flow.py            # Kickoff, Sustituciones
│   │   ├── setpieces.py            # Tiros libres, Corners
│   │   └── special.py              # VAR, Lesiones
│   ├── match/
│   │   ├── __init__.py
│   │   └── match.py                # Estado del partido
│   └── queue/
│       ├── __init__.py
│       └── event_queue.py          # Cola de eventos
└── README.md                       # Este archivo
```
