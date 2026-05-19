"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { fetchApi } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [error, setError] = useState("");
  const { register, handleSubmit, formState: { isSubmitting } } = useForm();

  const onSubmit = async (data: any) => {
    setError("");
    try {
      const res = await fetchApi("/auth/login", {
        method: "POST",
        body: JSON.stringify(data),
      });
      
      const json = await res.json();
      if (!res.ok) throw new Error(json.detail || "Invalid credentials");
      
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-indigo-900/20 via-slate-950 to-slate-950 -z-10" />
      
      <div className="w-full max-w-md p-8 rounded-3xl bg-white/5 border border-white/10 backdrop-blur-xl shadow-2xl">
        <h1 className="text-3xl font-outfit font-bold mb-2">Welcome back</h1>
        <p className="text-slate-400 mb-8">Sign in to your merchant dashboard</p>
        
        {error && <div className="p-3 mb-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm">{error}</div>}
        
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-1">Email</label>
            <input 
              type="email" 
              {...register("email", { required: true })}
              className="w-full px-4 py-3 rounded-xl bg-black/30 border border-white/10 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition-all"
              placeholder="merchant@example.com"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-1">Password</label>
            <input 
              type="password" 
              {...register("password", { required: true })}
              className="w-full px-4 py-3 rounded-xl bg-black/30 border border-white/10 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition-all"
              placeholder="••••••••"
            />
          </div>
          
          <button type="submit" disabled={isSubmitting} className="w-full py-3 mt-4 rounded-xl font-medium bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 transition-colors shadow-lg shadow-indigo-500/25">
            {isSubmitting ? "Signing in..." : "Sign In"}
          </button>
        </form>
        
        <p className="mt-6 text-center text-slate-400 text-sm">
          Don't have an account? <Link href="/register" className="text-indigo-400 hover:text-indigo-300 font-medium">Create one</Link>
        </p>
      </div>
    </div>
  );
}
