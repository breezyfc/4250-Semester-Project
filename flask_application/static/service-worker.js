// Service Worker for Calendrier - system notification handling

self.addEventListener('install', event => {
    self.skipWaiting();
});

self.addEventListener('activate', event => {
    event.waitUntil(clients.claim());
});

self.addEventListener('message', event => {
    const data = event.data || {};
    if (data.type !== 'SHOW_NOTIFICATION') {
        return;
    }

    const title = data.title || 'Calendrier Notification';
    const body = data.body || '';

    event.waitUntil(
        self.registration.showNotification(title, {
            body,
            icon: '/static/images/light-logo.png',
            badge: '/static/images/logo.png',
            tag: data.tag || 'daily-assignments',
            renotify: true,
            requireInteraction: true,
            data: { url: '/' }
        })
    );
});

self.addEventListener('push', event => {
    const payload = event.data ? event.data.json() : {};
    const title = payload.title || 'Calendrier Notification';
    const body = payload.body || '';
    const url = payload.url || '/';
    const tag = payload.tag || 'daily-assignments';

    event.waitUntil(
        self.registration.showNotification(title, {
            body,
            icon: '/static/images/light-logo.png',
            badge: '/static/images/logo.png',
            tag,
            renotify: true,
            requireInteraction: true,
            data: { url }
        })
    );
});

// Handle notification clicks
self.addEventListener('notificationclick', event => {
    event.notification.close();

    // Open or focus the app
    event.waitUntil(
        clients.matchAll({ type: 'window', includeUncontrolled: true }).then(clientList => {
            // Check if there's already a window open
            for (let i = 0; i < clientList.length; i++) {
                const client = clientList[i];
                if ('focus' in client) {
                    return client.focus();
                }
            }
            // If not, open a new window
            if (clients.openWindow) {
                return clients.openWindow(event.notification.data?.url || '/');
            }
        })
    );
});
