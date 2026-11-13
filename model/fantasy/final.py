import json
exec(open('proj.py').read())
P=[x for x in P][:300]
def ht(h):
    if not h: return '—'
    h=int(h); return f"{h//12}-{h%12}"
def n(v): return 0 if v is None else v
def fmt(v): return f"{int(v):,}"
pos_lists={k:[x for x in P if x['pos']==k and x['g']>=3] for k in ['QB','RB','WR','TE']}
def rk(x,key,pos=None):
    L=sorted(pos_lists[pos or x['pos']],key=lambda y:-y[key]); 
    for i,y in enumerate(L):
        if y is x: return i+1
    return None
for x in P:
    x['tpg']=x['tgt']/x['g'] if x['g'] else 0
    x['cpg']=x['car']/x['g'] if x['g'] else 0
    x['rpg']=x['ryd']/x['g'] if x['g'] else 0
out=[]
ordn=lambda i:f"{i}{'th' if 11<=i%100<=13 else {1:'st',2:'nd',3:'rd'}.get(i%10,'th')}"
for x in P:
    pos=x['pos']; g=x['g']
    if x.get('col26'):
        line=x['col26']; prev=''
    elif g==0:
        line='No 2026 games'
    elif pos=='QB':
        line=f"{fmt(x['pyd'])} pass yds · {x['ptd']} TD · {x['pint']} INT · {x['ryd']} rush yds · {x['rtd']} rush TD"
    elif pos=='RB':
        line=f"{x['car']} car · {fmt(x['ryd'])} yds · {x['rtd']} TD · {x['rec']} rec · {x['yds']} rec yds · {x['tdr']} rec TD"
    else:
        line=f"{x['rec']} rec · {fmt(x['yds'])} yds · {x['tdr']} TD on {x['tgt']} targets"
    l=x.get('l25') or {}
    if x['g25']:
        if pos=='QB': prev=f"{x['g25']} g · {fmt(n(l.get('pyd')))} pass yds · {int(n(l.get('ptd')))} TD · {fmt(n(l.get('ryd')))} rush yds · {round(x['ppr25']/x['g25'],1)} PPR/G"
        elif pos=='RB': prev=f"{x['g25']} g · {fmt(n(l.get('ryd')))} rush yds · {int(n(l.get('rtd')))+int(n(l.get('tdr')))} TD · {int(n(l.get('rec')))} rec · {round(x['ppr25']/x['g25'],1)} PPR/G"
        else: prev=f"{x['g25']} g · {int(n(l.get('rec')))} rec · {fmt(n(l.get('yds')))} yds · {int(n(l.get('tdr')))} TD"+(f" · {round(l['ts']*100,1)}% tgt share" if l.get('ts') else "")+f" · {round(x['ppr25']/x['g25'],1)} PPR/G"
    elif not x.get('col26'): prev='Rookie in 2026' if x['rookie']==2026 else ''
    # strengths
    st=[]
    if x.get('strg'): st.append(x['strg'])
    elif g>=3:
        if pos in('WR','TE'):
            r=rk(x,'ts'); st.append(f"{x['ts']}% target share ({ordn(r)} among {pos}s)")
            if x['ays']: st.append(f"{x['ays']}% of team air yards")
            if x['tgt'] and x['rec']/x['tgt']>=.75: st.append(f"Sure hands: {round(100*x['rec']/x['tgt'])}% catch rate")
            if x['tdr']>=4: st.append(f"Red-zone threat: {x['tdr']} TDs in {g} games")
            if x['rec'] and x['yds']/x['rec']>=15: st.append(f"Big-play ability: {round(x['yds']/x['rec'],1)} yds per catch")
        elif pos=='RB':
            if x['cpg']>=16: st.append(f"Workhorse: {round(x['cpg'],1)} carries per game")
            if x['car']>=25 and x['ryd']/x['car']>=5: st.append(f"Efficient: {round(x['ryd']/x['car'],1)} yds per carry")
            if x['tpg']>=4: st.append(f"Passing-down role: {round(x['tpg'],1)} targets per game ({x['ts']}% share)")
            if x['rtd']+x['tdr']>=5: st.append(f"Scoring role: {x['rtd']+x['tdr']} TDs in {g} games")
        elif pos=='QB':
            if x['rpg']>=25: st.append(f"Rushing floor: {round(x['rpg'])} rush yds per game, {x['rtd']} rush TDs")
            if x['ptd']>=2*max(1,x['pint']): st.append(f"Ball security: {x['ptd']} TD to {x['pint']} INT")
            if x['att'] and x['pyd']/x['att']>=8: st.append(f"Efficient: {round(x['pyd']/x['att'],1)} yds per attempt")
            if x['pyd']/g>=270: st.append(f"Volume: {round(x['pyd']/g)} pass yds per game")
        if x['snap'] and x['snap']>=80 and pos!='QB': st.append(f"Every-down player: {x['snap']}% of snaps")
        if not st: st.append(f"{x['ppg']} PPR points per game in 2026")
    elif x['g25']: st.append(f"Produced {round(x['ppr25']/x['g25'],1)} PPR/G in 2025")
    trend='flat'
    if g>=3 and x['g25'] and x['g25']>=6:
        d=x['ppg']-x['ppr25']/x['g25']
        trend='up' if d>=3 else 'down' if d<=-3 else 'flat'
    elif g>=3 and x['rookie']==2026 and x['ppg']>=10: trend='up'
    dr=x['draft']
    draft=(f"{int(dr[0])} Rd {int(dr[1])}, No. {int(dr[2])}" if dr and dr[0] and dr[1] and dr[2] else ("Undrafted" if x['rookie'] and x['rookie']<2027 else ""))
    if x['rookie']==2027: draft=f"Projected 2027 Rd {dr[1]}, No. {dr[2]} (base mock)"
    out.append([x['pid'],x['name'],pos,x['team'],x['age'],ht(x['ht']),int(x['wt']) if x['wt'] else 0,x['college'] or '',draft,
      g,x['ppr'],x['ppg'],line,x['ts'] if pos in('WR','TE','RB') and g else None,x['snap'],prev,round(x['proj'],1),round(x['pts']),x['rank'],x['prank'],x['note'],st,trend,
      2027-int(x['rookie']) if x['rookie'] else None])
json.dump(out,open('players.json','w'),ensure_ascii=False)
# breakouts
bk=[x for x in P if x['g']>=4 and ((x['g25'] or 0)>=6) ]
bk.sort(key=lambda x:-(x['ppg']-x['ppr25']/x['g25']))
rk26=[x for x in P if x['g']>=4 and x['rookie']==2026 and (x['pos']!='QB' or x['ppg']>=15)]; rk26.sort(key=lambda x:-x['ppg'])
B=[[x['name'],x['pos'],x['team'],round(x['ppr25']/x['g25'],1),x['ppg'],x['ts']] for x in bk[:10]]
R=[[x['name'],x['pos'],x['team'],x['ppg'],x['ts'],x['g']] for x in rk26[:6]]
json.dump({'b':B,'r':R},open('breakouts.json','w'),ensure_ascii=False)
for b in B: print(b)
for r in R: print(r)
print(len(out))
print(out[0])

import subprocess; subprocess.run(['python3','/home/claude/fantasy/badges.py']); subprocess.run(['python3','/home/claude/fantasy/top125.py'])
