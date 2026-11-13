const {chromium,devices}=require('playwright');
(async()=>{
const b=await chromium.launch();const errs=[];
const ctx=await b.newContext({...devices['iPhone 13'],serviceWorkers:'block'});
const pg=await ctx.newPage();pg.on('pageerror',e=>errs.push('pageerror '+e.message));pg.on('console',m=>{if(m.type()==='error')errs.push('console '+m.text())});
await pg.goto('http://localhost:8765/index.html');await pg.waitForTimeout(800);
const shot=n=>pg.screenshot({path:`/home/claude/tests/s_${n}.png`});
await shot('1draft');
// every player badge
const nob=await pg.evaluate(()=>P.filter(x=>!bdOf(x).length).map(x=>x.name));console.log('no badge',nob.length,nob.slice(0,5));
console.log('badge keys',await pg.evaluate(()=>[...new Set(P.flatMap(x=>bdOf(x)))].join(',')));
// settings
await pg.click('#openSettings');await pg.waitForTimeout(400);await shot('2settings');
await pg.selectOption('#scoring','half').catch(e=>errs.push('scoring '+e.message));
await pg.waitForTimeout(200);console.log('league line',await pg.textContent('#leagueLine'));
await pg.selectOption('#scoring','ppr');
await pg.evaluate(()=>closeSettings());await pg.waitForTimeout(400);
// pick window
await pg.click('#simUser');await pg.waitForTimeout(700);await shot('3afterSim');
const open=await pg.evaluate(()=>!!document.querySelector('#pkl'));console.log('picker open',open);
if(open){
 await shot('4picker');
 console.log('row badges max',await pg.evaluate(()=>Math.max(...[...document.querySelectorAll('#pkl .prow')].map(r=>r.querySelectorAll('.bds > .bd').length))));
 const sum=await pg.$('details.assist summary');console.log('assist summary',sum?await sum.textContent():null);
 if(sum){await sum.click();await pg.waitForTimeout(200);await shot('6assist');await sum.click()}
 await pg.click('#pkFilterBtn');await pg.waitForTimeout(200);await shot('5filter');
 await pg.click('#pkpos button[data-p="WR"]');await pg.waitForTimeout(200);console.log('filter btn',await pg.textContent('#pkFilterBtn'));
 await pg.click('#pkbd button[data-bh]');await pg.waitForTimeout(200);console.log('filter btn',await pg.textContent('#pkFilterBtn'));await pg.click('#pkbd button[data-bh]');await pg.click('#pkpos button[data-p="ALL"]');
 await pg.click('#pkFilterBtn');
 // swipe left on first row
 const r=await pg.$('#pkl .prow');const bb=await r.boundingBox();
 await pg.evaluate(({y})=>{const el=document.querySelector('#pkl .prow');const t=(x)=>new Touch({identifier:1,target:el,clientX:x,clientY:y});el.dispatchEvent(new TouchEvent('touchstart',{bubbles:true,touches:[t(300)],changedTouches:[t(300)]}));el.dispatchEvent(new TouchEvent('touchend',{bubbles:true,touches:[],changedTouches:[t(180)]}))},{y:bb.y+10});
 await pg.waitForTimeout(200);console.log('row open',await r.evaluate(e=>e.classList.contains('open')),'fav visible',await r.$eval('.favbtn',e=>getComputedStyle(e).display).catch(()=>'nofav'));
 await shot('7swipe');
 await r.evaluate(e=>e.classList.remove('open'));
 await pg.click('#pkl .prow .rk');await pg.waitForTimeout(500);console.log('bio open',await pg.evaluate(()=>!!document.querySelector('#bioHost')&&!document.querySelector('#bioHost').hidden&&document.querySelector('#bioHost').innerHTML.length>100));
 await shot('8bio');
}
await pg.goto('http://localhost:8765/index.html');await pg.waitForTimeout(600);
for(const t of ['board','top','mocks']){await pg.click(`.bnav [data-tab="${t}"]`);await pg.waitForTimeout(400);await shot('t_'+t)}
await pg.click('.bnav [data-tab="board"]');await pg.click('#bSeg [data-boardview="stats"], #bSeg button:nth-child(2)');await pg.waitForTimeout(300);await shot('t_boardstats');
await pg.click('#p-board th[data-sort]:nth-of-type(5)');await pg.waitForTimeout(150);await pg.click('#p-board th[data-sort]:nth-of-type(5)');await pg.waitForTimeout(150);console.log('sorted',await pg.$eval('#p-board th[aria-sort]',e=>e.textContent+' '+e.getAttribute('aria-sort')).catch(()=>'none'));await shot('t_boardsort');
await pg.click('.bnav [data-tab="top"]');console.log('top items',await pg.$$eval('#topList li',l=>l.length));
await pg.click('#tSeg button:nth-child(2)');await pg.waitForTimeout(300);await shot('t_topstats');
console.log('pdf link',await pg.getAttribute('#p-top a[href="top125.pdf"]','href'));
const res=await pg.request.get('http://localhost:8765/top125.pdf');console.log('pdf status',res.status(),res.headers()['content-type']);
await pg.click('.bnav [data-tab="mocks"]');await pg.waitForTimeout(300);console.log('curmock',(await pg.textContent('#curMock')).slice(0,150));
console.log('ERRS',errs);
// desktop
const d=await b.newContext({viewport:{width:1280,height:900},serviceWorkers:'block'});const dp=await d.newPage();dp.on('pageerror',e=>errs.push('D '+e.message));
await dp.goto('http://localhost:8765/index.html');await dp.waitForTimeout(600);await dp.screenshot({path:'/home/claude/tests/d_draft.png'});
await dp.click('.bnav [data-tab="top"]');await dp.waitForTimeout(300);await dp.screenshot({path:'/home/claude/tests/d_top.png'});
console.log('ERRS2',errs);await b.close()})();
