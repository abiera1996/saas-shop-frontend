"use client";

import Link from "next/link";
import { useCustomerAuth } from "./CustomerAuthProvider";
import { useEffect, useState } from "react";
import { fetchApi } from "@/lib/api";
import { getStorefrontLink } from "@/lib/storefront-link";

export function StorefrontNavbar({ shopSlug }: { shopSlug: string }) {
  const { customer, cart, logout } = useCustomerAuth();
  const [shop, setShop] = useState<any>(null);

  useEffect(() => {
    // Fetch shop details for name/logo
    const loadShop = async () => {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'}/storefront/${shopSlug}/`);
        if (res.ok) {
          setShop(await res.json());
        }
      } catch (err) { }
    };
    loadShop();
  }, [shopSlug]);

  const cartItemsCount = cart?.items.reduce((total, item) => total + item.quantity, 0) || 0;

  return (
    <nav className="bg-white border-b border-slate-200 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <div className="flex items-center gap-4">
            <Link href={getStorefrontLink('/', shopSlug)} className="text-xl font-bold font-outfit" style={{ color: shop?.theme_color || '#000' }}>
              {shop?.name || 'Store'}
            </Link>
          </div>
          <div className="flex items-center gap-6">
            <Link href={getStorefrontLink('/cart', shopSlug)} className="relative text-slate-600 hover:text-slate-900 transition-colors">
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              {cartItemsCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-indigo-600 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full">
                  {cartItemsCount}
                </span>
              )}
            </Link>

            {customer ? (
              <div className="flex items-center gap-4">
                <span className="text-sm font-medium text-slate-700">Hi, {customer.name}</span>
                <button onClick={logout} className="text-sm font-medium text-slate-500 hover:text-red-500 transition-colors">Logout</button>
              </div>
            ) : (
              <div className="flex items-center gap-3">
                <Link href={getStorefrontLink('/login', shopSlug)} className="text-sm font-medium text-slate-600 hover:text-slate-900">Log in</Link>
                <Link href={getStorefrontLink('/register', shopSlug)} className="text-sm font-medium px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-500 transition-colors shadow-md shadow-indigo-500/25">Sign up</Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
