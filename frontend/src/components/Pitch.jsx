import React from 'react';
import { Stage, Layer, Rect, Circle, Line } from 'react-konva';
import { motion } from 'framer-motion';
import { PITCH_WIDTH, PITCH_HEIGHT, PADDING } from '../utils/pitchCoordinates';

export const Pitch = ({ players, ball }) => {
  const pitchWidth = PITCH_WIDTH - PADDING * 2;
  const pitchHeight = PITCH_HEIGHT - PADDING * 2;
  
  return (
    <div className="flex justify-center bg-slate-800 p-4 rounded-xl shadow-2xl border border-slate-700/50 relative overflow-hidden">
      
      {/* Background Canvas (Static Pitch) */}
      <Stage width={PITCH_WIDTH} height={PITCH_HEIGHT}>
        <Layer>
          <Rect
            x={PADDING} y={PADDING}
            width={pitchWidth} height={pitchHeight}
            fill="#2f855a" stroke="#ffffff" strokeWidth={3}
            shadowColor="black" shadowBlur={10} shadowOpacity={0.5}
          />
          <Line points={[PITCH_WIDTH / 2, PADDING, PITCH_WIDTH / 2, PITCH_HEIGHT - PADDING]} stroke="#ffffff" strokeWidth={3} />
          <Circle x={PITCH_WIDTH / 2} y={PITCH_HEIGHT / 2} radius={50} stroke="#ffffff" strokeWidth={3} />
          <Circle x={PITCH_WIDTH / 2} y={PITCH_HEIGHT / 2} radius={4} fill="#ffffff" />

          {/* Left Goals */}
          <Rect x={PADDING} y={PITCH_HEIGHT / 2 - 100} width={100} height={200} stroke="#ffffff" strokeWidth={3} />
          <Rect x={PADDING} y={PITCH_HEIGHT / 2 - 40} width={40} height={80} stroke="#ffffff" strokeWidth={3} />
          
          {/* Right Goals */}
          <Rect x={PITCH_WIDTH - PADDING - 100} y={PITCH_HEIGHT / 2 - 100} width={100} height={200} stroke="#ffffff" strokeWidth={3} />
          <Rect x={PITCH_WIDTH - PADDING - 40} y={PITCH_HEIGHT / 2 - 40} width={40} height={80} stroke="#ffffff" strokeWidth={3} />
        </Layer>
      </Stage>

      {/* Dynamic Overlay for Players and Ball using Framer Motion */}
      <div className="absolute top-4 left-4" style={{ width: PITCH_WIDTH, height: PITCH_HEIGHT, pointerEvents: 'none' }}>
        
        {/* Players */}
        {Object.values(players).map((player) => {
          const isPenarol = player.team === 'penarol';
          const imgSrc = isPenarol ? '/assets/chibi_penarol.png' : '/assets/chibi_nacional.png';
          
          return (
            <motion.div
              key={player.id}
              className={`absolute flex flex-col items-center justify-center -ml-6 -mt-10`}
              initial={false}
              animate={{
                x: player.x,
                y: player.y,
                scale: player.active ? 1.2 : 1.0,
                rotate: player.active ? [0, -15, 15, -15, 15, 0] : 0,
                zIndex: player.active ? 50 : 10
              }}
              transition={{ type: 'spring', stiffness: 100, damping: 15 }}
            >
              {/* Highlight Aura for active player */}
              {player.active && (
                <div className={`absolute inset-0 bg-${isPenarol ? 'yellow' : 'white'}-400 rounded-full blur-md opacity-50 w-12 h-12 -z-10`} />
              )}
              
              <img 
                src={imgSrc} 
                alt={player.id} 
                className="w-12 h-12 object-contain drop-shadow-xl" 
                style={{ transform: `scaleX(${isPenarol ? 1 : -1})` }}
              />
              <div className="bg-black/60 text-white text-[10px] font-bold px-1.5 py-0.5 rounded backdrop-blur-sm mt-1 whitespace-nowrap">
                {player.id}
              </div>
            </motion.div>
          );
        })}

        {/* The Ball */}
        <motion.div
          className="absolute -ml-3 -mt-3 z-40"
          initial={false}
          animate={{ x: ball.x, y: ball.y, rotate: ball.active ? 360 : 0 }}
          transition={{ type: 'spring', stiffness: 200, damping: 20 }}
        >
          <img src="/assets/anime_soccer_ball.png" alt="Ball" className="w-6 h-6 object-contain drop-shadow-[0_4px_4px_rgba(0,0,0,0.5)]" />
        </motion.div>

      </div>
    </div>
  );
};
