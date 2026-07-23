import RepoInput from "./components/RepoInput";

function App() {
  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white">
      <header className="max-w-3xl mx-auto pt-16 pb-8 px-4 text-center">
        <div className="inline-flex items-center justify-center w-10 h-10 rounded-xl bg-orange-500 mb-4">
          <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
        </div>
        <h1 className="text-3xl font-bold tracking-tight">Beacon</h1>
        <p className="text-[#a1a1aa] mt-2 max-w-md mx-auto">
          AI-powered security analysis for public GitHub repositories
        </p>
      </header>
      <main className="max-w-3xl mx-auto px-4 pb-16">
        <RepoInput />
      </main>
    </div>
  );
}

export default App;
