"use client";

import { useEffect, useState, use } from "react";
import { fetchStorefrontApi } from "@/lib/storefront-api";
import { useCustomerAuth } from "../../CustomerAuthProvider";
import { useRouter } from "next/navigation";
import { getStorefrontLink } from "@/lib/storefront-link";

export default function ProductDetailsPage({ params }: { params: Promise<{ slug: string, id: string }> }) {
  console.log("--- COMPONENT START ---");
  const { slug, id } = use(params);
  const [product, setProduct] = useState<any>(null);
  const [shop, setShop] = useState<any>(null);
  const [quantity, setQuantity] = useState(1);
  const [isAdding, setIsAdding] = useState(false);
  const { customer, refreshCart, shopSlug } = useCustomerAuth();
  const router = useRouter();

  const targetSlug = shopSlug || slug;

  console.log("ProductDetailsPage Render:", {
    slug,
    shopSlug,
    targetSlug,
    id,
    apiBaseUrlEnv: process.env.NEXT_PUBLIC_API_URL
  });

  useEffect(() => {
    console.log("qwqgqw")
    const loadData = async () => {
      console.log("aswwwwdasd", targetSlug)
      if (!targetSlug || targetSlug === 'undefined') return;


      try {
        const apiBase = typeof window !== 'undefined'
          ? (process.env.NEXT_PUBLIC_API_URL || '/api/proxy')
          : (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api');
        console.log("asdasd", apiBase)
        const shopRes = await fetch(`${apiBase}/storefront/${targetSlug}/`);
        if (shopRes.ok) setShop(await shopRes.json());

        const productRes = await fetch(`${apiBase}/storefront/${targetSlug}/products/${id}/`);
        if (productRes.ok) setProduct(await productRes.json());
      } catch (err) { }
    };
    loadData();
  }, [targetSlug, id]);

  const handleAddToCart = async () => {
    if (!customer) {
      router.push(getStorefrontLink('/login', targetSlug));
      return;
    }

    setIsAdding(true);
    try {
      const res = await fetchStorefrontApi(targetSlug, '/cart/items/', {
        method: 'POST',
        body: JSON.stringify({ product_id: product.id, quantity })
      });
      if (res.ok) {
        await refreshCart();
        // Maybe show a success toast here
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsAdding(false);
    }
  };

  if (!product || !shop) return <div className="p-20 text-center text-slate-500">Loading...</div>;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="bg-white rounded-3xl shadow-sm border border-slate-100 overflow-hidden flex flex-col md:flex-row">

        {/* Product Image */}
        <div className="md:w-1/2 aspect-square bg-slate-50 flex items-center justify-center p-8">
          {product.image_url ? (
            <img src={product.image_url} alt={product.name} className="max-w-full max-h-full object-contain rounded-2xl shadow-lg" />
          ) : (
            <div className="w-32 h-32 rounded-full opacity-20" style={{ backgroundColor: shop.theme_color }} />
          )}
        </div>

        {/* Product Info */}
        <div className="md:w-1/2 p-8 md:p-12 flex flex-col">
          <div className="text-sm font-bold uppercase tracking-wider text-slate-400 mb-2">
            {product.brand && product.category ? `${product.brand} • ${product.category}` : product.brand || product.category}
          </div>
          <h1 className="text-3xl md:text-4xl font-bold font-outfit text-slate-900 mb-4">{product.name}</h1>

          <div className="text-3xl font-extrabold text-slate-900 mb-6">
            ${(product.price / 100).toFixed(2)}
          </div>

          <div className="prose prose-slate mb-8 flex-1">
            <p>{product.description}</p>
          </div>

          <div className="mt-auto border-t border-slate-100 pt-8">
            <div className="flex items-center gap-4 mb-6">
              <span className="font-semibold text-slate-700">Quantity</span>
              <div className="flex items-center border border-slate-200 rounded-lg bg-slate-50">
                <button
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  className="px-4 py-2 text-slate-500 hover:text-slate-700 hover:bg-slate-100 rounded-l-lg transition-colors"
                >-</button>
                <span className="px-4 py-2 font-medium text-slate-900 min-w-[3rem] text-center">{quantity}</span>
                <button
                  onClick={() => setQuantity(Math.min(product.inventory_count, quantity + 1))}
                  className="px-4 py-2 text-slate-500 hover:text-slate-700 hover:bg-slate-100 rounded-r-lg transition-colors"
                >+</button>
              </div>
              <span className="text-sm text-slate-400">{product.inventory_count} available in stock</span>
            </div>

            <button
              onClick={handleAddToCart}
              disabled={isAdding || product.inventory_count === 0}
              className="w-full py-4 rounded-xl text-white font-bold text-lg shadow-lg hover:shadow-xl transition-all active:scale-95 disabled:opacity-50 disabled:active:scale-100 flex justify-center items-center gap-2"
              style={{ backgroundColor: shop.theme_color }}
            >
              {isAdding ? "Adding..." : "Add to Cart"}
            </button>
            {!customer && (
              <p className="text-center text-sm text-slate-500 mt-3">You will be prompted to log in to add items to your cart.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
