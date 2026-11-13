const {chromium,devices}=require('playwright');(async()=>{const b=await chromium.launch();const errs=[];const c=await b.newContext({...devices['iPhone 13'],serviceWorkers:'block'});const p=await c.newPage();p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8765/index.html');await p.waitForTimeout(500);await p.screenshot({path:'pr1.png'});
// hold a press
const bb=await (await p.$('#simOne')).boundingBox();await p.mouse.move(bb.x+20,bb.y+10);await p.mouse.down();await p.waitForTimeout(120);
console.log('pressed',await p.$eval('#simOne',e=>[e.classList.contains('pressed'),getComputedStyle(e).transform,getComputedStyle(e).boxShadow]));await p.screenshot({path:'pr2.png',clip:{x:0,y:90,width:390,height:110}});
await p.mouse.up();await p.waitForTimeout(250);await p.evaluate(()=>closeSheet());console.log('released',await p.$eval('#simOne',e=>[e.classList.contains('pressed'),getComputedStyle(e).transform]));
// normal flows still work
await p.click('#simUser');await p.waitForTimeout(500);console.log('picker',await p.isVisible('#pkl'));await p.screenshot({path:'pr3.png'});
await p.click('#pkl [data-take] >> nth=0');await p.click('#simUser').catch(()=>{});
for(const t of ['board','top','mocks']){await p.click(`.bnav [data-tab="${t}"]`);await p.waitForTimeout(200)}await p.click('.bnav [data-tab="top"]');await p.waitForTimeout(200);await p.screenshot({path:'pr4.png'});
await p.click('#openSettings');await p.waitForTimeout(400);await p.screenshot({path:'pr5.png'});
console.log('errs',errs);await b.close()})();
