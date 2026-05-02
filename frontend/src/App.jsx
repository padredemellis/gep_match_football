import { useEffect, useState } from 'react'
import { matchService } from './services/matchService'
import { ScoreBoard } from './components/ScoreBoard'
import { Pitch } from './components/Pitch'
import { EventFeed } from './components/EventFeed'
import { useMatchSimulation } from './hooks/useMatchSimulation'
import { GoalCelebration } from './components/GoalCelebration'
import { MatchStats } from './components/MatchStats'

function App() {
  const [connected, setConnected] = useState(false);
  const [events, setEvents] = useState([]);
  const [matchState, setMatchState] = useState({
    minute: 0,
    scoreHome: 0,
    scoreAway: 0
  });

  const [goalCelebrationTeam, setGoalCelebrationTeam] = useState(null);
  const [matchStatsData, setMatchStatsData] = useState(null);

  const { players, ball, processEvent } = useMatchSimulation();

  useEffect(() => {
    const unsubscribe = matchService.subscribe((data) => {
      if (data.type === 'CONNECTION_STATUS') {
        setConnected(data.connected);
        return;
      }

      // Add event to feed
      if (data.type) {
        setEvents(prev => [...prev, data]);
        processEvent(data);
        
        // Update minute
        if (data.data && data.data.minute !== undefined) {
          setMatchState(prev => ({ ...prev, minute: data.data.minute }));
        }

        // Simplistic score tracking based on Goal events
        if ((data.type === 'Goal' || data.type === 'goal') && data.data) {
          const team = data.data.team_id;
          if (team === 'penarol') {
            setMatchState(prev => ({ ...prev, scoreHome: prev.scoreHome + 1 }));
            setGoalCelebrationTeam('penarol');
          } else if (team === 'nacional') {
            setMatchState(prev => ({ ...prev, scoreAway: prev.scoreAway + 1 }));
            setGoalCelebrationTeam('nacional');
          }
          
          // Clear celebration after 4 seconds
          setTimeout(() => {
            setGoalCelebrationTeam(null);
          }, 4000);
        }

        // Handle match finished event
        if (data.type === 'match_finished' && data.data) {
          setMatchStatsData(data.data);
        }
      }
    });

    matchService.connect();

    return () => {
      unsubscribe();
    };
  }, []);

  const handleStartSimulation = () => {
    matchService.startSimulation();
  };

  return (
    <div className="min-h-screen bg-slate-900 p-8 text-white relative">
      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Header & Controls */}
        <div className="flex justify-between items-center bg-slate-800/50 p-4 rounded-xl border border-slate-700/50">
          <div className="flex items-center gap-3">
            <div className={`w-3 h-3 rounded-full ${connected ? 'bg-green-500 shadow-[0_0_10px_#22c55e]' : 'bg-red-500'}`}></div>
            <span className="font-semibold text-slate-300">
              {connected ? 'Conectado al Backend' : 'Desconectado'}
            </span>
          </div>
          
          <button 
            onClick={handleStartSimulation}
            disabled={!connected}
            className="flex items-center gap-2 bg-gradient-to-r from-yellow-500 to-amber-600 hover:from-yellow-400 hover:to-amber-500 disabled:opacity-50 disabled:cursor-not-allowed text-white px-6 py-3 rounded-lg font-bold shadow-lg transform transition hover:scale-105 active:scale-95"
          >
            {/* SVG Whistle Icon */}
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14 2h-4"/><path d="M12 2v2"/><path d="M10 4a4 4 0 0 0 0 8 4 4 0 0 0 0-8z"/><path d="M14 8c0 2.2-1.8 4-4 4-2.2 0-4-1.8-4-4"/><path d="M21 15v5a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/><path d="M12 13v9"/></svg>
            Tocar Silbato (Iniciar)
          </button>
        </div>

        <ScoreBoard 
          scoreHome={matchState.scoreHome} 
          scoreAway={matchState.scoreAway} 
          minute={matchState.minute} 
        />

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <Pitch players={players} ball={ball} />
          </div>
          <div>
            <EventFeed events={events} />
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
