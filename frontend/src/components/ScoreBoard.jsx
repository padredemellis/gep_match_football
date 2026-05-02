import React from 'react';

export const ScoreBoard = ({ scoreHome, scoreAway, minute }) => {
  return (
    <div className="bg-slate-800 rounded-xl shadow-2xl p-6 flex items-center justify-between mx-auto max-w-3xl mb-8 border border-slate-700/50 relative overflow-hidden group">
      <div className="absolute inset-0 bg-gradient-to-r from-yellow-400/10 via-transparent to-white/10 opacity-0 group-hover:opacity-100 transition-opacity duration-700"></div>
      
      {/* Home Team */}
      <div className="flex flex-col items-center gap-2 w-1/3">
        <div className="text-3xl font-black text-yellow-400 uppercase tracking-wider drop-shadow-md">
          Peñarol
        </div>
      </div>

      {/* Score and Minute */}
      <div className="flex flex-col items-center justify-center w-1/3">
        <div className="flex items-center gap-4">
          <span className="text-6xl font-black text-white drop-shadow-[0_0_15px_rgba(250,204,21,0.5)]">{scoreHome}</span>
          <span className="text-2xl font-bold text-slate-500">-</span>
          <span className="text-6xl font-black text-white drop-shadow-[0_0_15px_rgba(255,255,255,0.5)]">{scoreAway}</span>
        </div>
        <div className="mt-2 text-sm font-semibold text-emerald-400 tracking-[0.2em] uppercase animate-pulse">
          {minute > 0 ? `${minute}' MIN` : 'PREVIA'}
        </div>
      </div>

      {/* Away Team */}
      <div className="flex flex-col items-center gap-2 w-1/3">
        <div className="text-3xl font-black text-white uppercase tracking-wider drop-shadow-md">
          Nacional
        </div>
      </div>
    </div>
  );
};
