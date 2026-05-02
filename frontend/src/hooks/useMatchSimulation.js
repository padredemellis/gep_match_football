import { useState, useCallback, useEffect } from 'react';
import { getCoordinatesForZone, getInitialPosition, PITCH_WIDTH, PITCH_HEIGHT } from '../utils/pitchCoordinates';

// Datos estáticos extraídos de main.py para inicializar
const TEAMS = {
  "penarol": {
    "players": {
      "GK": "Aguerre", "DEF1": "Escobar", "DEF2": "Lemos", "DEF3": "Ferreira", "DEF4": "Olivera",
      "MID1": "Remedi", "MID2": "L. Fernandez", "MID3": "Trindade",
      "FWD1": "Angulo", "FWD2": "M. Fernandez", "FWD3": "Arezo"
    }
  },
  "nacional": {
    "players": {
      "GK": "Mejia", "DEF1": "N. Rodriguez", "DEF2": "Coates", "DEF3": "Rogel", "DEF4": "Candido",
      "MID1": "Boggio", "MID2": "L. Rodriguez", "MID3": "Lodeiro", "MID4": "Barcia",
      "FWD1": "Veron Lupi", "FWD2": "Gomez"
    }
  }
};

export const useMatchSimulation = () => {
  const [players, setPlayers] = useState({});
  const [ball, setBall] = useState({ x: PITCH_WIDTH / 2, y: PITCH_HEIGHT / 2, active: false });

  // Inicializar jugadores en sus posiciones
  useEffect(() => {
    const initialPlayers = {};
    
    ['penarol', 'nacional'].forEach(teamId => {
      Object.entries(TEAMS[teamId].players).forEach(([role, name]) => {
        const pos = getInitialPosition(teamId, role);
        initialPlayers[name] = {
          id: name,
          team: teamId,
          role,
          x: pos.x,
          y: pos.y,
          active: false
        };
      });
    });
    
    setPlayers(initialPlayers);
  }, []);

  const processEvent = useCallback((event) => {
    if (!event || !event.data) return;
    
    const { data, type } = event;
    const isTeam2 = data.team_id === 'nacional';
    
    setPlayers(prev => {
      const next = { ...prev };
      let ballTarget = null;
      
      // Reset active state
      Object.keys(next).forEach(k => next[k].active = false);

      if (type === 'PassEvent') {
        const passer = data.passer_id;
        const receiver = data.receiver_id;
        
        if (next[passer]) {
          const newPos = getCoordinatesForZone(data.location_in_the_field, isTeam2);
          next[passer] = { ...next[passer], ...newPos, active: true };
          ballTarget = newPos;
        }
        
        if (next[receiver]) {
          // El receptor se acerca
          const recvPos = getCoordinatesForZone(data.location_in_the_field, isTeam2);
          next[receiver] = { ...next[receiver], ...recvPos, active: true };
          // El balón viaja al receptor
          ballTarget = recvPos; 
        }

      } else if (type === 'Goal' || type === 'Shot') {
        const shooter = data.player_id || data.shooter_id || data.goal_scorer_id;
        if (next[shooter]) {
          const newPos = getCoordinatesForZone('area_rival', isTeam2);
          next[shooter] = { ...next[shooter], ...newPos, active: true };
          ballTarget = getCoordinatesForZone('propio_arco', !isTeam2); // hacia el arco
        }
      } else if (data.player_id && next[data.player_id]) {
        // Evento general con un jugador
        const newPos = getCoordinatesForZone(data.location_in_the_field, isTeam2);
        next[data.player_id] = { ...next[data.player_id], ...newPos, active: true };
        ballTarget = newPos;
      }

      if (ballTarget) {
        setBall({ ...ballTarget, active: true });
      } else {
        setBall(b => ({ ...b, active: false }));
      }

      return next;
    });
  }, []);

  return { players, ball, processEvent };
};
