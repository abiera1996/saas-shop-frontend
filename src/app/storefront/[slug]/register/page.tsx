"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { useCustomerAuth } from "../CustomerAuthProvider";
import { fetchStorefrontApi } from "@/lib/storefront-api";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { getStorefrontLink } from "@/lib/storefront-link";

export default function CustomerRegisterPage() {
  const { register, handleSubmit, formState: { isSubmitting } } = useForm();
  const [error, setError] = useState("");
  const { login, shopSlug } = useCustomerAuth();
  const router = useRouter();

  const onSubmit = async (data: any) => {
    setError("");
    try {
      const res = await fetchStorefrontApi(shopSlug, '/auth/register/', {
        method: "POST",
        body: JSON.stringify(data)
      });
      if (res.ok) {
        const json = await res.json();
        login(json.token, json.customer);
        router.push(getStorefrontLink('/', shopSlug));
      } else {
        const json = await res.json();
        setError(json.error || "Failed to register");
      }
    } catch (err) {
      setError("Network error. Please try again.");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-20 p-8 bg-white rounded-3xl shadow-xl shadow-slate-200/50 border border-slate-100">
      <h1 className="text-2xl font-bold font-outfit text-center mb-2">Create an Account</h1>
      <p className="text-center text-slate-500 mb-8">Join the shop to start purchasing.</p>

      {error && (
        <div className="mb-6 p-4 bg-red-50 text-red-600 rounded-xl text-sm border border-red-100">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Full Name</label>
          <input type="text" {...register("name", { required: true })} className="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:bg-white focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 outline-none transition-all" required />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Email Address</label>
          <input type="email" {...register("email", { required: true })} className="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:bg-white focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 outline-none transition-all" required />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Password</label>
          <input type="password" {...register("password", { required: true, minLength: 6 })} className="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:bg-white focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 outline-none transition-all" required />
        </div>
        <button type="submit" disabled={isSubmitting} className="w-full py-3.5 rounded-xl font-medium text-white bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 transition-colors shadow-lg shadow-indigo-500/25">
          {isSubmitting ? "Creating Account..." : "Create Account"}
        </button>
      </form>

      <p className="mt-6 text-center text-sm text-slate-500">
        Already have an account? <Link href={getStorefrontLink('/login', shopSlug)} className="text-indigo-600 hover:underline font-medium">Sign in</Link>
      </p>
    </div>
  );
}
