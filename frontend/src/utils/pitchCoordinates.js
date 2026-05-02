// Dimensions of the pitch in pixels (must match the Konva setup and CSS container)
export const PITCH_WIDTH = 800;
export const PITCH_HEIGHT = 500;
export const PADDING = 20;

export const PITCH_START_X = PADDING;
export const PITCH_END_X = PITCH_WIDTH - PADDING;
export const PITCH_START_Y = PADDING;
export const PITCH_END_Y = PITCH_HEIGHT - PADDING;

export const FIELD_W = PITCH_END_X - PITCH_START_X;
export const FIELD_H = PITCH_END_Y - PITCH_START_Y;

// Zonas en GEP y sus coordenadas relativas [minX, maxX, minY, maxY] (porcentajes 0.0 - 1.0)
// Asumimos que Peñarol ataca de Izquierda a Derecha por defecto (Team 1)
const ZONES_RELATIVE = {
  "propio_arco": [0.0, 0.1, 0.35, 0.65],
  "defensa_central": [0.1, 0.3, 0.3, 0.7],
  "defensa_izquierda": [0.1, 0.3, 0.0, 0.3],
  "defensa_derecha": [0.1, 0.3, 0.7, 1.0],
  "mediocampo_centro": [0.3, 0.7, 0.3, 0.7],
  "mediocampo_izquierda": [0.3, 0.7, 0.0, 0.3],
  "mediocampo_derecha": [0.3, 0.7, 0.7, 1.0],
  "ataque_centro": [0.7, 0.9, 0.3, 0.7],
  "ataque_izquierda": [0.7, 0.9, 0.0, 0.3],
  "ataque_derecha": [0.7, 0.9, 0.7, 1.0],
  "area_rival": [0.9, 1.0, 0.3, 0.7],
};

/**
 * Mapea una zona de GEP a un punto (X,Y) aleatorio dentro de esa zona.
 * @param {string} zone Zona (ej. 'mediocampo_centro')
 * @param {boolean} isTeam2 Si es el equipo 2, invertimos la dirección de ataque
 */
export const getCoordinatesForZone = (zone, isTeam2 = false) => {
  const relative = ZONES_RELATIVE[zone] || ZONES_RELATIVE["mediocampo_centro"];
  
  let [minX, maxX, minY, maxY] = relative;

  if (isTeam2) {
    // Invertir el eje X para el equipo rival (ataca de derecha a izquierda)
    const tempMinX = 1.0 - maxX;
    const tempMaxX = 1.0 - minX;
    minX = tempMinX;
    maxX = tempMaxX;
  }

  // Generar un punto aleatorio en ese rectángulo
  const randomX = minX + Math.random() * (maxX - minX);
  const randomY = minY + Math.random() * (maxY - minY);

  return {
    x: PITCH_START_X + (randomX * FIELD_W),
    y: PITCH_START_Y + (randomY * FIELD_H)
  };
};

/**
 * Posición inicial por defecto para un rol
 */
export const getInitialPosition = (team, role) => {
  const isTeam2 = team === 'nacional';
  // Simples posiciones base para inicializar el equipo antes de que ocurran eventos
  let x = 0.25;
  let y = 0.5;

  if (role === 'GK') { x = 0.05; y = 0.5; }
  else if (role === 'DEF1') { x = 0.2; y = 0.2; }
  else if (role === 'DEF2') { x = 0.2; y = 0.4; }
  else if (role === 'DEF3') { x = 0.2; y = 0.6; }
  else if (role === 'DEF4') { x = 0.2; y = 0.8; }
  else if (role === 'MID1') { x = 0.45; y = 0.3; }
  else if (role === 'MID2') { x = 0.45; y = 0.5; }
  else if (role === 'MID3') { x = 0.45; y = 0.7; }
  else if (role === 'MID4') { x = 0.45; y = 0.5; } // En caso de 4-4-2
  else if (role === 'FWD1') { x = 0.7; y = 0.3; }
  else if (role === 'FWD2') { x = 0.7; y = 0.5; }
  else if (role === 'FWD3') { x = 0.7; y = 0.7; }

  if (isTeam2) x = 1.0 - x;

  return {
    x: PITCH_START_X + (x * FIELD_W),
    y: PITCH_START_Y + (y * FIELD_H)
  };
}
