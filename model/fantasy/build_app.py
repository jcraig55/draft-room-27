# Builds the installable app (PWA) into /home/claude/app from the current Draft Room page.
import json,datetime
V=datetime.datetime.now().strftime('%Y%m%d%H%M')
t=open('/home/claude/fantasy/draft-room-2027.html',encoding='utf-8').read()
i=t.index('</style>')+8
head='''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#FFFFFF">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Draft Room">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" type="image/png" href="icon-192.png">
<style>[hidden]{display:none!important}:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}img{max-width:100%}</style>
'''
sw='<script>if("serviceWorker" in navigator){const had=!!navigator.serviceWorker.controller;let done=false;navigator.serviceWorker.addEventListener("controllerchange",()=>{if(had&&!done){done=true;location.reload()}});window.addEventListener("load",()=>navigator.serviceWorker.register("sw.js",{updateViaCache:"none"}).then(r=>r.update()).catch(()=>{}))}</script>\n'
tab='<button role="tab" data-tab="saved" aria-selected="false">Saved Mocks</button>'
assert tab in t
t=t.replace(tab,tab+'\n    <a class="tablink" href="top125.html">Top 125 ›</a>')
hp='Rankings come from this season’s production, last season’s, age and role.</p>'
assert hp in t
t=t.replace(hp,hp+'\n      <a class="boardlink" href="top125.html">Top 125 board &amp; player stats ›</a>',1)
t=t.replace('</style>','.boardlink{display:inline-block;margin-top:12px;padding:9px 16px;border-radius:999px;background:var(--accent);color:var(--accent-ink);font-weight:700;font-size:14px;text-decoration:none}</style>',1)
t=t.replace('</style>','.tablink{padding:8px 14px;border-radius:999px;font-family:var(--f-display);font-weight:700;font-size:17px;letter-spacing:.04em;text-transform:uppercase;color:var(--accent);white-space:nowrap;text-decoration:none;align-self:center}</style>',1)
i=t.index('</style>')+8
open('/home/claude/app/index.html','w',encoding='utf-8').write(head+t[:i]+'\n</head>\n<body>\n'+t[i:]+'\n'+sw+'</body>\n</html>\n')
# Top 125 + Player stats pages inside the app
pwa_head='<meta name="theme-color" content="#FFFFFF">\n<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-status-bar-style" content="default">\n<meta name="apple-mobile-web-app-title" content="Draft Room">\n<link rel="manifest" href="manifest.webmanifest">\n<link rel="apple-touch-icon" href="apple-touch-icon.png">\n<link rel="icon" type="image/png" href="icon-192.png">\n<style>body{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}</style>\n'
for src,dst in [('top125.html','top125.html'),('stats.html','stats.html')]:
    h=open('/home/claude/fantasy/'+src,encoding='utf-8').read()
    h=h.replace('<meta name="viewport" content="width=device-width,initial-scale=1">','<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'+pwa_head,1)
    h=h.replace('<nav class="nav"><a href="index.html"','<nav class="nav"><a href="index.html">‹ Draft Room</a><a href="top125.html"',1)
    h=h.replace('</body>',sw+'</body>',1)
    open('/home/claude/app/'+dst,'w',encoding='utf-8').write(h)
json.dump({"name":"Draft Room ’27","short_name":"Draft Room","description":"2027 fantasy football mock drafts: full PPR, 16 teams.","start_url":"./","scope":"./","display":"standalone","orientation":"portrait","background_color":"#FFFFFF","theme_color":"#FFFFFF",
 "icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png"},{"src":"icon-maskable-512.png","sizes":"512x512","type":"image/png","purpose":"maskable"}]},
 open('/home/claude/app/manifest.webmanifest','w',encoding='utf-8'),ensure_ascii=False,indent=1)
open('/home/claude/app/sw.js','w').write(f'''const C="dr27-{V}";
const CORE=["./","index.html","top125.html","stats.html","manifest.webmanifest","icon-192.png","icon-512.png","apple-touch-icon.png"];
self.addEventListener("install",e=>{{e.waitUntil(caches.open(C).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting()))}});
self.addEventListener("activate",e=>{{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==C).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))}});
self.addEventListener("fetch",e=>{{const r=e.request;if(r.method!=="GET")return;
 if(r.mode==="navigate"){{e.respondWith(fetch(r,{{cache:"no-cache"}}).then(res=>{{const cp=res.clone();caches.open(C).then(c=>c.put(r,cp));return res}}).catch(()=>caches.match(r,{{ignoreSearch:true}}).then(h=>h||caches.match("index.html"))));return}}
 e.respondWith(caches.match(r).then(hit=>hit||fetch(r).then(res=>{{if(res.ok||res.type==="opaque"){{const cp=res.clone();caches.open(C).then(c=>c.put(r,cp))}}return res}})))}});
''')
print('app built',V)
