const SHELL='rack-shell-v15';
const MEDIA='rack-media-v3';
const SHELL_FILES=['./','./index.html','./manifest.json','./icon-192.png','./icon-512.png','./icon-180.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(SHELL).then(c=>c.addAll(SHELL_FILES)).then(()=>self.skipWaiting()));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==SHELL&&k!==MEDIA).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',e=>{
  const url=e.request.url;
  if(e.request.method!=='GET')return;
  if(url.includes('static.exercisedb.dev')||url.includes('cdn.jsdelivr.net')){
    e.respondWith(caches.open(MEDIA).then(async c=>{
      const hit=await c.match(e.request); if(hit)return hit;
      try{const res=await fetch(e.request); if(res.ok)c.put(e.request,res.clone()); return res;}catch(err){return hit||Response.error();}
    }));
    return;
  }
  if(url.includes('/gifs/')){
    e.respondWith(caches.open(MEDIA).then(async c=>{
      const hit=await c.match(e.request); if(hit)return hit;
      try{const res=await fetch(e.request); if(res.ok)c.put(e.request,res.clone()); return res;}catch(err){return hit||Response.error();}
    }));
    return;
  }
  if(url.startsWith(self.location.origin)){
    if(e.request.mode==='navigate'||e.request.destination==='document'){
      e.respondWith(fetch(e.request).then(res=>{const cl=res.clone();caches.open(SHELL).then(c=>c.put(e.request,cl));return res;}).catch(()=>caches.match(e.request).then(h=>h||caches.match('./index.html'))));
      return;
    }
    e.respondWith(caches.match(e.request).then(hit=>hit||fetch(e.request)));
  }
});
