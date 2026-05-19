"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  const links = [
    { name: "Overview", href: "/dashboard" },
    { name: "My Shop", href: "/dashboard/create-shop" },
    { name: "Products", href: "/dashboard/products" },
  ];

  return (
    <div className="min-h-screen flex bg-slate-950">
      {/* Sidebar */}
      <aside className="w-64 border-r border-white/10 bg-black/20 p-6 flex flex-col">
        <div className="mb-10">
          <h2 className="text-xl font-outfit font-bold">Nexus<span className="text-indigo-500">Merchant</span></h2>
        </div>
        
        <nav className="flex-1 space-y-2">
          {links.map((link) => {
            const isActive = pathname === link.href;
            return (
              <Link 
                key={link.name} 
                href={link.href}
                className={`block px-4 py-3 rounded-xl transition-all ${
                  isActive 
                    ? "bg-indigo-500/10 text-indigo-400 font-medium" 
                    : "text-slate-400 hover:bg-white/5 hover:text-slate-200"
                }`}
              >
                {link.name}
              </Link>
            );
          })}
        </nav>
        
        <div className="mt-auto pt-6 border-t border-white/10">
          <Link href="/login" className="flex items-center text-slate-400 hover:text-red-400 transition-colors">
            <svg className="w-5 h-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            Logout
          </Link>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto bg-gradient-to-br from-slate-950 to-slate-900">
        <div className="p-10 max-w-6xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
}
