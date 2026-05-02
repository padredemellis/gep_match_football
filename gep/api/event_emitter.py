from gep.events.base import Event

class EventEmitter:
    """
    Handler que actúa como puente entre el EventDispatcher y los clientes WebSocket.
    Se registra como subscriber del dispatcher y envía eventos en tiempo real al WebSocketManager.
    """
    def __init__(self, websocket_manager):
        self.ws_manager = websocket_manager
        self.event_count = 0
    
    def handle_event(self, event: Event):
        """
        Recibe un evento del dispatcher y lo emite a todos los clientes WebSocket a través del manager.
        """
        self.event_count += 1
        
        # event_dict = event.__dict__.copy() # Si tuviera to_dict() usaríamos to_dict.
        # Vamos a asegurar que sea un dict serializable
        try:
            event_data = {k: v for k, v in event.__dict__.items() if not k.startswith('_')}
        except AttributeError:
            event_data = str(event)

        payload = {
            "id": self.event_count,
            "type": event.event_type if hasattr(event, 'event_type') else event.__class__.__name__,
            "timestamp": event.timestamp if hasattr(event, 'timestamp') else None,
            "data": event_data
        }
        
        # Broadcast asíncrono desde un hilo síncrono puede ser un poco tricky,
        # pero WebSocketManager se encargará de poner el mensaje en el event_loop
        self.ws_manager.broadcast_from_sync(payload)
