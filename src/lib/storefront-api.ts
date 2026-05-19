import { getStorefrontLink } from './storefront-link';

const API_BASE_URL = typeof window !== 'undefined'
  ? (process.env.NEXT_PUBLIC_API_URL || '/api/proxy')
  : (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api');

export async function fetchStorefrontApi(shopSlug: string, endpoint: string, options: RequestInit = {}) {
  const token = typeof window !== 'undefined' ? localStorage.getItem(`customer_token_${shopSlug}`) : null;
  
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> || {}),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}/storefront/${shopSlug}${endpoint}`, {
    ...options,
    headers,
  });

  if (response.status === 401 && typeof window !== 'undefined') {
    // If not on login page, clear token and maybe redirect
    if (!window.location.pathname.includes('/login')) {
      localStorage.removeItem(`customer_token_${shopSlug}`);
      window.location.href = getStorefrontLink('/login', shopSlug);
    }
  }

  return response;
}
