import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(req: NextRequest) {
  const url = req.nextUrl;
  
  // Get hostname of request (e.g. shop1.oursaas.com, localhost)
  const hostHeader = req.headers.get('host') || '';
  const hostname = hostHeader.split(':')[0];
  
  // Define allowed domains (including local development)
  const allowedDomains = ['localhost', 'oursaas.com', '127.0.0.1'];
  
  // Verify if it's a subdomain
  const isSubdomain = !allowedDomains.some(domain => hostname === domain);
  
  // Extract subdomain (e.g. 'shop1' from 'shop1.localhost' or 'shop1.oursaas.com')
  const subdomain = hostname.split('.')[0];
  
  // If the path already has /storefront, do not rewrite it (prevents 404 on direct paths)
  if (url.pathname.startsWith('/storefront')) {
    return NextResponse.next();
  }

  // Exclude public paths from being rewritten to a storefront
  // On subdomains, /login and /register should be rewritten to customer storefront login/register
  const publicPaths = isSubdomain 
    ? ['/dashboard', '/api', '/_next'] 
    : ['/login', '/register', '/dashboard', '/api', '/_next'];
    
  const isPublicPath = publicPaths.some(path => url.pathname.startsWith(path));
  console.log('hello', isSubdomain, isPublicPath)
  if (isSubdomain && !isPublicPath) {
    
    if (url.pathname.startsWith('/product')) {
      const productId = url.pathname.split('/product/')?.[1];
      console.log('hello2', productId)
      return NextResponse.rewrite(new URL(`/storefront/${subdomain}/product/${productId}`, req.url));
    }
    // Rewrite to our dynamic storefront route, preserving search parameters (like ?q=...)
    return NextResponse.rewrite(new URL(`/storefront/${subdomain}${url.pathname}${url.search}`, req.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};
