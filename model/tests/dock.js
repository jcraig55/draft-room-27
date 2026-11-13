const {chromium,devices}=require('playwright');(async()=>{const b=await chromium.launch();const errs=[];const c=await b.newContext({...devices['iPhone 13'],serviceWorkers:'block'});const p=await c.newPage();p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8765/index.html');await p.waitForTimeout(500);
await p.evaluate(()=>{S.user=[9];TM.pace="slow";persist();render()});await p.click('#simUser');await p.waitForTimeout(500);
await p.mouse.wheel(0,3000);await p.waitForTimeout(500);
const r=await p.$eval('.dock',e=>e.getBoundingClientRect().top);console.log('dock top after scroll',r,'pause visible',await p.isVisible('#simUser'));
await p.screenshot({path:'d1.png'});
await p.click('#simUser');console.log('paused from scrolled',await p.evaluate(()=>live.on));
// picker scroll → close
await p.evaluate(()=>openPicker(nextOpen().num));await p.waitForTimeout(300);
await p.$eval('.sheet',e=>e.scrollTop=1200);await p.waitForTimeout(300);console.log('xbtn visible',await p.isVisible('.sheet .xbtn'));await p.screenshot({path:'d2.png'});
await p.click('.sheet .xbtn');await p.waitForTimeout(200);console.log('picker closed',!(await p.$('.sheet')));
// settings
await p.click('#openSettings');await p.waitForTimeout(400);await p.$eval('.setsheet',e=>e.scrollTop=600);await p.waitForTimeout(300);await p.screenshot({path:'d3.png'});await p.click('.setsheet .xbtn');await p.waitForTimeout(400);console.log('settings closed',await p.isHidden('#setScrim'));
// board view
await p.click('.bnav [data-tab="board"]');await p.click('#bSeg [data-v="grid"]');await p.click('#boardList [data-boardview]');await p.waitForTimeout(300);await p.$eval('.bv',e=>e.scrollTop=500);await p.waitForTimeout(300);await p.click('.bv .xbtn');console.log('bv closed',!(await p.$('.bv')));
// guide mover
await p.click('.bnav [data-tab="mock"]');await p.evaluate(()=>openGuide());await p.waitForTimeout(400);await p.$eval('.mover',e=>e.scrollTop=400);await p.waitForTimeout(300);const vis=await p.isVisible('.mover .xbtn');console.log('guide xbtn',vis);if(vis){await p.click('.mover .xbtn');await p.waitForTimeout(400);console.log('guide closed',!(await p.$('.mover')))}
console.log('errs',errs);await b.close()})();
