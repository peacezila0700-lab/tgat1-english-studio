/* TGAT1 English Studio v45.0.0 offline service worker — network-first app assets. */
'use strict';
const CACHE_NAME = 'tgat1-studio-v45.0.0';
const APP_SHELL = [
  './', './index.html', './app.css', './app.js', './data.js',
  './learning-hub.css', './learning-hub.js', './learning-hub-curriculum.js',
  './landing.html', './ui-mockups.html',
  './manifest.webmanifest', './icon-192.png', './icon-512.png',
  './icon-maskable-192.png', './icon-maskable-512.png', './apple-touch-icon.png'
];
const LAZY_CHUNKS = ['./data-vault.js', './data-senses.js'];
const cleanUrl = url => { const u=new URL(url,self.location.href);u.search='';u.hash='';return u.href; };
const isAppEntry = url => { const scope=new URL(self.registration.scope);return url.pathname===scope.pathname||url.pathname===scope.pathname+'index.html'; };
// App assets (code/style that changes with every release): always fetch fresh from
// network first, fall back to cache only when offline. Guarantees the latest build
// is served after a GitHub Pages deploy, regardless of SW update timing.
const isAppAsset = url => /\/(app|learning-hub(?:-curriculum)?)\.(js|css)$/.test(url.pathname);
function fresh(url){return new Request(url,{cache:'reload'});}

// Precache app shell on install; fetch lazy chunks in background.
// skipWaiting: activate the new SW immediately so a freshly-deployed build takes
// over on the next navigation without requiring a manual 'update' click.
self.addEventListener('install',event=>{self.skipWaiting();event.waitUntil(caches.open(CACHE_NAME).then(cache=>cache.addAll(APP_SHELL.map(fresh)).then(()=>Promise.allSettled(LAZY_CHUNKS.map(url=>fetch(fresh(url)).then(r=>r&&r.ok?cache.put(url,r):undefined))))))});
self.addEventListener('message',event=>{if(event.data&&event.data.type==='SKIP_WAITING')self.skipWaiting();});
self.addEventListener('activate',event=>event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('tgat1-studio-')&&k!==CACHE_NAME).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));

// Strategy: HTML + app assets = network-first (fresh after deploy);
// data files = stale-while-revalidate; icons/manifest = cache-first.
self.addEventListener('fetch',event=>{
  const req=event.request,url=new URL(req.url);
  if(req.method!=='GET'||url.origin!==self.location.origin)return;
  if(req.mode==='navigate'){
    event.respondWith(fetch(req).then(response=>{if(response&&response.ok&&isAppEntry(url)){const copy=response.clone();caches.open(CACHE_NAME).then(cache=>cache.put('./index.html',copy));}return response;}).catch(()=>caches.match('./index.html')));return;
  }
  // App assets: network-first (latest build when online, cache fallback offline)
  if(isAppAsset(url)){
    event.respondWith(fetch(req).then(response=>{if(response&&response.ok){const copy=response.clone();caches.open(CACHE_NAME).then(cache=>cache.put(cleanUrl(req.url),copy));}return response;}).catch(()=>caches.match(req).then(cached=>cached||caches.match(cleanUrl(req.url)).then(qc=>qc||caches.match('./index.html')))));return;
  }
  // Data files (data*.js): stale-while-revalidate — serve cache immediately, refresh in background
  const isDataFile = /\/data(?:-[a-z]+)?\.js$/.test(url.pathname);
  if(isDataFile){
    event.respondWith(caches.match(req).then(cached=>{
      fetch(fresh(req)).then(response=>{if(response&&response.ok){const copy=response.clone();caches.open(CACHE_NAME).then(cache=>cache.put(cleanUrl(req.url),copy));}}).catch(()=>{});
      return cached||fetch(req).then(response=>{if(response&&response.ok){const copy=response.clone();caches.open(CACHE_NAME).then(cache=>cache.put(cleanUrl(req.url),copy));}return response;}).catch(()=>caches.match(req));
    }));
    return;
  }
  // Other assets (icons, manifest): cache-first, then network
  const key=cleanUrl(req.url);
  event.respondWith(caches.match(req).then(cached=>cached||caches.match(key).then(qcached=>qcached||fetch(req).then(response=>{
    if(response&&response.ok){const copy=response.clone();caches.open(CACHE_NAME).then(cache=>cache.put(key,copy));}
    return response;
  })).catch(()=>caches.match(key))));
});
