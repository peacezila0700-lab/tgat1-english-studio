/* TGAT1 English Studio v43.0.0 offline service worker — optimized (v43.1.0). */
'use strict';
const CACHE_NAME = 'tgat1-studio-v43.0.0';
const APP_SHELL = [
  './', './index.html', './app.css', './app.js', './data.js',
  './learning-hub.css', './learning-hub.js', './learning-hub-curriculum.js',
  './manifest.webmanifest', './icon-192.png', './icon-512.png',
  './icon-maskable-192.png', './icon-maskable-512.png', './apple-touch-icon.png'
];
const LAZY_CHUNKS = ['./data-vault.js', './data-senses.js'];
const cleanUrl = url => { const u=new URL(url,self.location.href);u.search='';u.hash='';return u.href; };
const isAppEntry = url => { const scope=new URL(self.registration.scope);return url.pathname===scope.pathname||url.pathname===scope.pathname+'index.html'; };
function fresh(url){return new Request(url,{cache:'reload'});}

// Precache app shell on install; fetch lazy chunks in background
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE_NAME).then(cache=>cache.addAll(APP_SHELL.map(fresh)).then(()=>Promise.allSettled(LAZY_CHUNKS.map(url=>fetch(fresh(url)).then(r=>r&&r.ok?cache.put(url,r):undefined)))))));
self.addEventListener('message',event=>{if(event.data&&event.data.type==='SKIP_WAITING')self.skipWaiting();});
self.addEventListener('activate',event=>event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('tgat1-studio-')&&k!==CACHE_NAME).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));

// Stale-while-revalidate for same-origin GET requests
self.addEventListener('fetch',event=>{
  const req=event.request,url=new URL(req.url);
  if(req.method!=='GET'||url.origin!==self.location.origin)return;
  if(req.mode==='navigate'){
    event.respondWith(fetch(req).then(response=>{if(response&&response.ok&&isAppEntry(url)){const copy=response.clone();caches.open(CACHE_NAME).then(cache=>cache.put('./index.html',copy));}return response;}).catch(()=>caches.match('./index.html')));return;
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
  // Other assets: cache-first, then network
  const key=cleanUrl(req.url);
  event.respondWith(caches.match(req).then(cached=>cached||caches.match(key).then(qcached=>qcached||fetch(req).then(response=>{
    if(response&&response.ok){const copy=response.clone();caches.open(CACHE_NAME).then(cache=>cache.put(key,copy));}
    return response;
  })).catch(()=>caches.match(key))));
});
