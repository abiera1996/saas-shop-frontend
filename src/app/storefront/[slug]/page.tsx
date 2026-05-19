import { notFound } from "next/navigation";
import Link from "next/link";
import { getStorefrontLink } from "@/lib/storefront-link";

// Force Server-Side Rendering (SSR) for this page on every request
export const dynamic = "force-dynamic";

export default async function StorefrontPage({
  params,
  searchParams,
}: {
  params: Promise<{ slug: string }>;
  searchParams: Promise<{ q?: string; category?: string; brand?: string; min_price?: string; max_price?: string; min_rating?: string }>;
}) {
  // Await the params and searchParams objects
  const { slug } = await params;
  const searchParamsData = await searchParams;
  const { q, category, brand, min_price, max_price, min_rating } = searchParamsData;

  const DJANGO_API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

  // Fetch shop details via SSR
  const shopRes = await fetch(`${DJANGO_API_URL}/storefront/${slug}/`);

  if (!shopRes.ok) {
    return notFound();
  }

  const shop = await shopRes.json();

  // Fetch shop products with optional search queries via SSR
  const queryParams = new URLSearchParams();
  if (q) queryParams.append('q', q);
  if (category) queryParams.append('category', category);
  if (brand) queryParams.append('brand', brand);
  if (min_price) queryParams.append('min_price', min_price);
  if (max_price) queryParams.append('max_price', max_price);
  if (min_rating) queryParams.append('min_rating', min_rating);

  const queryString = queryParams.toString();
  const productsUrl = `${DJANGO_API_URL}/storefront/${slug}/products/${queryString ? `?${queryString}` : ''}`;

  const productsRes = await fetch(productsUrl);
  const products = productsRes.ok ? await productsRes.json() : [];

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 transition-colors duration-500" style={{ '--theme-color': shop.theme_color } as React.CSSProperties}>
      {/* Header */}
      <header className="py-8 border-b bg-white" style={{ borderColor: `${shop.theme_color}30` }}>
        <div className="container mx-auto px-6 text-center">
          <h1 className="text-4xl md:text-5xl font-bold font-outfit" style={{ color: shop.theme_color }}>
            {shop.name}
          </h1>
          <p className="mt-4 text-slate-600 max-w-2xl mx-auto">{shop.description}</p>

          {/* Pure SSR Search Bar - utilizes GET action to naturally trigger SSR on submission */}
          <form action="" method="GET" className="max-w-md mx-auto mt-6">
            {/* Preserve other filters when searching */}
            {category && <input type="hidden" name="category" value={category} />}
            {brand && <input type="hidden" name="brand" value={brand} />}
            {min_price && <input type="hidden" name="min_price" value={min_price} />}
            {max_price && <input type="hidden" name="max_price" value={max_price} />}
            {min_rating && <input type="hidden" name="min_rating" value={min_rating} />}

            <div className="relative">
              <input
                type="text"
                name="q"
                placeholder="Search products..."
                defaultValue={q || ''}
                className="w-full pl-12 pr-4 py-3 rounded-full bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-[var(--theme-color)] focus:border-transparent shadow-sm text-slate-800 transition-all"
                style={{ '--tw-ring-color': shop.theme_color } as React.CSSProperties}
              />
              <svg className="w-5 h-5 absolute left-4 top-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </form>
        </div>
      </header>

      {/* Main Content Layout */}
      <main className="container mx-auto px-6 py-12 flex flex-col md:flex-row gap-8 items-start">

        {/* Filter Sidebar */}
        <aside className="w-full md:w-64 shrink-0 sticky top-6">
          <form action="" method="GET" className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
            {q && <input type="hidden" name="q" value={q} />}
            <div className="flex items-center justify-between mb-6">
              <h3 className="font-bold text-lg text-slate-800">Filters</h3>
              <svg className="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"></path></svg>
            </div>

            <div className="space-y-6">
              {/* Category */}
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">Category</label>
                <select name="category" defaultValue={category || ''} className="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-[var(--theme-color)] text-sm" style={{ '--tw-ring-color': shop.theme_color } as React.CSSProperties}>
                  <option value="">All Categories</option>
                  {shop.categories?.map((cat: any) => (
                    <option key={cat.id} value={cat.name}>{cat.name}</option>
                  ))}
                </select>
              </div>

              {/* Brand */}
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">Brand</label>
                <select name="brand" defaultValue={brand || ''} className="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-[var(--theme-color)] text-sm" style={{ '--tw-ring-color': shop.theme_color } as React.CSSProperties}>
                  <option value="">All Brands</option>
                  {shop.brands?.map((b: any) => (
                    <option key={b.id} value={b.name}>{b.name}</option>
                  ))}
                </select>
              </div>

              {/* Price Range */}
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">Price Range ($)</label>
                <div className="flex gap-2 items-center">
                  <input type="number" name="min_price" defaultValue={min_price || ''} placeholder="Min" min="0" step="1" className="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-[var(--theme-color)] text-sm" style={{ '--tw-ring-color': shop.theme_color } as React.CSSProperties} />
                  <span className="text-slate-400">-</span>
                  <input type="number" name="max_price" defaultValue={max_price || ''} placeholder="Max" min="0" step="1" className="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-[var(--theme-color)] text-sm" style={{ '--tw-ring-color': shop.theme_color } as React.CSSProperties} />
                </div>
              </div>

              {/* Rating */}
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">Minimum Rating</label>
                <select name="min_rating" defaultValue={min_rating || ''} className="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-[var(--theme-color)] text-sm" style={{ '--tw-ring-color': shop.theme_color } as React.CSSProperties}>
                  <option value="">Any Rating</option>
                  <option value="4">4+ Stars</option>
                  <option value="3">3+ Stars</option>
                  <option value="2">2+ Stars</option>
                  <option value="1">1+ Stars</option>
                </select>
              </div>
            </div>

            <button type="submit" className="w-full py-2.5 mt-8 rounded-lg text-white font-semibold shadow-sm transition-transform active:scale-95" style={{ backgroundColor: shop.theme_color }}>
              Apply Filters
            </button>

            {(q || category || brand || min_price || max_price || min_rating) && (
              <a href="?" className="block text-center mt-4 text-sm font-medium text-slate-500 hover:text-slate-800 transition-colors">
                Clear all filters
              </a>
            )}
          </form>
        </aside>

        {/* Product Grid */}
        <div className="flex-1">
          {products.length === 0 ? (
            <div className="text-center py-20 bg-white rounded-2xl border border-slate-100 shadow-sm">
              <div className="w-16 h-16 mx-auto bg-slate-100 rounded-full flex items-center justify-center mb-4">
                <svg className="w-8 h-8 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              </div>
              <p className="text-slate-600 font-medium text-lg">No products found matching your criteria.</p>
              <p className="text-slate-400 mt-1">Try adjusting your filters or search term.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {products.map((product: any) => (
                <div key={product.id} className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden hover:shadow-md transition-all group flex flex-col">
                  <Link href={getStorefrontLink(`/product/${product.id}`, shop.slug)} className="aspect-square bg-slate-50 flex items-center justify-center relative">
                    {product.image_url ? (
                      <img src={product.image_url} alt={product.name} className="object-cover w-full h-full" />
                    ) : (
                      <div className="w-16 h-16 rounded-full opacity-30" style={{ backgroundColor: shop.theme_color }} />
                    )}
                    <div className="absolute inset-0 bg-black/0 group-hover:bg-black/5 transition-colors" />
                  </Link>
                  <div className="p-6 flex flex-col flex-1">
                    <div className="flex justify-between items-start mb-2 gap-2">
                      <div className="text-xs font-bold uppercase tracking-wider text-slate-400 truncate">
                        {product.brand && product.category ? `${product.brand} • ${product.category}` : product.brand || product.category || 'Product'}
                      </div>
                      {product.average_rating > 0 && (
                        <div className="flex items-center text-amber-500 text-sm font-bold shrink-0">
                          <svg className="w-4 h-4 mr-0.5 fill-current" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path></svg>
                          {product.average_rating.toFixed(1)}
                        </div>
                      )}
                    </div>

                    <Link href={getStorefrontLink(`/product/${product.id}`, shop.slug)}>
                      <h3 className="text-lg font-bold text-slate-800 leading-tight mb-1 hover:underline">{product.name}</h3>
                    </Link>
                    <p className="text-slate-500 text-sm line-clamp-2 mb-4 flex-1">{product.description}</p>

                    <div className="mt-auto flex items-center justify-between">
                      <span className="font-extrabold text-xl text-slate-900">${(product.price / 100).toFixed(2)}</span>
                      <button
                        className="px-4 py-2 rounded-lg text-white font-semibold shadow-sm transition-transform active:scale-95"
                        style={{ backgroundColor: shop.theme_color }}
                      >
                        Add to Cart
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="py-12 border-t bg-white mt-12 text-center text-slate-500 text-sm">
        <p>&copy; {new Date().getFullYear()} {shop.name}. Powered by Nexus SaaS.</p>
      </footer>
    </div>
  );
}
