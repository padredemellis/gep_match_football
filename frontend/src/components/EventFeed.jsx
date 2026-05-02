import React, { useEffect, useRef } from 'react';
import { Activity, Goal, FileWarning, MoveRight, Hand } from 'lucide-react';

const getIcon = (type) => {
  switch (type) {
    case 'Goal': return <Goal className="w-5 h-5 text-green-400" />;
    case 'Foul': return <Hand className="w-5 h-5 text-orange-400" />;
    case 'YellowCard': return <FileWarning className="w-5 h-5 text-yellow-400" />;
    case 'RedCard': return <FileWarning className="w-5 h-5 text-red-500" />;
    case 'PassEvent': return <MoveRight className="w-5 h-5 text-blue-400" />;
    case 'Shot': return <Activity className="w-5 h-5 text-purple-400" />;
    default: return <Activity className="w-5 h-5 text-slate-400" />;
  }
};

export const EventFeed = ({ events }) => {
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [events]);

  return (
    <div className="bg-slate-800/80 backdrop-blur-md rounded-xl p-4 shadow-xl border border-slate-700 h-[400px] flex flex-col">
      <h3 className="text-lg font-bold mb-4 text-slate-200 border-b border-slate-700 pb-2 flex items-center gap-2">
        <Activity className="w-5 h-5" />
        Feed de Eventos
      </h3>
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto space-y-3 pr-2 scrollbar-thin scrollbar-thumb-slate-600 scrollbar-track-transparent"
      >
        {events.map((ev, i) => (
          <div 
            key={i} 
            className="flex items-start gap-3 p-3 bg-slate-900/50 rounded-lg hover:bg-slate-700/50 transition-colors border border-slate-800/50"
          >
            <div className="mt-1">
              {getIcon(ev.type)}
            </div>
            <div className="flex-1">
              <div className="flex justify-between items-center">
                <span className="font-bold text-slate-300 text-sm">{ev.type}</span>
                <span className="text-xs text-emerald-400 font-mono">{ev.data.minute}'</span>
              </div>
              <p className="text-sm text-slate-400 mt-1">
                {ev.data.player_id && <span className="text-slate-200 font-medium">{ev.data.player_id}</span>}
                {ev.data.passer_id && <span>Pase de {ev.data.passer_id} a {ev.data.receiver_id}</span>}
                {ev.data.goal_scorer_id && <span>Gol de {ev.data.goal_scorer_id}</span>}
                {ev.data.sanction_type && <span> ({ev.data.sanction_severity})</span>}
                {!ev.data.player_id && !ev.data.passer_id && !ev.data.goal_scorer_id && <span className="text-xs">Evento general</span>}
              </p>
            </div>
          </div>
        ))}
        {events.length === 0 && (
          <div className="text-slate-500 text-center h-full flex items-center justify-center italic">
            Esperando eventos...
          </div>
        )}
      </div>
    </div>
  );
};
