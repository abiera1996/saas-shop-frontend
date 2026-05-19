"use client";

import { useCustomerAuth } from "../CustomerAuthProvider";
import { fetchStorefrontApi } from "@/lib/storefront-api";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { getStorefrontLink } from "@/lib/storefront-link";

export default function CartPage() {
  const { cart, customer, refreshCart, shopSlug } = useCustomerAuth();
  const router = useRouter();

  if (!customer) {
    router.push(getStorefrontLink('/login', shopSlug));
    return <div className="p-20 text-center text-slate-500">Redirecting to login...</div>;
  }

  const updateQuantity = async (itemId: number, newQuantity: number) => {
    try {
      await fetchStorefrontApi(shopSlug, `/cart/items/${itemId}/`, {
        method: 'PATCH',
        body: JSON.stringify({ quantity: newQuantity })
      });
      await refreshCart();
    } catch (err) {
      console.error(err);
    }
  };

  const removeItem = async (itemId: number) => {
    try {
      await fetchStorefrontApi(shopSlug, `/cart/items/${itemId}/`, {
        method: 'DELETE'
      });
      await refreshCart();
    } catch (err) {
      console.error(err);
    }
  };

  if (!cart || cart.items.length === 0) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center">
        <div className="w-24 h-24 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg className="w-12 h-12 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
        </div>
        <h2 className="text-2xl font-bold font-outfit text-slate-900 mb-2">Your cart is empty</h2>
        <p className="text-slate-500 mb-8">Looks like you haven't added anything to your cart yet.</p>
        <Link href={getStorefrontLink('/', shopSlug)} className="inline-block px-8 py-3 bg-indigo-600 text-white font-medium rounded-xl hover:bg-indigo-500 transition-colors shadow-lg shadow-indigo-500/25">
          Continue Shopping
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-3xl font-bold font-outfit text-slate-900 mb-8">Shopping Cart</h1>

      <div className="flex flex-col lg:flex-row gap-8">
        <div className="flex-1 space-y-4">
          {cart.items.map((item) => (
            <div key={item.id} className="bg-white p-4 rounded-2xl border border-slate-100 shadow-sm flex items-center gap-6">
              <div className="w-24 h-24 bg-slate-50 rounded-xl flex items-center justify-center shrink-0">
                {item.product.image_url ? (
                  <img src={item.product.image_url} alt={item.product.name} className="w-full h-full object-cover rounded-xl" />
                ) : (
                  <div className="w-8 h-8 rounded-full bg-slate-200" />
                )}
              </div>
              <div className="flex-1">
                <Link href={getStorefrontLink(`/product/${item.product.id}`, shopSlug)} className="font-bold text-slate-900 hover:text-indigo-600 text-lg line-clamp-1">
                  {item.product.name}
                </Link>
                <div className="text-sm font-bold text-slate-500 mt-1">${(item.product.price / 100).toFixed(2)}</div>
              </div>
              <div className="flex items-center gap-4">
                <div className="flex items-center border border-slate-200 rounded-lg bg-slate-50">
                  <button onClick={() => updateQuantity(item.id, item.quantity - 1)} className="px-3 py-1 text-slate-500 hover:bg-slate-100 rounded-l-lg">-</button>
                  <span className="px-3 py-1 font-medium text-slate-900 min-w-[2.5rem] text-center">{item.quantity}</span>
                  <button onClick={() => updateQuantity(item.id, item.quantity + 1)} className="px-3 py-1 text-slate-500 hover:bg-slate-100 rounded-r-lg">+</button>
                </div>
                <button onClick={() => removeItem(item.id)} className="p-2 text-red-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
          ))}
        </div>

        <div className="lg:w-96 shrink-0">
          <div className="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm sticky top-24">
            <h2 className="text-xl font-bold font-outfit text-slate-900 mb-6">Order Summary</h2>
            <div className="space-y-4 mb-6">
              <div className="flex justify-between text-slate-600">
                <span>Subtotal ({cart.items.reduce((a, b) => a + b.quantity, 0)} items)</span>
                <span className="font-medium">${(cart.total_price / 100).toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-slate-600">
                <span>Shipping</span>
                <span className="font-medium">Free</span>
              </div>
            </div>
            <div className="border-t border-slate-100 pt-4 mb-8">
              <div className="flex justify-between items-center">
                <span className="text-lg font-bold text-slate-900">Total</span>
                <span className="text-2xl font-extrabold text-slate-900">${(cart.total_price / 100).toFixed(2)}</span>
              </div>
            </div>
            <Link href={getStorefrontLink('/checkout', shopSlug)} className="block w-full py-4 text-center rounded-xl text-white font-bold bg-indigo-600 hover:bg-indigo-500 transition-colors shadow-lg shadow-indigo-500/25">
              Proceed to Checkout
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
