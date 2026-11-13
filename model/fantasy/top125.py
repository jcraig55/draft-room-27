# Builds the Top 125 PDF + page from players.json. Run after final.py.
import json,html,glob,os,datetime
for _f in glob.glob('/home/claude/downloads/draft-room-27-top-125*.pdf'): os.remove(_f)
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import datetime
DATE=datetime.date.today().strftime('%b %-d, %Y')
import pandas as _pd
WEEK=int(_pd.read_csv('/home/claude/nfldata/stats26.csv',usecols=['week']).week.max())
_pj={x['name']:x for x in json.load(open('/home/claude/fantasy/proj.json'))}
d=[]
for i,r in enumerate(json.load(open('/home/claude/fantasy/players.json'))[:125]):
    x=_pj.get(r[1],{}); mv=0
    d.append([r[1],r[2],r[3],mv,r[0]])
SUB=f"2027 redraft  ·  Full PPR  ·  16 teams  ·  QB / RB / 2 WR / TE / 2 FLEX  ·  Updated {DATE}"
W,H=letter
c=canvas.Canvas(f'/home/claude/downloads/draft-room-27-top-125 ({datetime.date.today().strftime("%b %-d")}).pdf',pagesize=letter)
c.setTitle("Draft Room '27 Top 125")
ink=HexColor('#13202B'); mute=HexColor('#6b7280'); rule=HexColor('#9FCBEA')
pc={'QB':HexColor('#138A4E'),'RB':HexColor('#1E407C'),'WR':HexColor('#BB0000'),'TE':HexColor('#FFD100')}
pink={'QB':HexColor('#FFFFFF'),'RB':HexColor('#FFFFFF'),'WR':HexColor('#FFFFFF'),'TE':HexColor('#1A1400')}
m=36
c.setFillColor(ink); c.setFont('Helvetica-Bold',20); c.drawString(m,H-m-14,"Draft Room ’27 — Top 125")
c.setFont('Helvetica',9.5); c.setFillColor(mute); c.drawString(m,H-m-30,SUB)
c.setStrokeColor(rule); c.line(m,H-m-40,W-m,H-m-40)
cols=3; gap=14; cw=(W-2*m-gap*(cols-1))/cols; top=H-m-58; rh=15.6; per=42
UPB,UPT,DNB,DNT=HexColor('#dcfce7'),HexColor('#15803d'),HexColor('#fee2e2'),HexColor('#b91c1c')
for i,(n,p,t,mv,_id) in enumerate(d):
    x=m+(i//per)*(cw+gap); y=top-(i%per)*rh
    if mv>0: c.setFillColor(UPB); c.rect(x,y-4.5,cw,rh,stroke=0,fill=1)
    elif mv<0: c.setFillColor(DNB); c.rect(x,y-4.5,cw,rh,stroke=0,fill=1)
    elif (i%per)%2==0: c.setFillColor(HexColor('#F2F8FC')); c.rect(x,y-4.5,cw,rh,stroke=0,fill=1)
    c.setFillColor(ink); c.setFont('Helvetica-Bold',8.5); c.drawRightString(x+17,y,str(i+1))
    c.setFillColor(pc[p]); c.roundRect(x+22,y-2.5,19,10.5,2.5,stroke=0,fill=1)
    c.setFillColor(pink[p]); c.setFont('Helvetica-Bold',6.8); c.drawCentredString(x+31.5,y,p)
    nm=n
    while c.stringWidth(nm,'Helvetica',8.6)>cw-75: nm=nm[:-1]
    c.setFillColor(ink); c.setFont('Helvetica',8.6); c.drawString(x+46,y,nm)
    c.setFillColor(mute); c.setFont('Helvetica',7.8); c.drawRightString(x+cw-4,y,t)
    if mv:
        col=UPT if mv>0 else DNT; lbl=str(abs(mv)); c.setFillColor(col); c.setFont('Helvetica-Bold',7)
        lx=x+cw-26-c.stringWidth(lbl,'Helvetica-Bold',7); c.drawString(lx,y,lbl)
        pth=c.beginPath(); tx=lx-7
        if mv>0: pth.moveTo(tx,y-0.5); pth.lineTo(tx+5,y-0.5); pth.lineTo(tx+2.5,y+5)
        else: pth.moveTo(tx,y+5); pth.lineTo(tx+5,y+5); pth.lineTo(tx+2.5,y-0.5)
        pth.close(); c.drawPath(pth,stroke=0,fill=1)
c.setFont('Helvetica',7.5); c.setFillColor(mute)
c.drawString(m,m-8,"Rookie teams are projected landing spots. Rankings include manual adjustments.")
c.save()
# web page: reuse existing page shell, swap list + date
pg=open('/home/claude/fantasy/top125.html',encoding='utf-8').read()
def _mv(mv): return '' if not mv else f'<span class="mv">{"▲" if mv>0 else "▼"}{abs(mv)}</span>'
def _cl(mv): return ' class="up"' if mv>0 else (' class="dn"' if mv<0 else '')
rows=''.join(f'<li{_cl(mv)} data-p="{p}" data-id="{_id}"><span class="rk">{i+1}</span><span class="pos {p}">{p}</span><span class="nm">{html.escape(n)}</span>{_mv(mv)}<span class="tm">{t}</span><button class="fav" data-fav="{_id}" aria-pressed="false" aria-label="Add {html.escape(n)} to favorites">♡</button></li>' for i,(n,p,t,mv,_id) in enumerate(d))
a=pg.index('<ol>')+4; b=pg.index('</ol>')
pg=pg[:a]+rows+pg[b:]
import re
pg=re.sub(r'Updated [A-Z][a-z]{2} \d{1,2}, \d{4}','Updated '+DATE,pg)
open('/home/claude/fantasy/top125.html','w',encoding='utf-8').write(pg)
print('top125 rebuilt',DATE)

# ---------- STATS PAGE ----------
MING=3
_pr={}
for _pos in ['QB','RB','WR','TE']:
    _L=sorted([y for y in _pj.values() if y['pos']==_pos and y['g']>=MING],key=lambda y:-y['ppg'])
    for _i,_y in enumerate(_L): _pr[_y['name']]=_i+1
_rows=[]
for i,r in enumerate(json.load(open('/home/claude/fantasy/players.json'))[:125]):
    x=_pj[r[1]]
    p26=round(x['ppg'],1) if x['g'] else None
    p25=round(x['ppr25']/x['g25'],1) if x.get('g25') else None
    _rows.append(dict(rk=i+1,n=x['name'],p=x['pos'],pr=_pr.get(x['name']),t=x['team'],g=x['g'],a=p26,b=p25,g25=x.get('g25') or 0,j=round(x['proj'],1)))
def _f(v): return '<span class="na">—</span>' if v is None else f'{v:.1f}'
_rows.sort(key=lambda r:-(r['a'] if r['a'] is not None else -1))
trs=''.join(f'<tr data-p="{r["p"]}"><td class="n">{r["rk"]}</td><td class="pl"><span class="pos {r["p"]}">{r["p"]}</span>{html.escape(r["n"])}</td><td class="n" data-v="{r["pr"] if r["pr"] else 999}">{(r["p"]+str(r["pr"])) if r["pr"] else '<span class="na">—</span>'}</td><td>{r["t"]}</td><td class="n" data-v="{r["a"] if r["a"] is not None else -1}">{_f(r["a"])}<small>{r["g"]} g</small></td><td class="n" data-v="{r["b"] if r["b"] is not None else -1}">{_f(r["b"])}<small>{r["g25"]} g</small></td><td class="n">{r["j"]:.1f}</td></tr>' for r in _rows)
css=pg[pg.index('<style>'):pg.index('</style>')+8]
sp=f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Draft Room ’27 Player Stats</title>
{css}
<style>
.wrap{{overflow-x:auto;border:1px solid var(--rule);border-radius:18px;background:var(--card)}}
table{{border-collapse:collapse;width:100%;min-width:640px;font-size:13.5px}}
th{{text-align:left;font-size:11.5px;text-transform:uppercase;letter-spacing:.04em;color:var(--mute);font-weight:600;padding:10px 10px;border-bottom:1px solid var(--rule);cursor:pointer;white-space:nowrap;user-select:none;position:sticky;top:0;background:var(--card)}}
th.n,td.n{{text-align:right}}th[aria-sort="ascending"]::after{{content:" ▲"}}th[aria-sort="descending"]::after{{content:" ▼"}}
td{{padding:7px 10px;border-bottom:1px solid var(--rule);white-space:nowrap;font-variant-numeric:tabular-nums}}tr:last-child td{{border-bottom:0}}tbody tr:nth-child(odd){{background:var(--stripe)}}
td.pl{{font-weight:500}}td.pl .pos{{display:inline-block;width:28px;margin-right:8px;font-size:10px;padding:1px 0}}
td small{{display:block;font-size:10.5px;color:var(--mute)}}.na{{color:var(--mute)}}tr[hidden]{{display:none}}
</style></head><body><main>
<nav class="nav"><a href="index.html">Top 125</a><a href="stats.html" aria-current="page">Player stats</a></nav>
<h1>Player stats — Top 125</h1>
<p class="sub">Sorted by 2026 fantasy points per game (full PPR)  ·  Updated {DATE}  ·  Tap a column to sort</p>
<div class="f" role="group" aria-label="Filter by position"><button aria-pressed="true" data-f="ALL">All</button><button aria-pressed="false" data-f="QB">QB</button><button aria-pressed="false" data-f="RB">RB</button><button aria-pressed="false" data-f="WR">WR</button><button aria-pressed="false" data-f="TE">TE</button></div>
<div class="wrap"><table><thead><tr><th class="n" data-k="0" data-t="n">Board rank</th><th data-k="1">Player</th><th class="n" data-k="2" data-t="n">Pos rank (PPG)</th><th data-k="3">Team</th><th class="n" data-k="4" data-t="n" aria-sort="descending">2026 PPR/G</th><th class="n" data-k="5" data-t="n">2025 PPR/G</th><th class="n" data-k="6" data-t="n">2027 proj/G</th></tr></thead>
<tbody>{trs}</tbody></table></div>
<p class="note">2026 stats through Week {WEEK}. 2027 projection is the model's per-game estimate behind the rankings. Pos rank is the player's spot at his position by 2026 points per game, among all players with at least 3 games (— = fewer than 3). Board rank is his spot on the draft board.</p>
</main><script>
const tb=document.querySelector('tbody');
document.querySelectorAll('.f button').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.f button').forEach(x=>x.setAttribute('aria-pressed',x===b));const f=b.dataset.f;tb.querySelectorAll('tr').forEach(r=>r.hidden=!(f==='ALL'||r.dataset.p===f))}});
document.querySelectorAll('th').forEach(th=>th.onclick=()=>{{
 const k=+th.dataset.k,num=th.dataset.t==='n',cur=th.getAttribute('aria-sort');
 const dir=cur==='descending'?'ascending':(cur==='ascending'?'descending':(num&&k>=4?'descending':'ascending'));
 document.querySelectorAll('th').forEach(x=>x.removeAttribute('aria-sort'));th.setAttribute('aria-sort',dir);
 const val=r=>{{const c=r.children[k];return num?parseFloat(c.dataset.v??c.textContent):c.textContent.toLowerCase()}};
 [...tb.rows].sort((a,b)=>{{const x=val(a),y=val(b);return (x<y?-1:x>y?1:0)*(dir==='ascending'?1:-1)}}).forEach(r=>tb.appendChild(r));
}});
</script></body></html>"""
open('/home/claude/fantasy/stats.html','w',encoding='utf-8').write(sp)
