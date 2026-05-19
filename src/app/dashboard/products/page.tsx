"use client";

import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { fetchApi } from "@/lib/api";

export default function ProductsPage() {
  const [showModal, setShowModal] = useState(false);
  const [products, setProducts] = useState<any[]>([]);
  const [shopInfo, setShopInfo] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  const { register, handleSubmit, reset, watch, formState: { isSubmitting } } = useForm();
  
  const categorySelect = watch("category_select");
  const brandSelect = watch("brand_select");

  const loadProducts = async () => {
    try {
      const res = await fetchApi("/proxy/products");
      if (res.ok) {
        const data = await res.json();
        setProducts(data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const loadShopInfo = async () => {
    try {
      const res = await fetchApi("/proxy/shops/me/");
      if (res.ok) {
        setShopInfo(await res.json());
      }
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadProducts();
    loadShopInfo();
  }, []);

  const onSubmit = async (data: any) => {
    setError("");
    const formattedData = {
      ...data,
      price: Math.round(parseFloat(data.price) * 100),
      inventory_count: parseInt(data.inventory_count, 10),
      category: data.category_select === "__new__" ? data.new_category : data.category_select,
      brand: data.brand_select === "__new__" ? data.new_brand : data.brand_select,
    };
    
    delete formattedData.category_select;
    delete formattedData.new_category;
    delete formattedData.brand_select;
    delete formattedData.new_brand;
    
    if (!formattedData.category?.trim()) delete formattedData.category;
    if (!formattedData.brand?.trim()) delete formattedData.brand;

    try {
      const res = await fetchApi("/proxy/products", {
        method: "POST",
        body: JSON.stringify(formattedData),
      });

      if (!res.ok) {
        const json = await res.json();
        throw new Error(json.detail || json.non_field_errors?.[0] || "Failed to add product. Make sure you created a shop first.");
      }

      await loadProducts();
      setShowModal(false);
      reset();
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-outfit font-bold mb-2">Products</h1>
          <p className="text-slate-400">Manage your store's inventory and pricing.</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="px-6 py-3 rounded-xl font-medium bg-indigo-600 hover:bg-indigo-500 transition-colors shadow-lg shadow-indigo-500/25 flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Add Product
        </button>
      </div>

      <div className="bg-white/5 border border-white/10 rounded-3xl overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-black/20 text-slate-400 text-sm border-b border-white/10">
            <tr>
              <th className="px-6 py-4 font-medium">Product Name</th>
              <th className="px-6 py-4 font-medium">Price</th>
              <th className="px-6 py-4 font-medium">Stock Level</th>
              <th className="px-6 py-4 font-medium text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/10">
            {isLoading ? (
              <tr>
                <td colSpan={4} className="px-6 py-8 text-center text-slate-500">
                  Loading products...
                </td>
              </tr>
            ) : products.map((product) => (
              <tr key={product.id} className="hover:bg-white/5 transition-colors">
                <td className="px-6 py-4 font-medium text-slate-200">{product.name}</td>
                <td className="px-6 py-4 text-slate-300">${(product.price / 100).toFixed(2)}</td>
                <td className="px-6 py-4">
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${product.inventory_count > 50 ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                    }`}>
                    {product.inventory_count} in stock
                  </span>
                </td>
                <td className="px-6 py-4 text-right">
                  <button className="text-indigo-400 hover:text-indigo-300 text-sm font-medium mr-4">Edit</button>
                  <button className="text-red-400 hover:text-red-300 text-sm font-medium">Delete</button>
                </td>
              </tr>
            ))}
            {!isLoading && products.length === 0 && (
              <tr>
                <td colSpan={4} className="px-6 py-8 text-center text-slate-500">
                  No products found. Add your first product to get started.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Add Product Modal Placeholder */}
      {showModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-white/10 rounded-3xl w-full max-w-lg overflow-hidden shadow-2xl">
            <div className="p-6 border-b border-white/10 flex justify-between items-center">
              <h3 className="text-xl font-bold font-outfit">Add New Product</h3>
              <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-white">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <form onSubmit={handleSubmit(onSubmit)} className="p-6 space-y-4">
              {error && <div className="p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm">{error}</div>}
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">Name</label>
                <input type="text" {...register("name", { required: true })} className="w-full px-4 py-3 rounded-xl bg-black/30 border border-white/10 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none" required />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Price ($)</label>
                  <input type="number" step="0.01" {...register("price", { required: true })} className="w-full px-4 py-3 rounded-xl bg-black/30 border border-white/10 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none" required />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Stock</label>
                  <input type="number" {...register("inventory_count", { required: true })} className="w-full px-4 py-3 rounded-xl bg-black/30 border border-white/10 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none" required />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Category</label>
                  <select {...register("category_select")} className="w-full px-4 py-3 rounded-xl bg-black/30 border border-white/10 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none mb-2">
                    <option value="">-- Select Category --</option>
                    {shopInfo?.categories?.map((c: any) => <option key={c.id} value={c.name}>{c.name}</option>)}
                    <option value="__new__">+ Add New Category</option>
                  </select>
                  {categorySelect === "__new__" && (
                    <input type="text" {...register("new_category", { required: categorySelect === "__new__" })} placeholder="Enter new category name" className="w-full px-4 py-3 rounded-xl bg-black/30 border border-white/10 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none" />
                  )}
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Brand</label>
                  <select {...register("brand_select")} className="w-full px-4 py-3 rounded-xl bg-black/30 border border-white/10 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none mb-2">
                    <option value="">-- Select Brand --</option>
                    {shopInfo?.brands?.map((b: any) => <option key={b.id} value={b.name}>{b.name}</option>)}
                    <option value="__new__">+ Add New Brand</option>
                  </select>
                  {brandSelect === "__new__" && (
                    <input type="text" {...register("new_brand", { required: brandSelect === "__new__" })} placeholder="Enter new brand name" className="w-full px-4 py-3 rounded-xl bg-black/30 border border-white/10 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none" />
                  )}
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">Description</label>
                <textarea {...register("description")} className="w-full px-4 py-3 rounded-xl bg-black/30 border border-white/10 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none min-h-[100px]" />
              </div>
              <div className="pt-6 flex justify-end gap-3">
                <button type="button" onClick={() => setShowModal(false)} className="px-5 py-2.5 rounded-xl font-medium text-slate-300 hover:text-white hover:bg-white/5 transition-colors">Cancel</button>
                <button type="submit" disabled={isSubmitting} className="px-5 py-2.5 rounded-xl font-medium bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 transition-colors">{isSubmitting ? "Saving..." : "Save Product"}</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
