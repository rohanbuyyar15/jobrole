import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';

export default function Result() {
  const [data, setData] = useState(null);
  const router = useRouter();

  useEffect(() => {
    const raw = localStorage.getItem('resumeResult');
    if (raw) {
      setData(JSON.parse(raw));
    } else {
      router.push('/');
    }
  }, [router]);

  if (!data) return <div className="min-h-screen flex items-center justify-center p-4 text-white text-3xl font-extrabold animate-pulse">Analyzing...</div>;

  return (
    <div className="min-h-screen p-6 md:p-12 text-white">
      <div className="max-w-6xl mx-auto space-y-8 animate-fade-in-up">
        
        <header className="flex justify-between items-center glass-panel p-6 shadow-2xl">
          <h1 className="text-3xl font-extrabold tracking-tight drop-shadow-md">Analysis Results</h1>
          <button onClick={() => router.push('/')} className="bg-white/20 hover:bg-white/30 text-white px-6 py-2 rounded-lg font-bold transition-all shadow-lg hover:shadow-xl hover:-translate-y-0.5">
            Upload Another
          </button>
        </header>

        <div className="grid md:grid-cols-3 gap-8">
          
          {/* Top Roles */}
          <div className="glass-panel p-8 md:col-span-2 shadow-2xl transition-transform hover:scale-[1.01]">
            <h2 className="text-2xl font-bold mb-6 border-b border-white/20 pb-2">Predicted Roles</h2>
            <div className="space-y-4">
              {data.roles?.map((role, idx) => (
                <div key={idx} className="bg-white/10 rounded-xl p-5 flex items-center justify-between hover:bg-white/20 transition-all border border-transparent hover:border-white/30 shadow-md">
                  <span className="text-xl font-bold tracking-wide">{role.name}</span>
                  <div className="flex items-center gap-4">
                    <span className="text-lg font-extrabold bg-blue-500/30 px-3 py-1 rounded-full">{role.score}%</span>
                    <div className="w-24 md:w-40 h-4 bg-gray-800 rounded-full overflow-hidden shadow-inner flex items-center p-0.5">
                      <div className="h-full bg-gradient-to-r from-blue-400 to-indigo-400 rounded-full" style={{ width: `${role.score}%` }}></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Match Score */}
          <div className="glass-panel p-8 text-center flex flex-col justify-center items-center shadow-2xl transition-transform hover:scale-[1.02]">
            <h2 className="text-2xl font-bold mb-6">Top Match Score</h2>
            <div className="relative w-48 h-48 drop-shadow-2xl">
              <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                <path className="text-white/10" strokeWidth="3" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                <path className="text-green-400 drop-shadow-lg" strokeDasharray={`${data.match_score}, 100`} strokeWidth="3" strokeLinecap="round" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-br from-green-300 to-green-500 drop-shadow-md">
                  {data.match_score}%
                </span>
              </div>
            </div>
          </div>

        </div>

        <div className="grid md:grid-cols-2 gap-8">
          
          {/* Missing Skills */}
          <div className="glass-panel p-8 shadow-2xl transition-transform hover:scale-[1.01]">
            <h2 className="text-2xl font-bold mb-6 border-b border-white/20 pb-2 flex items-center gap-3">
              <svg className="w-7 h-7 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
              Missing Skills
            </h2>
            <div className="flex flex-wrap gap-3">
              {data.missing_skills?.length > 0 ? data.missing_skills.map((skill, idx) => (
                <span key={idx} className="px-5 py-2.5 bg-red-500/20 text-red-100 border border-red-400/50 rounded-full font-bold shadow-md hover:bg-red-500/30 transition-colors">
                  {skill.toUpperCase()}
                </span>
              )) : (
                <span className="text-green-300 font-bold bg-green-500/20 px-4 py-2 rounded-lg border border-green-500/40">No missing critical skills detected! Great job!</span>
              )}
            </div>
          </div>

          {/* Suggestions */}
          <div className="glass-panel p-8 shadow-2xl transition-transform hover:scale-[1.01]">
            <h2 className="text-2xl font-bold mb-6 border-b border-white/20 pb-2 flex items-center gap-3">
              <svg className="w-7 h-7 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
              Suggestions
            </h2>
            <ul className="space-y-4">
              {data.suggestions?.map((sg, idx) => (
                <li key={idx} className="flex items-start gap-4 bg-white/5 p-4 rounded-xl border border-white/10 hover:bg-white/10 transition-colors shadow-sm">
                  <div className="mt-1.5 flex-shrink-0 w-3 h-3 bg-gradient-to-br from-yellow-300 to-yellow-500 rounded-full shadow-md"></div>
                  <span className="text-gray-100 font-medium leading-relaxed">{sg}</span>
                </li>
              ))}
            </ul>
          </div>
          
        </div>

        {/* Roadmap */}
        <div className="glass-panel p-8 shadow-2xl mb-8">
          <h2 className="text-2xl font-bold mb-10 border-b border-white/20 pb-2 flex items-center gap-3">
            <svg className="w-7 h-7 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"></path></svg>
            Career Roadmap
          </h2>
          <div className="space-y-6 relative before:absolute before:inset-0 before:ml-6 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-1 before:bg-gradient-to-b before:from-blue-400 before:via-indigo-500 before:to-purple-500 before:rounded-full">
            {data.roadmap?.map((step, idx) => (
              <div key={idx} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                <div className="flex items-center justify-center w-12 h-12 rounded-full border-4 border-[#1e3c72] bg-gradient-to-br from-blue-400 to-indigo-600 text-white shadow-xl shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10 font-black text-xl">
                  {idx + 1}
                </div>
                <div className="w-[calc(100%-4rem)] md:w-[calc(50%-3rem)] bg-white/10 p-6 rounded-2xl border border-white/20 shadow-xl hover:scale-[1.02] transition-transform backdrop-blur-md">
                  <h3 className="font-bold text-lg text-blue-100">{step}</h3>
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
}
