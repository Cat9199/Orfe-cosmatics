const CACHE_NAME = 'orfe-admin-v1.0.3';
const STATIC_CACHE = 'orfe-admin-static-v1.0.3';
const DYNAMIC_CACHE = 'orfe-admin-dynamic-v1.0.3';

// Files to cache immediately
const STATIC_FILES = [
  '/admin',
  '/admin/products',
  '/admin/orders',
  '/admin/categories',
  '/admin/shipping',
  '/static/manifest.json',
  '/static/images/logo.svg',
  '/static/css/bootstrap.min.css',
  'https://cdn.tailwindcss.com',
  'https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css',
  'https://cdn.jsdelivr.net/npm/chart.js',
  'https://cdn.jsdelivr.net/npm/sweetalert2@11'
];

// Dynamic files to cache on first access
const DYNAMIC_FILES = [
  '/static/uploads/',
  '/admin/api/'
];

// Install event - cache static files
self.addEventListener('install', (event) => {
  console.log('Service Worker: Installing...');
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(cache => {
        console.log('Service Worker: Caching static files');
        return cache.addAll(STATIC_FILES);
      })
      .then(() => {
        console.log('Service Worker: Static files cached successfully');
        return self.skipWaiting();
      })
      .catch(error => {
        console.error('Service Worker: Failed to cache static files', error);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('Service Worker: Activating...');
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames.map(cacheName => {
            if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE && cacheName !== CACHE_NAME) {
              console.log('Service Worker: Deleting old cache', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('Service Worker: Activated successfully');
        return self.clients.claim();
      })
  );
});

// Fetch event - serve cached files when offline
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Only handle admin routes
  if (!url.pathname.startsWith('/admin')) {
    return;
  }

  // Handle admin API requests
  if (url.pathname.startsWith('/admin/api/')) {
    event.respondWith(
      caches.open(DYNAMIC_CACHE)
        .then(cache => {
          return fetch(request)
            .then(response => {
              // Cache successful API responses
              if (response.status === 200) {
                cache.put(request, response.clone());
              }
              return response;
            })
            .catch(() => {
              // Return cached response if available
              return cache.match(request);
            });
        })
    );
    return;
  }

  // Handle admin pages and static files
  event.respondWith(
    caches.match(request)
      .then(cachedResponse => {
        if (cachedResponse) {
          // Serve from cache
          return cachedResponse;
        }

        // Fetch from network and cache dynamic content
        return fetch(request)
          .then(response => {
            // Don't cache non-successful responses
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // Cache dynamic content
            if (url.pathname.startsWith('/admin') || url.pathname.startsWith('/static/uploads/')) {
              const responseToCache = response.clone();
              caches.open(DYNAMIC_CACHE)
                .then(cache => {
                  cache.put(request, responseToCache);
                });
            }

            return response;
          })
          .catch(() => {
            // Return offline page for admin routes
            if (url.pathname.startsWith('/admin')) {
              return caches.match('/admin/offline') || 
                     new Response(generateOfflinePage(), {
                       headers: { 'Content-Type': 'text/html; charset=utf-8' }
                     });
            }
          });
      })
  );
});

// Background sync for offline actions
self.addEventListener('sync', (event) => {
  if (event.tag === 'background-sync-orders') {
    event.waitUntil(syncOfflineOrders());
  }
  if (event.tag === 'background-sync-products') {
    event.waitUntil(syncOfflineProducts());
  }
});

// Push notifications
self.addEventListener('push', (event) => {
  const options = {
    body: event.data ? event.data.text() : 'إشعار جديد من لوحة التحكم',
    icon: '/static/icons/icon-192x192.png',
    badge: '/static/icons/icon-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'فتح لوحة التحكم',
        icon: '/static/icons/icon-96x96.png'
      },
      {
        action: 'close',
        title: 'إغلاق',
        icon: '/static/icons/icon-96x96.png'
      }
    ],
    requireInteraction: true,
    silent: false,
    dir: 'rtl',
    lang: 'ar'
  };

  event.waitUntil(
    self.registration.showNotification('Orfe Admin', options)
  );
});

// Handle notification clicks
self.addEventListener('notificationclick', (event) => {
  event.notification.close();

  if (event.action === 'explore') {
    event.waitUntil(
      self.clients.openWindow('/admin')
    );
  } else if (event.action === 'close') {
    // Just close the notification
    return;
  } else {
    // Default action - open admin dashboard
    event.waitUntil(
      self.clients.openWindow('/admin')
    );
  }
});

// Sync offline orders
async function syncOfflineOrders() {
  try {
    const cache = await caches.open(DYNAMIC_CACHE);
    const requests = await cache.keys();
    
    for (const request of requests) {
      if (request.url.includes('/admin/orders') && request.method === 'POST') {
        try {
          await fetch(request);
          await cache.delete(request);
          console.log('Synced offline order:', request.url);
        } catch (error) {
          console.error('Failed to sync order:', error);
        }
      }
    }
  } catch (error) {
    console.error('Failed to sync offline orders:', error);
  }
}

// Sync offline products
async function syncOfflineProducts() {
  try {
    const cache = await caches.open(DYNAMIC_CACHE);
    const requests = await cache.keys();
    
    for (const request of requests) {
      if (request.url.includes('/admin/products') && request.method === 'POST') {
        try {
          await fetch(request);
          await cache.delete(request);
          console.log('Synced offline product:', request.url);
        } catch (error) {
          console.error('Failed to sync product:', error);
        }
      }
    }
  } catch (error) {
    console.error('Failed to sync offline products:', error);
  }
}

// Generate offline page HTML
function generateOfflinePage() {
  return `
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>غير متصل - Orfe Admin</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css" rel="stylesheet">
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        </style>
    </head>
    <body class="bg-gray-50 min-h-screen flex items-center justify-center">
        <div class="text-center max-w-md mx-auto p-8">
            <div class="mb-8">
                <i class='bx bx-wifi-off text-6xl text-gray-400 mb-4'></i>
                <h1 class="text-2xl font-bold text-gray-800 mb-2">غير متصل بالإنترنت</h1>
                <p class="text-gray-600">يبدو أنك غير متصل بالإنترنت. تحقق من اتصالك وحاول مرة أخرى.</p>
            </div>
            
            <div class="space-y-4">
                <button onclick="window.location.reload()" class="w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors">
                    <i class='bx bx-refresh mr-2'></i>
                    إعادة المحاولة
                </button>
                
                <button onclick="history.back()" class="w-full bg-gray-200 text-gray-700 py-3 px-6 rounded-lg hover:bg-gray-300 transition-colors">
                    <i class='bx bx-arrow-back mr-2'></i>
                    العودة
                </button>
            </div>
            
            <div class="mt-8 p-4 bg-blue-50 rounded-lg">
                <p class="text-sm text-blue-800">
                    <i class='bx bx-info-circle mr-1'></i>
                    بعض الميزات متاحة حتى بدون اتصال بالإنترنت
                </p>
            </div>
        </div>
    </body>
    </html>
  `;
}

// Handle message events from main thread
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

console.log('Service Worker: Loaded successfully');
