import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute top-0 left-1/2 w-full -translate-x-1/2 h-[500px] bg-indigo-600/20 blur-[120px] rounded-full pointer-events-none" />
      
      <nav className="container mx-auto px-6 py-6 flex justify-between items-center relative z-10">
        <h1 className="text-2xl font-outfit font-bold tracking-tight">
          Nexus<span className="text-indigo-500">Platform</span>
        </h1>
        <div className="flex gap-4">
          <Link href="/login" className="px-5 py-2.5 rounded-full font-medium hover:bg-white/5 transition-colors">
            Login
          </Link>
          <Link href="/register" className="px-5 py-2.5 rounded-full font-medium bg-white text-black hover:bg-slate-200 transition-colors">
            Start Free
          </Link>
        </div>
      </nav>

      <main className="flex-1 flex flex-col items-center justify-center text-center px-6 relative z-10">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 text-sm font-medium mb-8 border border-indigo-500/20">
          <span className="w-2 h-2 rounded-full bg-indigo-500 animate-pulse" />
          Microservices Architecture Ready
        </div>
        
        <h2 className="text-5xl md:text-7xl font-outfit font-bold tracking-tight max-w-4xl mb-6">
          Scale your storefront with <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-pink-500">infinite power</span>.
        </h2>
        
        <p className="text-lg md:text-xl text-slate-400 max-w-2xl mb-10">
          The ultimate SaaS platform for modern merchants. Built on a modular monolithic core and Next.js, allowing you to deploy dynamic storefronts in seconds.
        </p>

        <div className="flex flex-col sm:flex-row gap-4">
          <Link href="/register" className="px-8 py-4 rounded-full font-medium bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-400 hover:to-purple-500 transition-all shadow-lg shadow-indigo-500/25">
            Create Your Shop
          </Link>
        </div>
      </main>
    </div>
  );
}
