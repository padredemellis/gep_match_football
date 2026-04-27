from typing import Any
from base import Event

class EventDispatcher:
    def __init__(self) -> None:
        self.handlers: dict[str, list[Any]] = {}

    def subscribe(self, event_type:str, handler: Any):
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
    
    def dispatch(self, event: Event):
        type: str = event.event_type
        if type in self.handlers:
            for handler in self.handlers[type]:
                handler(event)



