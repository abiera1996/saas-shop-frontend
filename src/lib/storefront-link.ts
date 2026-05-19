/**
 * Helper to generate storefront links dynamically.
 * Omit the `/storefront/[slug]` prefix if the customer is browsing via a tenant subdomain.
 */
export function getStorefrontLink(path: string, shopSlug: string): string {
  return path
  if (typeof window === 'undefined') {
    return `/storefront/${shopSlug}${path === '/' ? '' : path}`;
  }

  const hostname = window.location.hostname;
  
  // Base allowed main domains
  const baseDomains = ['localhost', 'oursaas.com'];
  
  // Verify if it is a subdomain of oursaas.com or a subdomain in general
  const isSubdomain = !baseDomains.some(domain => hostname === domain);
  
  if (isSubdomain) {
    // Under subdomain mode, the path maps directly (e.g. /login maps to customer login)
    return path;
  }
  
  return `/storefront/${shopSlug}${path === '/' ? '' : path}`;
}
