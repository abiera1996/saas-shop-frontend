export default function DashboardOverview() {
  return (
    <div>
      <h1 className="text-3xl font-outfit font-bold mb-8">Dashboard Overview</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="p-6 rounded-3xl bg-white/5 border border-white/10">
          <p className="text-sm text-slate-400 mb-2">Total Revenue</p>
          <p className="text-4xl font-light">$12,450</p>
          <div className="mt-4 text-emerald-400 text-sm font-medium">+14% from last month</div>
        </div>
        <div className="p-6 rounded-3xl bg-white/5 border border-white/10">
          <p className="text-sm text-slate-400 mb-2">Active Orders</p>
          <p className="text-4xl font-light">34</p>
          <div className="mt-4 text-emerald-400 text-sm font-medium">+2 this week</div>
        </div>
        <div className="p-6 rounded-3xl bg-indigo-500/10 border border-indigo-500/20">
          <p className="text-sm text-indigo-300 mb-2">Store Status</p>
          <p className="text-4xl font-light text-indigo-400">Online</p>
          <div className="mt-4 text-indigo-300/60 text-sm">342 visits today</div>
        </div>
      </div>

      <div className="p-8 rounded-3xl bg-white/5 border border-white/10 min-h-[400px] flex items-center justify-center">
        <p className="text-slate-500">Analytics Chart Placeholder</p>
      </div>
    </div>
  );
}
