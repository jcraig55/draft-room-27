const {chromium,devices}=require('playwright');(async()=>{const b=await chromium.launch();const errs=[];const c=await b.newContext({...devices['iPhone 13'],serviceWorkers:'block'});const p=await c.newPage();p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8765/index.html');await p.waitForTimeout(500);
await p.evaluate(()=>{S.user=[4];persist();render()});
console.log('btn',await p.textContent('#simUser'));
await p.click('#simUser');await p.waitForTimeout(900);console.log('btn live',await p.textContent('#simUser'),'| ticker',await p.textContent('#liveTicker'));
await p.screenshot({path:'l1.png'});
await p.waitForTimeout(3000);console.log('picks after ~4s normal',await p.evaluate(()=>Object.keys(S.sel).length),await p.textContent('#liveTicker'));
await p.screenshot({path:'l2.png'});
// pause
await p.click('#simUser');const n1=await p.evaluate(()=>Object.keys(S.sel).length);await p.waitForTimeout(2500);console.log('paused holds',n1,await p.evaluate(()=>Object.keys(S.sel).length),await p.textContent('#simUser'));
// speed fast
await p.evaluate(()=>{TM.pace="fast"});await p.click('#simUser');
await p.waitForSelector('#pkClock:not([hidden])',{timeout:15000});console.log('picker opened at',await p.evaluate(()=>nextOpen().label),'clock',await p.textContent('#pkClock b'));
await p.screenshot({path:'l3.png'});
await p.click('#pkl [data-take] >> nth=0');await p.waitForTimeout(1600);console.log('continues after my pick',await p.evaluate(()=>Object.keys(S.sel).length),await p.textContent('#liveTicker'));
await p.screenshot({path:'l4.png'});
// close picker on my next turn, check pill + ticker button
await p.waitForSelector('#pkClock:not([hidden])',{timeout:30000});await p.click('#pkx');await p.waitForTimeout(300);console.log('ticker you',await p.textContent('#liveTicker'),'pill',await p.isVisible('#clockPill'));await p.screenshot({path:'l5.png'});
// timer auto pick continues
await p.evaluate(()=>{clk.dl=Date.now()+800});await p.waitForTimeout(2500);console.log('auto + continue',await p.evaluate(()=>[Object.keys(S.sel).length,live.on]));
// instant
await p.evaluate(()=>{TM.pace="instant"});await p.waitForSelector('#pkClock:not([hidden])',{timeout:30000});console.log('instant at',await p.evaluate(()=>nextOpen().label));
// sim all to end
await p.click('#pkx');await p.click('#simAll');await p.waitForTimeout(800);console.log('done btn',await p.textContent('#simUser'),await p.evaluate(()=>[live.on,!!nextOpen()]),'ticker empty',(await p.textContent('#liveTicker'))==='');
await p.click('#clearPicks');await p.click('#clearPicks');console.log('cleared btn',await p.textContent('#simUser'));
console.log('errs',errs);await b.close()})();
