# Badges + weekly scoring for every player in the pool. Writes /home/claude/fantasy/badges.json keyed by player id.
import json, pandas as pd, numpy as np
P=json.load(open('/home/claude/fantasy/proj.json'))
s=pd.read_csv('/home/claude/nfldata/stats26.csv',low_memory=False)
if 'season_type' in s: s=s[s.season_type=='REG']
TH={'QB':(12,18,30,35),'RB':(6,12,25,30),'WR':(6,12,25,30),'TE':(4,9,20,24)}  # bust, start, boom, huge week
maxwk=int(s.week.max())
ppg_rank={};ts_rank={}
for pos in TH:
    L=sorted([x for x in P if x['pos']==pos and x['g']>=4],key=lambda x:-x['ppg'])
    for i,x in enumerate(L): ppg_rank[x['pid']]=i+1
    L=sorted([x for x in P if x['pos']==pos and x['g']>=3 and x.get('ts') is not None],key=lambda x:-x['ts'])
    for i,x in enumerate(L): ts_rank[x['pid']]=i+1
byid={k:g.sort_values('week') for k,g in s.groupby('player_id')}
out={}
# Breakout: hand-picked by Jared (hyped, high ceiling, upside not fully shown yet). Edit this list to change it.
BREAKOUT=['Luther Burden III','Bhayshul Tuten','Jeremiah Smith','Jonah Coleman','Emeka Egbuka','DeVonta Smith','Quinshon Judkins','Omar Cooper Jr.','Jordyn Tyson','Denzel Boston','KC Concepcion','Caleb Douglas','Charlie Becker']
# Bust?: players Jared flags by hand in addition to the stat rule
BUST_ADD=['Ladd McConkey','Carnell Tate','RJ Harvey','Michael Pittman','Bo Nix']
# other hand-added badges
VOLATILE_ADD=['DK Metcalf']
CEILING_ADD=['Brenton Strange']
def ordn(n): return f"{n}{'th' if 10<=n%100<=20 else {1:'st',2:'nd',3:'rd'}.get(n%10,'th')}"
def r1(v): return float(round(v,1))
for x in P:
    pid=x['pid'];pos=x['pos'];g=byid.get(pid)
    if g is None:  # fall back to name match
        m=s[s.player_display_name==x['name']]
        g=m.sort_values('week') if len(m) else None
    wk=[] if g is None else [[int(r.week),str(r.opponent_team),r1(r.fantasy_points_ppr)] for r in g.itertuples()]
    v=np.array([w[2] for w in wk]);B=[];W={}
    p25=x['ppr25']/x['g25'] if x.get('g25') else None
    if len(v)>=4:
        b,st,bm,hi=TH[pos];m=v.mean();cv=v.std()/m if m>0 else 9;start=(v>=st).mean();bust=(v<b).mean();boom=int((v>=bm).sum())
        if len(v)>=5 and start>=.65 and cv<=.40: B.append('consistent');W['consistent']=f"{int((v>=st).sum())} of {len(v)} games with {st}+ pts"
        if boom>=2 or v.max()>=hi: B.append('ceiling');W['ceiling']=f"{boom} game{'s' if boom!=1 else ''} of {bm}+ · season high {v.max():.1f}"
        under_st=(v<st).mean()
        if (cv>=.65 and boom>=1 and bust>=.3) or (cv>=.5 and boom>=1 and under_st>=.35):
            B.append('volatile');W['volatile']=f"Weekly range {v.min():.1f} to {v.max():.1f} pts · {boom} boom week{'s' if boom!=1 else ''}, {int((v<st).sum())} under {st}"
        if bust>=.35: B.append('floor');W['floor']=f"Under {b} pts in {int((v<b).sum())} of {len(v)} games"
        if 'consistent' in B and x['rank']<=60 and (x.get('age') or 99)<=29 and p25 and abs(m-p25)/p25<=.2 and len(v)>=maxwk-2:
            B.insert(0,'safety');W['safety']=f"{p25:.1f} PPG in 2025, {m:.1f} in 2026, rarely misses games"
        l4=v[-4:].mean() if len(v)>=6 else None;pr=ppg_rank.get(pid)
        if 55<=x['rank']<=220 and m>=.85*st and ((pr and pr<=x['prank']-8) or (l4 and l4>=1.3*m and l4>=st)):
            B.append('sleeper');W['sleeper']=(f"{pos}{pr} in points per game but {pos}{x['prank']} on the board" if pr and pr<=x['prank']-8 else f"Last 4 games: {l4:.1f} PPG vs {m:.1f} for the season")
        if p25 and p25>=10 and m<=.8*p25 and p25-m>=3: B.append('under');W['under']=f"{m:.1f} PPG, down from {p25:.1f} in 2025"
    # Bust?: severe drop from 2025 (min 3 games): 2025 PPG 12+, now 65% or less of it and 5+ PPG lower. Replaces Underperformer.
    if len(v)>=3 and p25 and p25>=12:
        m=v.mean()
        if m<=.65*p25 and p25-m>=5:
            B=[k for k in B if k!='under'];W.pop('under',None)
            B.append('bust');W['bust']=f"{m:.1f} PPG in 2026 vs {p25:.1f} in 2025 ({round(100*(1-m/p25))}% drop)"
    # Volume machine: heavy weekly opportunity (min 4 games)
    if x['g']>=4 and len(v)>=4:
        G=x['g'];car=(x.get('car') or 0)/G;tg=(x.get('tgt') or 0)/G;att=(x.get('att') or 0)/G;ts=x.get('ts') or 0
        vol=None
        if pos=='QB' and att+car>=38: vol=f"{att+car:.1f} pass attempts + carries per game"
        if pos=='RB' and car+tg>=20: vol=f"{car+tg:.1f} touches per game ({car:.1f} carries, {tg:.1f} targets)"
        if pos=='WR' and (tg>=9.5 or ts>=30): vol=f"{tg:.1f} targets per game · {ts}% target share"
        if pos=='TE' and (tg>=7.5 or ts>=24): vol=f"{tg:.1f} targets per game · {ts}% target share"
        if vol:
            B.append('volume');W['volume']=vol
            # Volume machine replaces High ceiling
            if 'ceiling' in B: B.remove('ceiling');W.pop('ceiling',None)
    if x['name'] in BUST_ADD and 'bust' not in B:
        B=[k for k in B if k!='under'];W.pop('under',None);B.append('bust')
        if x['g'] and p25: W['bust']=f"{x['ppg']} PPG in 2026 vs {p25:.1f} in 2025 ({round(100*(1-x['ppg']/p25))}% drop). Flagged by hand"
        elif x['g']: W['bust']=f"{x['ppg']} PPG in {x['g']} games, below expectations. Flagged by hand"
        else: W['bust']="Flagged by hand"
    if x['name'] in VOLATILE_ADD and 'volatile' not in B and len(v):
        B.append('volatile');W['volatile']=f"Weekly range {v.min():.1f} to {v.max():.1f} pts. Flagged by hand"
    if x['name'] in CEILING_ADD and 'ceiling' not in B and len(v):
        B.append('ceiling');W['ceiling']=f"Season high {v.max():.1f} pts. Flagged by hand"
    if x['name'] in BREAKOUT:
        B.append('breakout')
        if not x['g']: W['breakout']="2027 rookie with top-of-class buzz and a big ceiling"
        else:
            yr=2026-int(x.get('rookie') or 2026)+1
            extra=f" · {x['ts']}% target share" if pos in ('WR','TE') and x.get('ts') else (f" · {((x.get('car') or 0)+(x.get('tgt') or 0))/x['g']:.1f} touches per game" if pos=='RB' else "")
            W['breakout']=f"{ordn(yr)} NFL season: {x['ppg']} PPG in {x['g']} games{extra}. Upside not fully tapped yet"
    if 'bust' in B and 'sleeper' in B: B.remove('sleeper');W.pop('sleeper',None)
    order=['safety','consistent','volume','breakout','ceiling','sleeper','bust','volatile','floor','under']
    B=sorted(B,key=order.index)
    rpg=round((x.get('rec') or 0)/x['g'],2) if x['g']>=3 else {'QB':0,'RB':2.0,'WR':3.5,'TE':3.0}[pos]
    out[pid]={'b':B,'w':W,'wk':wk,'pr':ppg_rank.get(pid),'tr':ts_rank.get(pid),'rpg':rpg}
json.dump(out,open('/home/claude/fantasy/badges.json','w'),separators=(',',':'))
from collections import Counter
print('badges',dict(Counter(b for o in out.values() for b in o['b'])),'players',len(out))
