import logging
from typing import Callable, Optional
from gep.events.base import Event

logger = logging.getLogger(__name__)

# Tipo para los handlers: funciones que reciben un Event y no retornan nada
EventHandler = Callable[[Event], None]


class EventDispatcher:
    """
    Dispatcher central de eventos de fútbol.

    Responsabilidades:
        - Registrar handlers (suscripciones) por tipo de evento.
        - Despachar eventos a todos los handlers suscritos.
        - Soportar un wildcard ("*") para handlers que escuchan todos los eventos.
        - Mantener un historial de eventos despachados.
        - Proveer métodos de introspección (listar suscriptores, verificar existencia, etc.).
    """

    WILDCARD = "*"

    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = {}
        self._history: list[Event] = []

    # ------------------------------------------------------------------ #
    #  Suscripción
    # ------------------------------------------------------------------ #

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        """
        Registra un handler para un tipo de evento.

        Args:
            event_type: Tipo de evento (ej. "goal", "foul") o "*" para todos.
            handler: Callable que recibe un Event.
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []

        if handler in self._handlers[event_type]:
            logger.warning(
                f"Handler {handler} ya está suscrito a '{event_type}', se ignora duplicado."
            )
            return

        self._handlers[event_type].append(handler)
        logger.debug(f"Handler {handler} suscrito a '{event_type}'.")

    def subscribe_many(self, event_types: list[str], handler: EventHandler) -> None:
        """
        Registra un mismo handler para múltiples tipos de evento.

        Args:
            event_types: Lista de tipos de evento.
            handler: Callable que recibe un Event.
        """
        for event_type in event_types:
            self.subscribe(event_type, handler)

    # ------------------------------------------------------------------ #
    #  Desuscripción
    # ------------------------------------------------------------------ #

    def unsubscribe(self, event_type: str, handler: EventHandler) -> bool:
        """
        Elimina un handler de un tipo de evento.

        Args:
            event_type: Tipo de evento del que se quiere desuscribir.
            handler: El handler a eliminar.

        Returns:
            True si se eliminó, False si no estaba suscrito.
        """
        if event_type not in self._handlers:
            return False

        try:
            self._handlers[event_type].remove(handler)
            logger.debug(f"Handler {handler} desuscrito de '{event_type}'.")

            # Limpiar la lista si queda vacía
            if not self._handlers[event_type]:
                del self._handlers[event_type]

            return True
        except ValueError:
            return False

    def unsubscribe_all(self, event_type: Optional[str] = None) -> int:
        """
        Elimina todos los handlers de un tipo de evento,
        o de TODOS los tipos si no se especifica.

        Args:
            event_type: Tipo de evento (opcional). Si es None, limpia todo.

        Returns:
            Cantidad de handlers eliminados.
        """
        if event_type is not None:
            handlers = self._handlers.pop(event_type, [])
            count = len(handlers)
        else:
            count = sum(len(h) for h in self._handlers.values())
            self._handlers.clear()

        logger.debug(f"Se eliminaron {count} handler(s) de '{event_type or 'todos los tipos'}'.")
        return count

    # ------------------------------------------------------------------ #
    #  Despacho
    # ------------------------------------------------------------------ #

    def dispatch(self, event: Event) -> int:
        """
        Despacha un evento a todos los handlers registrados para su tipo,
        incluyendo los handlers wildcard ("*").

        Args:
            event: El evento a despachar.

        Returns:
            Cantidad de handlers que procesaron el evento.

        Raises:
            No lanza excepciones propias; los errores de handlers se loguean
            y el despacho continúa con los demás handlers.
        """
        event_type: str = event.event_type
        self._history.append(event)

        handlers: list[EventHandler] = []
        handlers.extend(self._handlers.get(event_type, []))
        handlers.extend(self._handlers.get(self.WILDCARD, []))

        if not handlers:
            logger.debug(f"Evento '{event_type}' despachado sin handlers suscritos.")
            return 0

        count = 0
        for handler in handlers:
            try:
                handler(event)
                count += 1
            except Exception:
                logger.exception(
                    f"Error en handler {handler} al procesar evento '{event_type}' (id={event.event_id})."
                )

        logger.info(f"Evento '{event_type}' (id={event.event_id}) despachado a {count} handler(s).")
        return count

    # ------------------------------------------------------------------ #
    #  Introspección
    # ------------------------------------------------------------------ #

    def has_subscribers(self, event_type: str) -> bool:
        """Retorna True si hay al menos un handler para el tipo dado."""
        return bool(self._handlers.get(event_type))

    def get_subscribers(self, event_type: str) -> list[EventHandler]:
        """
        Retorna una copia de la lista de handlers registrados para un tipo.
        """
        return list(self._handlers.get(event_type, []))

    def get_registered_event_types(self) -> list[str]:
        """Retorna todos los tipos de evento que tienen al menos un handler."""
        return list(self._handlers.keys())

    def subscriber_count(self, event_type: Optional[str] = None) -> int:
        """
        Retorna la cantidad de handlers.

        Args:
            event_type: Si se especifica, cuenta solo los de ese tipo.
                        Si es None, cuenta todos.
        """
        if event_type is not None:
            return len(self._handlers.get(event_type, []))
        return sum(len(h) for h in self._handlers.values())

    # ------------------------------------------------------------------ #
    #  Historial
    # ------------------------------------------------------------------ #

    def get_history(self) -> list[Event]:
        """Retorna una copia del historial de eventos despachados."""
        return list(self._history)

    def get_history_by_type(self, event_type: str) -> list[Event]:
        """Retorna los eventos despachados filtrados por tipo."""
        return [e for e in self._history if e.event_type == event_type]

    def clear_history(self) -> None:
        """Limpia el historial de eventos despachados."""
        self._history.clear()

    # ------------------------------------------------------------------ #
    #  Reset
    # ------------------------------------------------------------------ #

    def reset(self) -> None:
        """Limpia todos los handlers y el historial."""
        self._handlers.clear()
        self._history.clear()
        logger.info("EventDispatcher reseteado.")

    # ------------------------------------------------------------------ #
    #  Representación
    # ------------------------------------------------------------------ #

    def __str__(self) -> str:
        total_handlers = self.subscriber_count()
        total_types = len(self._handlers)
        return (
            f"EventDispatcher("
            f"{total_types} tipo(s) registrado(s), "
            f"{total_handlers} handler(s), "
            f"{len(self._history)} evento(s) despachado(s))"
        )

    def __repr__(self) -> str:
        return (
            f"EventDispatcher(handlers={dict(self._handlers)}, "
            f"history_len={len(self._history)})"
        )
