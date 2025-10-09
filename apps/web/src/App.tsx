import { useQuery } from "@tanstack/react-query";

import { getHealth } from "./services/healthService";

function App() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["health"],
    queryFn: getHealth
  });

  return (
    <div className="min-h-screen bg-slate-950 text-slate-50 flex items-center justify-center">
      <div className="rounded-lg border border-slate-800 bg-slate-900 p-8 shadow-xl w-full max-w-md text-center space-y-4">
        <h1 className="text-2xl font-semibold">Proficiency Platform</h1>
        <p className="text-sm text-slate-300">
          Full-stack workspace scaffolding is ready to customize.
        </p>
        {isLoading && <p>Checking service health…</p>}
        {error && (
          <p className="text-red-400">
            Unable to reach the API placeholder service.
          </p>
        )}
        {data && (
          <p className="text-emerald-400">
            API status: <strong>{data.status}</strong>
          </p>
        )}
      </div>
    </div>
  );
}

export default App;
