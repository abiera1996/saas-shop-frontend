// Lightweight service worker for Solid SaaS Platform installation prompts
const CACHE_NAME = 'solid-saas-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/static/css/global.css',
  '/static/js/jquery-3.6.3.min.js',
  '/static/plugins/aos/aos.css',
  '/static/plugins/aos/aos.js'
];

// Installation Lifecycle
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[Service Worker] Pre-caching static core assets');
        return cache.addAll(ASSETS_TO_CACHE);
      })
      .then(() => self.skipWaiting())
  );
});

// Activation Lifecycle
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.map(key => {
          if (key !== CACHE_NAME) {
            console.log('[Service Worker] Purging legacy cache assets', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch Interceptor Intersections
self.addEventListener('fetch', event => {
  // Gracefully filter non-GET and third-party local request pipelines
  if (event.request.method !== 'GET' || !event.request.url.startsWith(self.location.origin)) {
    return;
  }
  
  event.respondWith(
    caches.match(event.request)
      .then(cachedResponse => {
        if (cachedResponse) {
          return cachedResponse;
        }
        return fetch(event.request).then(networkResponse => {
          if (!networkResponse || networkResponse.status !== 200) {
            return networkResponse;
          }
          // Dynamically cache new local GET assets
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseToCache);
          });
          return networkResponse;
        }).catch(() => {
          // Graceful fallback for offline content requests
          console.warn('[Service Worker] Fetch failed, resource is currently offline.');
        });
      })
  );
});
