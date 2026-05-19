"use client";

import { useCustomerAuth } from "../CustomerAuthProvider";
import { fetchStorefrontApi } from "@/lib/storefront-api";
import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { getStorefrontLink } from "@/lib/storefront-link";

export default function CheckoutPage() {
  const { cart, customer, refreshCart, shopSlug } = useCustomerAuth();
  const router = useRouter();
  const { register, handleSubmit, formState: { isSubmitting } } = useForm();

  const [addresses, setAddresses] = useState<any[]>([]);
  const [selectedAddressId, setSelectedAddressId] = useState<number | 'new' | null>(null);
  const [paymentMethod, setPaymentMethod] = useState("Cash on Delivery");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    if (!customer) {
      router.push(getStorefrontLink('/login', shopSlug));
    } else {
      // Fetch addresses
      fetchStorefrontApi(shopSlug, '/auth/me/').then(async (res) => {
        if (res.ok) {
          const data = await res.json();
          setAddresses(data.addresses || []);
          if (data.addresses && data.addresses.length > 0) {
            setSelectedAddressId(data.addresses[0].id);
          } else {
            setSelectedAddressId('new');
          }
        }
      });
    }
  }, [customer, shopSlug, router]);

  if (!customer) return null;
  if (!cart || cart.items.length === 0) {
    if (!success) router.push(getStorefrontLink('/cart', shopSlug));
    return null;
  }

  const onSubmit = async (data: any) => {
    setError("");
    try {
      const payload = {
        payment_method: paymentMethod,
        address: selectedAddressId === 'new' ? {
          street: data.street,
          city: data.city,
          state: data.state,
          zip_code: data.zip_code
        } : { id: selectedAddressId }
      };

      const res = await fetchStorefrontApi(shopSlug, '/checkout/', {
        method: 'POST',
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        await refreshCart();
        setSuccess(true);
      } else {
        const json = await res.json();
        setError(json.error || "Checkout failed");
      }
    } catch (err) {
      setError("Network error. Please try again.");
    }
  };

  if (success) {
    return (
      <div className="max-w-2xl mx-auto mt-20 p-12 bg-white rounded-3xl shadow-xl shadow-emerald-500/10 border border-slate-100 text-center">
        <div className="w-20 h-20 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg className="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h1 className="text-3xl font-bold font-outfit text-slate-900 mb-4">Order Confirmed!</h1>
        <p className="text-slate-500 mb-8">Thank you for your purchase. We've received your order and it is now being processed.</p>
        <button onClick={() => router.push(getStorefrontLink('/', shopSlug))} className="px-8 py-3 bg-indigo-600 text-white font-medium rounded-xl hover:bg-indigo-500 transition-colors shadow-lg shadow-indigo-500/25">
          Continue Shopping
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-3xl font-bold font-outfit text-slate-900 mb-8">Checkout</h1>

      {error && (
        <div className="mb-8 p-4 bg-red-50 text-red-600 rounded-xl text-sm border border-red-100">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col lg:flex-row gap-8">

        <div className="flex-1 space-y-8">
          {/* Shipping Address */}
          <div className="bg-white p-6 md:p-8 rounded-3xl border border-slate-100 shadow-sm">
            <h2 className="text-xl font-bold font-outfit text-slate-900 mb-6">Shipping Address</h2>

            {addresses.length > 0 && (
              <div className="space-y-4 mb-6">
                {addresses.map((addr) => (
                  <label key={addr.id} className={`flex items-start gap-4 p-4 rounded-xl border cursor-pointer transition-all ${selectedAddressId === addr.id ? 'border-indigo-600 bg-indigo-50/50' : 'border-slate-200 hover:border-indigo-300'}`}>
                    <input type="radio" name="address_selection" checked={selectedAddressId === addr.id} onChange={() => setSelectedAddressId(addr.id)} className="mt-1 text-indigo-600 focus:ring-indigo-500 w-4 h-4" />
                    <div>
                      <p className="font-semibold text-slate-900">{addr.street}</p>
                      <p className="text-slate-500 text-sm">{addr.city}, {addr.state} {addr.zip_code}</p>
                    </div>
                  </label>
                ))}
                <label className={`flex items-center gap-4 p-4 rounded-xl border cursor-pointer transition-all ${selectedAddressId === 'new' ? 'border-indigo-600 bg-indigo-50/50' : 'border-slate-200 hover:border-indigo-300'}`}>
                  <input type="radio" name="address_selection" checked={selectedAddressId === 'new'} onChange={() => setSelectedAddressId('new')} className="text-indigo-600 focus:ring-indigo-500 w-4 h-4" />
                  <span className="font-medium text-slate-900">Ship to a different address</span>
                </label>
              </div>
            )}

            {selectedAddressId === 'new' && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-5 p-6 bg-slate-50 border border-slate-100 rounded-2xl">
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-slate-700 mb-1">Street Address</label>
                  <input type="text" {...register("street", { required: selectedAddressId === 'new' })} className="w-full px-4 py-3 rounded-xl bg-white border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 outline-none" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">City</label>
                  <input type="text" {...register("city", { required: selectedAddressId === 'new' })} className="w-full px-4 py-3 rounded-xl bg-white border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 outline-none" />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">State</label>
                    <input type="text" {...register("state", { required: selectedAddressId === 'new' })} className="w-full px-4 py-3 rounded-xl bg-white border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 outline-none" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">ZIP</label>
                    <input type="text" {...register("zip_code", { required: selectedAddressId === 'new' })} className="w-full px-4 py-3 rounded-xl bg-white border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 outline-none" />
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Payment Method */}
          <div className="bg-white p-6 md:p-8 rounded-3xl border border-slate-100 shadow-sm">
            <h2 className="text-xl font-bold font-outfit text-slate-900 mb-6">Payment Method</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <label className={`flex items-center gap-3 p-4 rounded-xl border cursor-pointer transition-all ${paymentMethod === 'Cash on Delivery' ? 'border-indigo-600 bg-indigo-50/50' : 'border-slate-200 hover:border-indigo-300'}`}>
                <input type="radio" checked={paymentMethod === 'Cash on Delivery'} onChange={() => setPaymentMethod('Cash on Delivery')} className="text-indigo-600 focus:ring-indigo-500 w-4 h-4" />
                <span className="font-semibold text-slate-900">Cash on Delivery</span>
              </label>
              <label className={`flex items-center gap-3 p-4 rounded-xl border cursor-pointer transition-all ${paymentMethod === 'Bank Transfer' ? 'border-indigo-600 bg-indigo-50/50' : 'border-slate-200 hover:border-indigo-300'}`}>
                <input type="radio" checked={paymentMethod === 'Bank Transfer'} onChange={() => setPaymentMethod('Bank Transfer')} className="text-indigo-600 focus:ring-indigo-500 w-4 h-4" />
                <span className="font-semibold text-slate-900">Bank Transfer</span>
              </label>
            </div>
          </div>
        </div>

        {/* Order Summary Sidebar */}
        <div className="lg:w-[400px] shrink-0">
          <div className="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm sticky top-24">
            <h2 className="text-xl font-bold font-outfit text-slate-900 mb-6">Review Order</h2>

            <div className="space-y-4 mb-6 max-h-[300px] overflow-y-auto pr-2">
              {cart.items.map((item) => (
                <div key={item.id} className="flex items-center gap-4">
                  <div className="w-16 h-16 bg-slate-50 rounded-lg shrink-0">
                    {item.product.image_url ? (
                      <img src={item.product.image_url} alt="" className="w-full h-full object-cover rounded-lg" />
                    ) : (
                      <div className="w-full h-full bg-slate-100 rounded-lg" />
                    )}
                  </div>
                  <div className="flex-1">
                    <p className="font-semibold text-slate-900 text-sm line-clamp-1">{item.product.name}</p>
                    <p className="text-xs text-slate-500">Qty: {item.quantity}</p>
                  </div>
                  <div className="font-bold text-slate-900 text-sm">
                    ${((item.product.price * item.quantity) / 100).toFixed(2)}
                  </div>
                </div>
              ))}
            </div>

            <div className="space-y-3 mb-6 pt-6 border-t border-slate-100">
              <div className="flex justify-between text-slate-600 text-sm">
                <span>Subtotal</span>
                <span className="font-medium text-slate-900">${(cart.total_price / 100).toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-slate-600 text-sm">
                <span>Shipping</span>
                <span className="font-medium text-slate-900">Free</span>
              </div>
            </div>

            <div className="border-t border-slate-100 pt-6 mb-8">
              <div className="flex justify-between items-center">
                <span className="text-lg font-bold text-slate-900">Total</span>
                <span className="text-3xl font-extrabold text-slate-900">${(cart.total_price / 100).toFixed(2)}</span>
              </div>
            </div>

            <button type="submit" disabled={isSubmitting} className="block w-full py-4 text-center rounded-xl text-white font-bold bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 disabled:hover:bg-indigo-600 transition-colors shadow-lg shadow-indigo-500/25">
              {isSubmitting ? "Processing..." : "Place Order"}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
