const NEXT_API_URL = '/api';

export async function fetchApi(endpoint: string, options: RequestInit = {}) {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };

  // The browser will automatically attach the HttpOnly cookie for us.
  const response = await fetch(`${NEXT_API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    if (typeof window !== 'undefined') {
      window.location.href = '/login';
    }
  }

  return response;
}
