"use client";

import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { fetchApi } from "@/lib/api";

export default function CreateShopPage() {
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [isEditing, setIsEditing] = useState(false);
  const [shopId, setShopId] = useState<number | null>(null);
  
  const { register, handleSubmit, setValue, watch, formState: { isSubmitting } } = useForm({
    defaultValues: { name: "", slug: "", description: "", theme_color: "#6366f1" }
  });

  const watchName = watch("name");
  const watchSlug = watch("slug");

  useEffect(() => {
    if (watchName && !watchSlug) {
      setValue("slug", watchName.toLowerCase().replace(/[^a-z0-9]+/g, '-'), { shouldValidate: true, shouldDirty: true });
    }
  }, [watchName, watchSlug, setValue]);

  useEffect(() => {
    fetchApi("/proxy/shops/me/").then(async res => {
      if (res.ok) {
        const data = await res.json();
        setIsEditing(true);
        setShopId(data.id);
        setValue("name", data.name);
        setValue("slug", data.slug);
        setValue("description", data.description);
        setValue("theme_color", data.theme_color);
      }
    });
  }, [setValue]);

  const onSubmit = async (data: any) => {
    setError("");
    setSuccess("");
    try {
      const url = isEditing ? `/proxy/shops/${shopId}` : "/proxy/shops";
      const method = isEditing ? "PUT" : "POST";
      
      const res = await fetchApi(url, {
        method,
        body: JSON.stringify(data),
      });
      
      if (!res.ok) {
        const json = await res.json();
        throw new Error(json.detail || json.name?.[0] || json.slug?.[0] || "Failed to save shop");
      }
      
      const json = await res.json();
      setIsEditing(true);
      setShopId(json.id);
      setSuccess("Shop configuration saved successfully!");
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="max-w-2xl">
      <h1 className="text-3xl font-outfit font-bold mb-2">Shop Configuration</h1>
      <p className="text-slate-400 mb-8">Set up your storefront details and branding.</p>
      
      <div className="p-8 rounded-3xl bg-white/5 border border-white/10">
        {error && <div className="p-3 mb-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm">{error}</div>}
        {success && <div className="p-3 mb-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-sm">{success}</div>}
        
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Shop Name</label>
              <input 
                type="text" 
                {...register("name", { required: true })}
                className="w-full px-4 py-3 rounded-xl bg-black/30 border border-white/10 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition-all"
                placeholder="e.g. Acme Corp"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">URL Slug (Subdomain)</label>
              <div className="flex">
                <input 
                  type="text" 
                  {...register("slug", { 
                    required: true,
                    onChange: (e) => setValue("slug", e.target.value.toLowerCase().replace(/[^a-z0-9\-]+/g, ''))
                  })}
                  className="w-full px-4 py-3 rounded-l-xl bg-black/30 border border-white/10 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition-all text-right"
                  placeholder="acme"
                />
                <span className="inline-flex items-center px-4 rounded-r-xl border border-l-0 border-white/10 bg-black/50 text-slate-400 text-sm">
                  .oursaas.com
                </span>
              </div>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">Description</label>
            <textarea 
              {...register("description")}
              className="w-full px-4 py-3 rounded-xl bg-black/30 border border-white/10 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition-all min-h-[120px]"
              placeholder="Tell your customers about your shop..."
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">Theme Color</label>
            <div className="flex items-center gap-4">
              <input 
                type="color" 
                {...register("theme_color")}
                className="w-14 h-14 rounded-xl cursor-pointer bg-black/30 border border-white/10 p-1"
              />
              <div className="flex-1 px-4 py-3 rounded-xl bg-black/30 border border-white/10 text-slate-300">
                {watch("theme_color")}
              </div>
            </div>
          </div>
          
          <div className="pt-4 border-t border-white/10 flex justify-end">
            <button type="submit" disabled={isSubmitting} className="px-8 py-3 rounded-xl font-medium bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 transition-colors shadow-lg shadow-indigo-500/25">
              {isSubmitting ? "Saving..." : "Save Configuration"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
