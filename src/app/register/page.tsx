"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { fetchApi } from "@/lib/api";

export default function RegisterPage() {
  const router = useRouter();
  const [error, setError] = useState("");
  const { register, handleSubmit, formState: { isSubmitting } } = useForm();

  const onSubmit = async (data: any) => {
    setError("");
    try {
      const res = await fetchApi("/auth/register", {
        method: "POST",
        body: JSON.stringify(data),
      });
      
      if (!res.ok) {
        const json = await res.json();
        throw new Error(json.email ? json.email[0] : "Registration failed");
      }
      
      router.push("/login");
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-purple-900/20 via-slate-950 to-slate-950 -z-10" />
      
      <div className="w-full max-w-md p-8 rounded-3xl bg-white/5 border border-white/10 backdrop-blur-xl shadow-2xl">
        <h1 className="text-3xl font-outfit font-bold mb-2">Create Account</h1>
        <p className="text-slate-400 mb-8">Start your multi-tenant journey today.</p>
        
        {error && <div className="p-3 mb-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm">{error}</div>}
        
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-1">Email</label>
            <input 
              type="email" 
              {...register("email", { required: true })}
              className="w-full px-4 py-3 rounded-xl bg-black/30 border border-white/10 focus:border-purple-500 focus:ring-1 focus:ring-purple-500 outline-none transition-all"
              placeholder="merchant@example.com"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-1">Password</label>
            <input 
              type="password" 
              {...register("password", { required: true })}
              className="w-full px-4 py-3 rounded-xl bg-black/30 border border-white/10 focus:border-purple-500 focus:ring-1 focus:ring-purple-500 outline-none transition-all"
              placeholder="••••••••"
            />
          </div>
          
          <button type="submit" disabled={isSubmitting} className="w-full py-3 mt-4 rounded-xl font-medium bg-purple-600 hover:bg-purple-500 disabled:opacity-50 transition-colors shadow-lg shadow-purple-500/25">
            {isSubmitting ? "Creating Account..." : "Sign Up"}
          </button>
        </form>
        
        <p className="mt-6 text-center text-slate-400 text-sm">
          Already have an account? <Link href="/login" className="text-purple-400 hover:text-purple-300 font-medium">Sign in</Link>
        </p>
      </div>
    </div>
  );
}
