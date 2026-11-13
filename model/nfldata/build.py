import pandas as pd, numpy as np, json, math
s=pd.read_csv('stats26.csv',low_memory=False); s=s[s.position.isin(['QB','RB','WR','TE'])]
s25=pd.read_csv('stats25.csv',low_memory=False); s25=s25[s25.position.isin(['QB','RB','WR','TE'])]
p=pd.read_csv('players.csv',low_memory=False).drop_duplicates('gsis_id').set_index('gsis_id')
sn=pd.read_csv('snaps26.csv',low_memory=False)
tt=s.groupby(['game_id','team']).targets.sum().rename('team_tgt').reset_index()
s=s.merge(tt,on=['game_id','team'])
A=s.sort_values('week').groupby('player_id').agg(name=('player_display_name','first'),pos=('position','first'),team=('team','last'),
 g=('game_id','nunique'),ppr=('fantasy_points_ppr','sum'),cmp=('completions','sum'),att=('attempts','sum'),pyd=('passing_yards','sum'),ptd=('passing_tds','sum'),pint=('passing_interceptions','sum'),
 car=('carries','sum'),ryd=('rushing_yards','sum'),rtd=('rushing_tds','sum'),tgt=('targets','sum'),rec=('receptions','sum'),yds=('receiving_yards','sum'),tdr=('receiving_tds','sum'),
 team_tgt=('team_tgt','sum'),ays=('air_yards_share','mean'),teams=('team',lambda x:list(dict.fromkeys(x)))).reset_index()
A['ts']=np.where(A.team_tgt>0,A.tgt/A.team_tgt,0)
A['ppg']=A.ppr/A.g
# snaps: map via pfr_id
p2=p.reset_index()[['gsis_id','pfr_id']].dropna()
sn=sn[sn.game_type=='REG'].merge(p2,left_on='pfr_player_id',right_on='pfr_id')
snp=sn.groupby('gsis_id').offense_pct.mean()
A['snap']=A.player_id.map(snp)
B=s25.set_index('player_id')
def g25(pid,c):
    try: return B.loc[pid,c]
    except KeyError: return None
TEAMFIX={'LA':'LAR'}
out=[]
for _,r in A.iterrows():
    pid=r.player_id
    if pid not in p.index: continue
    b=p.loc[pid]
    if r.ppr<8 and (g25(pid,'fantasy_points_ppr') or 0)<60: continue
    out.append(dict(pid=pid,name=r['name'],pos=r.pos,team=TEAMFIX.get(r.team,r.team),teams=[TEAMFIX.get(t,t) for t in r.teams],
      birth=b.birth_date,ht=b.height,wt=b.weight,college=b.college_name,rookie=b.rookie_season,status=b.status,draft=[b.draft_year,b.draft_round,b.draft_pick],
      g=int(r.g),ppr=round(r.ppr,1),ppg=round(r.ppg,1),cmp=int(r.cmp),att=int(r.att),pyd=int(r.pyd),ptd=int(r.ptd),pint=int(r.pint),car=int(r.car),ryd=int(r.ryd),rtd=int(r.rtd),
      tgt=int(r.tgt),rec=int(r.rec),yds=int(r.yds),tdr=int(r.tdr),ts=round(r.ts*100,1),ays=None if pd.isna(r.ays) else round(r.ays*100,1),snap=None if pd.isna(r.snap) else round(r.snap*100),
      g25=None if g25(pid,'games') is None else int(g25(pid,'games')),ppr25=g25(pid,'fantasy_points_ppr'),
      l25=dict(pyd=g25(pid,'passing_yards'),ptd=g25(pid,'passing_tds'),ryd=g25(pid,'rushing_yards'),rtd=g25(pid,'rushing_tds'),rec=g25(pid,'receptions'),yds=g25(pid,'receiving_yards'),tdr=g25(pid,'receiving_tds'),ts=g25(pid,'target_share'))))
# players with 2025 production but no 2026 games
ids=set(A.player_id)
for pid,r in B.iterrows():
    if pid in ids or r.fantasy_points_ppr<110 or pid not in p.index: continue
    b=p.loc[pid]
    out.append(dict(pid=pid,name=r.player_display_name,pos=r.position,team=TEAMFIX.get(b.latest_team,b.latest_team),teams=[],birth=b.birth_date,ht=b.height,wt=b.weight,college=b.college_name,rookie=b.rookie_season,status=b.status,draft=[b.draft_year,b.draft_round,b.draft_pick],
      g=0,ppr=0,ppg=0,cmp=0,att=0,pyd=0,ptd=0,pint=0,car=0,ryd=0,rtd=0,tgt=0,rec=0,yds=0,tdr=0,ts=0,ays=None,snap=None,g25=int(r.games),ppr25=r.fantasy_points_ppr,
      l25=dict(pyd=r.passing_yards,ptd=r.passing_tds,ryd=r.rushing_yards,rtd=r.rushing_tds,rec=r.receptions,yds=r.receiving_yards,tdr=r.receiving_tds,ts=r.target_share)))
def clean(o):
    if isinstance(o,dict): return {k:clean(v) for k,v in o.items()}
    if isinstance(o,list): return [clean(v) for v in o]
    if isinstance(o,(float,np.floating)): return None if math.isnan(o) else float(o)
    if isinstance(o,(np.integer,)): return int(o)
    return o
json.dump(clean(out),open('/home/claude/fantasy/raw.json','w'))
print(len(out))
