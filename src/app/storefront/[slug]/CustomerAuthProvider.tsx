"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { fetchStorefrontApi } from "@/lib/storefront-api";

type Customer = {
  id: number;
  email: string;
  name: string;
};

type CartItem = {
  id: number;
  product_id: number;
  product: any;
  quantity: number;
};

type Cart = {
  id: number;
  items: CartItem[];
  total_price: number;
};

type CustomerAuthContextType = {
  customer: Customer | null;
  cart: Cart | null;
  isLoading: boolean;
  shopSlug: string;
  login: (token: string, customerData: Customer) => void;
  logout: () => void;
  refreshCart: () => Promise<void>;
};

const CustomerAuthContext = createContext<CustomerAuthContextType | undefined>(undefined);

export function CustomerAuthProvider({ children, shopSlug }: { children: React.ReactNode, shopSlug: string }) {
  const [customer, setCustomer] = useState<Customer | null>(null);
  const [cart, setCart] = useState<Cart | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const loadSession = async () => {
    const token = localStorage.getItem(`customer_token_${shopSlug}`);
    if (token) {
      try {
        const res = await fetchStorefrontApi(shopSlug, '/auth/me/');
        if (res.ok) {
          const data = await res.json();
          setCustomer(data);
          await refreshCart();
        } else {
          localStorage.removeItem(`customer_token_${shopSlug}`);
        }
      } catch (err) {
        console.error("Failed to load session", err);
      }
    }
    setIsLoading(false);
  };

  const refreshCart = async () => {
    try {
      const res = await fetchStorefrontApi(shopSlug, '/cart/');
      if (res.ok) {
        setCart(await res.json());
      }
    } catch (err) {
      console.error("Failed to load cart", err);
    }
  };

  useEffect(() => {
    loadSession();
  }, [shopSlug]);

  const login = (token: string, customerData: Customer) => {
    localStorage.setItem(`customer_token_${shopSlug}`, token);
    setCustomer(customerData);
    refreshCart();
  };

  const logout = () => {
    localStorage.removeItem(`customer_token_${shopSlug}`);
    setCustomer(null);
    setCart(null);
  };

  return (
    <CustomerAuthContext.Provider value={{ customer, cart, isLoading, shopSlug, login, logout, refreshCart }}>
      {children}
    </CustomerAuthContext.Provider>
  );
}

export function useCustomerAuth() {
  const context = useContext(CustomerAuthContext);
  if (context === undefined) {
    throw new Error("useCustomerAuth must be used within a CustomerAuthProvider");
  }
  return context;
}
