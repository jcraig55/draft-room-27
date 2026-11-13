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
i=t.index('</style>')+8
open('/home/claude/app/index.html','w',encoding='utf-8').write(head+t[:i]+'\n</head>\n<body>\n'+t[i:]+'\n'+sw+'</body>\n</html>\n')
# Top 125 PDF inside the app (latest dated copy)
import glob,shutil,os
for old in ('top125.html','stats.html'):
    if os.path.exists('/home/claude/app/'+old): os.remove('/home/claude/app/'+old)
pdfs=sorted(glob.glob('/home/claude/downloads/draft-room-27-top-125 (*).pdf'),key=os.path.getmtime)
if pdfs: shutil.copy(pdfs[-1],'/home/claude/app/top125.pdf')
json.dump({"name":"Draft Room ’27","short_name":"Draft Room","description":"2027 fantasy football mock drafts: full PPR, 16 teams.","start_url":"./","scope":"./","display":"standalone","orientation":"portrait","background_color":"#FFFFFF","theme_color":"#FFFFFF",
 "icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png"},{"src":"icon-maskable-512.png","sizes":"512x512","type":"image/png","purpose":"maskable"}]},
 open('/home/claude/app/manifest.webmanifest','w',encoding='utf-8'),ensure_ascii=False,indent=1)
open('/home/claude/app/sw.js','w').write(f'''const C="dr27-{V}";
const CORE=["./","index.html","manifest.webmanifest","icon-192.png","icon-512.png","apple-touch-icon.png"];
self.addEventListener("install",e=>{{e.waitUntil(caches.open(C).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting()))}});
self.addEventListener("activate",e=>{{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==C).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))}});
self.addEventListener("fetch",e=>{{const r=e.request;if(r.method!=="GET")return;
 if(r.mode==="navigate"){{e.respondWith(fetch(r,{{cache:"no-cache"}}).then(res=>{{const cp=res.clone();caches.open(C).then(c=>c.put(r,cp));return res}}).catch(()=>caches.match(r,{{ignoreSearch:true}}).then(h=>h||caches.match("index.html"))));return}}
 e.respondWith(caches.match(r).then(hit=>hit||fetch(r).then(res=>{{if(res.ok||res.type==="opaque"){{const cp=res.clone();caches.open(C).then(c=>c.put(r,cp))}}return res}})))}});
''')
print('app built',V)
