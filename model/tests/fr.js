const {chromium,devices}=require('playwright');(async()=>{const b=await chromium.launch();const errs=[];const c=await b.newContext({...devices['iPhone 13'],serviceWorkers:'block'});const p=await c.newPage();p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8765/index.html');await p.waitForTimeout(500);
console.log('same order now',await p.evaluate(()=>P.slice(0,300).every((x,i)=>x.trank===x.rank)),await p.evaluate(()=>P.slice(0,5).map(x=>x.rank+' '+x.name+' t'+x.trank).join(' | ')));
await p.click('.bnav [data-tab="top"]');await p.waitForTimeout(300);console.log(await p.textContent('#topSub'));console.log((await p.textContent('#topList')).slice(0,120));
await p.click('#tPos [data-tp="QB"]');console.log(await p.$$eval('.tierbox .tierdiv',l=>l.map(e=>e.textContent).join(' / ')));
await p.click('.bnav [data-tab="board"]');console.log(await p.textContent('#p-board .sub'));
console.log('errs',errs);await b.close()})();
