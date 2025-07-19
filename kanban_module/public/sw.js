// Service Worker for BizFlow Kanban Board
// Version 1.0.0

const CACHE_NAME = 'bizflow-kanban-v1.0.0';
const API_CACHE_NAME = 'bizflow-api-v1.0.0';
const IMAGE_CACHE_NAME = 'bizflow-images-v1.0.0';

// Cache strategy configuration
const CACHE_STRATEGIES = {
  CACHE_FIRST: 'cache-first',
  NETWORK_FIRST: 'network-first',
  STALE_WHILE_REVALIDATE: 'stale-while-revalidate',
  NETWORK_ONLY: 'network-only',
  CACHE_ONLY: 'cache-only'
};

// Files to cache immediately
const STATIC_ASSETS = [
  '/',
  '/static/js/bundle.js',
  '/static/css/main.css',
  '/manifest.json',
  '/favicon.ico',
  '/logo192.png',
  '/logo512.png'
];

// API endpoints to cache
const API_ROUTES = [
  '/api/tasks',
  '/api/columns',
  '/api/projects'
];

// Install event - cache static assets
self.addEventListener('install', (event) => {
  console.log('[SW] Installing service worker...');
  
  event.waitUntil(
    Promise.all([
      // Cache static assets
      caches.open(CACHE_NAME).then((cache) => {
        console.log('[SW] Caching static assets');
        return cache.addAll(STATIC_ASSETS);
      }),
      
      // Skip waiting to activate immediately
      self.skipWaiting()
    ])
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating service worker...');
  
  event.waitUntil(
    Promise.all([
      // Clean up old caches
      caches.keys().then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== CACHE_NAME && 
                cacheName !== API_CACHE_NAME && 
                cacheName !== IMAGE_CACHE_NAME) {
              console.log('[SW] Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      }),
      
      // Take control of all pages
      self.clients.claim()
    ])
  );
});

// Fetch event - handle requests
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const { url, method } = request;
  
  // Only handle GET requests
  if (method !== 'GET') {
    return;
  }
  
  // Determine cache strategy based on request type
  if (url.includes('/api/')) {
    // API requests - network first with cache fallback
    event.respondWith(handleApiRequest(request));
  } else if (url.match(/\.(png|jpg|jpeg|gif|svg|ico|webp)$/)) {
    // Images - cache first
    event.respondWith(handleImageRequest(request));
  } else if (url.includes('/static/')) {
    // Static assets - cache first
    event.respondWith(handleStaticRequest(request));
  } else {
    // HTML pages - stale while revalidate
    event.respondWith(handlePageRequest(request));
  }
});

// Handle API requests (Network First)
async function handleApiRequest(request) {
  const cache = await caches.open(API_CACHE_NAME);
  
  try {
    // Try network first
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      // Cache successful responses
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.log('[SW] Network failed for API request, trying cache:', request.url);
    
    // Fallback to cache
    const cachedResponse = await cache.match(request);
    if (cachedResponse) {
      // Add offline indicator header
      const headers = new Headers(cachedResponse.headers);
      headers.set('X-Served-By', 'service-worker-cache');
      
      return new Response(cachedResponse.body, {
        status: cachedResponse.status,
        statusText: cachedResponse.statusText,
        headers: headers
      });
    }
    
    // Return offline response
    return createOfflineResponse(request);
  }
}

