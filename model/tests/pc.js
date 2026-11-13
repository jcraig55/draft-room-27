const {chromium,devices}=require('playwright');(async()=>{const b=await chromium.launch();const errs=[];const c=await b.newContext({...devices['iPhone 13'],serviceWorkers:'block'});const p=await c.newPage();p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8765/index.html');await p.waitForTimeout(500);
await p.evaluate(()=>{S.user=[4];TM.pace="instant";persist();render()});await p.click('#simUser');await p.waitForTimeout(800);
await p.click('#pkFilterX');await p.waitForTimeout(200);
console.log(await p.textContent('.pickcard'));await p.locator('.pickcard').scrollIntoViewIfNeeded();await p.screenshot({path:'pc1.png'});
await p.click('#pkFilterBtn');await p.click('#pkpos [data-p="RB"]');console.log('with filter still shown',await p.isVisible('.pickcard'));
console.log('errs',errs);await b.close()})();
