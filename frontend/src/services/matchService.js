class MatchService {
  constructor() {
    this.ws = null;
    this.listeners = new Set();
    this.connected = false;
  }

  connect() {
    if (this.ws && (this.ws.readyState === WebSocket.OPEN || this.ws.readyState === WebSocket.CONNECTING)) {
      return;
    }

    this.ws = new WebSocket('ws://localhost:8080');

    this.ws.onopen = () => {
      console.log('Connected to simulation server');
      this.connected = true;
      this.notifyListeners({ type: 'CONNECTION_STATUS', connected: true });
    };

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this.notifyListeners(data);
      } catch (e) {
        console.error("Failed to parse event", e);
      }
    };

    this.ws.onclose = () => {
      console.log('Disconnected from server');
      this.connected = false;
      this.notifyListeners({ type: 'CONNECTION_STATUS', connected: false });
      // Reconnect
      setTimeout(() => this.connect(), 5000);
    };

    this.ws.onerror = (err) => {
      console.error('WebSocket error:', err);
    };
  }

  startSimulation() {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type: 'START_SIMULATION' }));
    }
  }

  subscribe(callback) {
    this.listeners.add(callback);
    return () => this.listeners.delete(callback);
  }

  notifyListeners(data) {
    this.listeners.forEach(listener => listener(data));
  }
}

export const matchService = new MatchService();
