# Rest-of-season trade values for the Trade analyzer (2026 season), rebuilt with every weekly stats update.
# Inputs: live players.json / badges.json (same data as the Player stats page), nflverse 2026 weekly stats,
# 2026 schedule (nfldata/sched/games.csv) and injury reports (nfldata/injuries26.csv).
import json,os,pandas as pd
F='/home/claude/fantasy/';N='/home/claude/nfldata/'
POS=['QB','RB','WR','TE']
BASE={'QB':13,'RB':8,'WR':8,'TE':6}           # prior for players with few games and no 2025 line
REPL={'QB':20,'RB':44,'WR':58,'TE':20}         # replacement level in a 16-team QB/RB/2WR/TE/2FLEX league (ranked by ROS PPG)
K=3                                            # games of prior blended into 2026 PPG
SOS_W=0.25                                     # "slight" schedule effect: 25% of the raw matchup difference
SOS_CAP=0.08                                   # never more than +/-8%
def qb_disc(r): return 0.05+0.15*min(1,(r-1)/14)   # QB discount ladder by QB rank
STYLE_W=0.25                                   # Safe/Upside value styles shift ROS PPG 25% toward floor/ceiling
def build():
    P=json.load(open(F+'players.json'));B=json.load(open(F+'badges.json'))
    st=pd.read_csv(N+'stats26.csv',usecols=['player_id','position','week','season_type','team','opponent_team','fantasy_points_ppr'],low_memory=False)
    st=st[(st.season_type=='REG')&st.position.isin(POS)]
    # fantasy points allowed per game by each defense to each position
    g=st.groupby(['opponent_team','position','week']).fantasy_points_ppr.sum().reset_index()
    da=g.groupby(['opponent_team','position']).fantasy_points_ppr.mean()
    lg=g.groupby('position').fantasy_points_ppr.mean()
    fac={(d,p):v/lg[p] for (d,p),v in da.items()}
    sc=pd.read_csv(N+'sched/games.csv');sc=sc[(sc.season==2026)&(sc.game_type=='REG')]
    left=sc[sc.home_score.isna()]
    played_wk=int(sc[sc.home_score.notna()].week.max()) if sc.home_score.notna().any() else 0
    opp={}
    for _,r in left.iterrows():
        opp.setdefault(r.home_team,[]).append((int(r.week),r.away_team));opp.setdefault(r.away_team,[]).append((int(r.week),r.home_team))
    teams=set(sc.home_team)|set(sc.away_team)
    tmap=lambda t:'LA' if t=='LAR' and 'LA' in teams else t
    inj={}
    if os.path.exists(N+'injuries26.csv'):
        I=pd.read_csv(N+'injuries26.csv',low_memory=False);I=I[I.week==I.week.max()] if I.week.max()>played_wk else I.iloc[0:0]  # only reports for the upcoming week
        for _,r in I.iterrows():
            if isinstance(r.report_status,str) and r.report_status in('Out','Doubtful','Questionable'): inj[r.gsis_id]=(r.report_status,str(r.report_primary_injury) if isinstance(r.report_primary_injury,str) else '')
    rows=[]
    for r in P:
        pid,name,pos,team,gm,ppg=r[0],r[1],r[2],r[3],r[9] or 0,r[11] or 0
        if pos not in POS or gm==0: continue
        b=B.get(pid,{});p25=b.get('p25')
        prior=p25 if p25 else BASE[pos]
        adj=(gm*ppg+K*prior)/(gm+K)
        sched=sorted(opp.get(tmap(team),[]))
        raw=[fac.get((o,pos),1.0) for _,o in sched]
        f=sum(raw)/len(raw) if raw else 1.0
        mult=max(1-SOS_CAP,min(1+SOS_CAP,1+SOS_W*(f-1)))
        wk=sorted(w[2] for w in b.get('wk',[]))
        c=round(sum(wk[-3:])/3,1) if len(wk)>=4 else None   # ceiling: average of his 3 best games
        f=round(sum(wk[:3])/3,1) if len(wk)>=4 else None    # floor: average of his 3 worst games
        rows.append({'id':pid,'name':name,'pos':pos,'team':team,'g':gm,'ppg':round(ppg,1),'adj':round(adj,2),'ros':round(adj*mult,2),'left':len(sched),'sos':round(mult,3),
                     'opp':[o for _,o in sched],'inj':inj.get(pid),'c':c,'f':f})
    # value over replacement for the rest of the season, scaled 0-100.
    # Three styles: Balanced (val), Safe (vs: ROS PPG shifted toward floor), Upside (vu: toward ceiling). All on the Balanced scale.
    # players with under 4 games use their position's typical ceiling/floor ratio, so styles move everyone consistently
    RAT={}
    for pos in POS:
        L=[x for x in rows if x['pos']==pos and x['c'] is not None and x['adj']>0]
        RAT[pos]=(sum(x['c']/x['adj'] for x in L)/len(L),sum(x['f']/x['adj'] for x in L)/len(L)) if L else (1.5,0.5)
    def rosOf(x,st):
        if st=='bal': return x['ros']
        if x['c'] is None: t=x['ros']*(RAT[x['pos']][1] if st=='safe' else RAT[x['pos']][0])
        else: t=(x['f'] if st=='safe' else x['c'])*x['sos']
        return x['ros']+STYLE_W*(t-x['ros'])
    mx=None
    for st,key in (('bal','val'),('safe','vs'),('up','vu')):
        for pos in POS:
            L=sorted([x for x in rows if x['pos']==pos],key=lambda x:-rosOf(x,st))
            repl=rosOf(L[min(REPL[pos],len(L))-1],st) if L else 0
            for k,x in enumerate(L):
                r=rosOf(x,st);x['raw']=max(0,r-repl)*x['left']+0.15*r*x['left']
                if pos=='QB':                      # QB ladder: 5% off for QB1 rising smoothly to 20% off by QB15 (one-QB league)
                    d=qb_disc(k+1);x['raw']*=1-d
                    if st=='bal': x['qbr']=k+1;x['qbd']=round(d*100,1)
        if mx is None: mx=max(x['raw'] for x in rows) or 1
        for x in rows: x[key]=max(1,min(100,round(100*(x['raw']/mx)**0.85)))
    rows.sort(key=lambda x:-x['val'])
    for x in rows: del x['raw']
    return {'week':played_wk,'rows':rows}
if __name__=='__main__':
    T=build();print('through week',T['week'],'players',len(T['rows']))
    for x in T['rows'][:15]: print(x['val'],x['vs'],x['vu'],x['name'],x['pos'],x['ros'],x['c'],x['f'],x['left'],x['sos'],x['inj'])
