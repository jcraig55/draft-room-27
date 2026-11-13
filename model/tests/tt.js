const {chromium,devices}=require('playwright');(async()=>{const b=await chromium.launch();const errs=[];const c=await b.newContext({...devices['iPhone 13'],serviceWorkers:'block'});const p=await c.newPage();p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8765/index.html');await p.waitForTimeout(500);
await p.click('.bnav [data-tab="top"]');await p.waitForTimeout(300);await p.screenshot({path:'tt0.png'});
await p.click('#tPos [data-tp="RB"]');await p.waitForTimeout(300);console.log(await p.$$eval('.tierbox .tierdiv',l=>l.map(e=>e.textContent)));await p.screenshot({path:'tt1.png'});
await p.click('#tPos [data-tp="WR"]');await p.waitForTimeout(300);await p.screenshot({path:'tt2.png'});
await p.click('.tierbox .nm >> nth=0');await p.waitForTimeout(300);console.log('bio',await p.evaluate(()=>!!document.querySelector('#bioHost')?.innerText));
console.log('errs',errs);await b.close()})();
