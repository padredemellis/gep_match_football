import React from 'react';
import { motion } from 'framer-motion';

export const MatchStats = ({ stats, scoreHome, scoreAway, winner }) => {
  if (!stats) return null;

  // Extraer todos los tipos de eventos
  const allEvents = new Set();
  if (stats.penarol) Object.keys(stats.penarol).forEach(e => allEvents.add(e));
  if (stats.nacional) Object.keys(stats.nacional).forEach(e => allEvents.add(e));
  const eventTypes = Array.from(allEvents).sort();

  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      className="absolute inset-0 z-50 flex items-center justify-center p-8 bg-black/80 backdrop-blur-sm"
    >
      <div className="bg-[#1a472a] text-white rounded-2xl shadow-[0_0_50px_rgba(34,197,94,0.3)] w-full max-w-2xl border border-green-500 overflow-hidden">
        
        {/* Header */}
        <div className="bg-[#0f2e1a] p-6 text-center border-b border-green-800">
          <h2 className="text-3xl font-black uppercase text-green-400 mb-2">Final del Partido</h2>
          <div className="flex justify-center items-center gap-8 text-4xl font-bold">
            <span className={winner === 'Peñarol' ? 'text-yellow-400' : ''}>Peñarol {scoreHome}</span>
            <span className="text-gray-400">-</span>
            <span className={winner === 'Nacional' ? 'text-blue-300' : ''}>{scoreAway} Nacional</span>
          </div>
          {winner && <div className="mt-4 text-xl text-yellow-300 font-bold">¡Ganador: {winner}!</div>}
          {!winner && <div className="mt-4 text-xl text-gray-300 font-bold">¡Empate!</div>}
        </div>

        {/* Stats Table */}
        <div className="p-6">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b-2 border-green-700 text-green-300 uppercase text-sm tracking-wider">
                <th className="py-3 px-4 font-semibold">Evento</th>
                <th className="py-3 px-4 font-semibold text-center">Peñarol</th>
                <th className="py-3 px-4 font-semibold text-center">Nacional</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-green-800">
              {eventTypes.map(type => {
                const homeVal = stats.penarol?.[type] || 0;
                const awayVal = stats.nacional?.[type] || 0;
                return (
                  <tr key={type} className="hover:bg-green-800/30 transition-colors">
                    <td className="py-3 px-4 capitalize font-medium text-green-100">{type.replace('_', ' ')}</td>
                    <td className="py-3 px-4 text-center text-lg">{homeVal}</td>
                    <td className="py-3 px-4 text-center text-lg">{awayVal}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

      </div>
    </motion.div>
  );
};