// Handle image requests (Cache First)
async function handleImageRequest(request) {
  const cache = await caches.open(IMAGE_CACHE_NAME);
  const cachedResponse = await cache.match(request);
  
  if (cachedResponse) {
    return cachedResponse;
  }
  
  try {
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch (error) {
    console.log('[SW] Failed to load image:', request.url);
    return createPlaceholderImage();
  }
}

// Handle static assets (Cache First)
async function handleStaticRequest(request) {
  const cache = await caches.open(CACHE_NAME);
  const cachedResponse = await cache.match(request);
  
  if (cachedResponse) {
    return cachedResponse;
  }
  
  try {
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch (error) {
    console.log('[SW] Failed to load static asset:', request.url);
    return new Response('', { status: 404 });
  }
}

// Handle page requests (Stale While Revalidate)
async function handlePageRequest(request) {
  const cache = await caches.open(CACHE_NAME);
  const cachedResponse = await cache.match(request);
  
  // Start fetch in background
  const fetchPromise = fetch(request).then((networkResponse) => {
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  }).catch((error) => {
    console.log('[SW] Network failed for page request:', request.url);
    return null;
  });
  
  // Return cached version immediately if available
  if (cachedResponse) {
    return cachedResponse;
  }
  
  // Wait for network if no cache
  try {
    const networkResponse = await fetchPromise;
    return networkResponse || createOfflinePageResponse();
  } catch (error) {
    return createOfflinePageResponse();
  }
}

// Create offline response for API requests
function createOfflineResponse(request) {
  const offlineData = {
    error: 'offline',
    message: 'この機能はオフラインでは利用できません',
    timestamp: new Date().toISOString(),
    request: {
      url: request.url,
      method: request.method
    }
  };
  
  return new Response(JSON.stringify(offlineData), {
    status: 503,
    statusText: 'Service Unavailable',
    headers: {
      'Content-Type': 'application/json',
      'X-Served-By': 'service-worker-offline'
    }
  });
}

// Create offline page response
function createOfflinePageResponse() {
  const offlineHTML = `
    <!DOCTYPE html>
    <html lang="ja">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>オフライン - BizFlow カンバンボード</title>
      <style>
        body {
          font-family: 'Inter', sans-serif;
          margin: 0;
          padding: 40px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          text-align: center;
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        .container {
          max-width: 500px;
          background: rgba(255,255,255,0.1);
          padding: 40px;
          border-radius: 16px;
          backdrop-filter: blur(10px);
        }
        h1 { margin-bottom: 20px; }
        p { margin-bottom: 30px; opacity: 0.9; }
        button {
          background: white;
          color: #667eea;
          border: none;
          padding: 12px 24px;
          border-radius: 8px;
          font-weight: 600;
          cursor: pointer;
          font-size: 16px;
        }
        button:hover { transform: translateY(-2px); }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>📱 オフラインです</h1>
        <p>インターネット接続が確認できません。<br>接続を確認してから再度お試しください。</p>
        <button onclick="window.location.reload()">再試行</button>
      </div>
      <script>
        // Auto-retry when online
        window.addEventListener('online', () => {
          window.location.reload();
        });
      </script>
    </body>
    </html>
  `;
  
  return new Response(offlineHTML, {
    status: 200,
    headers: {
      'Content-Type': 'text/html; charset=utf-8',
      'X-Served-By': 'service-worker-offline'
    }
  });
}

// Create placeholder image
function createPlaceholderImage() {
  // Simple SVG placeholder
  const svg = `
    <svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
      <rect width="200" height="200" fill="#f3f4f6"/>
      <text x="100" y="100" text-anchor="middle" dy=".3em" fill="#9ca3af">画像なし</text>
    </svg>
  `;
  
  return new Response(svg, {
    status: 200,
    headers: {
      'Content-Type': 'image/svg+xml',
      'X-Served-By': 'service-worker-placeholder'
    }
  });
}

// Handle background sync
self.addEventListener('sync', (event) => {
  console.log('[SW] Background sync triggered:', event.tag);
  
  if (event.tag === 'sync-tasks') {
    event.waitUntil(syncTasks());
  }
});

// Sync tasks when back online
async function syncTasks() {
  try {
    // Get pending changes from IndexedDB
    const pendingChanges = await getPendingChanges();
    
    for (const change of pendingChanges) {
      try {
        const response = await fetch(change.url, {
          method: change.method,
          headers: change.headers,
          body: change.body
        });
        
        if (response.ok) {
          await removePendingChange(change.id);
          console.log('[SW] Synced change:', change.id);
        }
      } catch (error) {
        console.log('[SW] Failed to sync change:', change.id, error);
      }
    }
  } catch (error) {
    console.log('[SW] Background sync failed:', error);
  }
}

// Handle push notifications
self.addEventListener('push', (event) => {
  if (!event.data) {
    return;
  }
  
  const data = event.data.json();
  const options = {
    body: data.body,
    icon: '/logo192.png',
    badge: '/badge-72x72.png',
    vibrate: [200, 100, 200],
    data: data.data,
    actions: data.actions || [
      {
        action: 'view',
        title: '表示',
        icon: '/icon-view.png'
      },
      {
        action: 'dismiss',
        title: '閉じる',
        icon: '/icon-close.png'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification(data.title, options)
  );
});

// Handle notification clicks
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  
  const data = event.notification.data;
  let url = '/';
  
  if (data && data.url) {
    url = data.url;
  }
  
  event.waitUntil(
    self.clients.matchAll({ type: 'window' }).then((clients) => {
      // Check if there's already a window/tab open with the target URL
      for (const client of clients) {
        if (client.url === url && 'focus' in client) {
          return client.focus();
        }
      }
      
      // Open new window/tab
      if (self.clients.openWindow) {
        return self.clients.openWindow(url);
      }
    })
  );
});

// Utility functions (these would typically connect to IndexedDB)
async function getPendingChanges() {
  // Implementation would get pending changes from IndexedDB
  return [];
}

async function removePendingChange(id) {
  // Implementation would remove change from IndexedDB
  console.log('[SW] Removing pending change:', id);
}

// Log service worker lifecycle
console.log('[SW] Service Worker script loaded');