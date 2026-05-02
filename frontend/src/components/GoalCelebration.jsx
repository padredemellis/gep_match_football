import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

export const GoalCelebration = ({ team }) => {
  if (!team) return null;

  const isPenarol = team === 'penarol';
  const bgColor = isPenarol ? 'bg-yellow-400' : 'bg-white';
  const textColor = isPenarol ? 'text-black' : 'text-blue-900';
  const strokeColor = isPenarol ? 'black' : '#e11d48'; // red outline for Nacional

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 1.2 }}
        transition={{ duration: 0.5, type: 'spring' }}
        className="absolute inset-0 z-50 flex items-center justify-center overflow-hidden pointer-events-none"
      >
        {/* Flash background */}
        <motion.div 
          className={`absolute inset-0 ${bgColor} opacity-60`}
          animate={{ opacity: [0.3, 0.6, 0.3] }}
          transition={{ repeat: Infinity, duration: 0.5 }}
        />
        
        {/* Goal Text */}
        <motion.h1
          className={`relative text-9xl font-black italic tracking-tighter uppercase ${textColor} drop-shadow-2xl`}
          initial={{ y: 50, rotate: -5 }}
          animate={{ y: 0, rotate: [-5, 5, -5] }}
          transition={{ repeat: Infinity, duration: 0.4 }}
          style={{ WebkitTextStroke: `4px ${strokeColor}` }}
        >
          ¡GOOOOL!
        </motion.h1>

        {/* Emojis floating */}
        {[...Array(10)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute text-6xl"
            initial={{ 
              x: Math.random() * window.innerWidth - window.innerWidth/2, 
              y: window.innerHeight / 2 
            }}
            animate={{ 
              y: -window.innerHeight,
              rotate: Math.random() * 360
            }}
            transition={{ 
              duration: 2 + Math.random() * 2, 
              repeat: Infinity 
            }}
          >
            {isPenarol ? '🟡⚫' : '⚪🔴🔵'}
          </motion.div>
        ))}
      </motion.div>
    </AnimatePresence>
  );
};
