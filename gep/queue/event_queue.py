from typing import Any, Optional
from gep.events.base import Event


class EventQueue:
    """
    Cola FIFO para almacenar eventos
    """
    def __init__(self) -> None:
        """
        Comenzamos la cola vacía
        """
        self.listEvent: list[Any] = []

    def inqueue(self, event: Event) -> None:
        """Agregamos un evento al final de la cola"""
        self.listEvent.append(event)
        
    
    def outqueue(self) -> Any:
        """
        Saca el primer evento de la cola.
        
        Raises:
            Exception: Si la cola está vacía
        """
        if self.is_empty():
            raise Exception("Cola vacía")
        return self.listEvent.pop(0)
    
    def is_empty(self)-> bool:
        """Retorna True si la cola está vacía."""
        return len(self.listEvent) == 0
    
    def size(self)-> int:
        """Retorna la cantidad de eventos en la cola."""
        return len(self.listEvent)
    
    def __str__(self) -> str:
        """Representación legible de la cola."""
        if self.is_empty():
            return "EventQueue(vacía)"
        return f"EventQueue({self.size()} eventos)"
