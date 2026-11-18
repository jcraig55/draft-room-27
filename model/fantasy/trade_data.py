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
        rows.append({'id':pid,'name':name,'pos':pos,'team':team,'g':gm,'ppg':round(ppg,1),'adj':round(adj,2),'ros':round(adj*mult,2),'left':len(sched),'sos':round(mult,3),
                     'opp':[o for _,o in sched],'inj':inj.get(pid)})
    # value over replacement for the rest of the season, scaled 0-100
    for pos in POS:
        L=sorted([x for x in rows if x['pos']==pos],key=lambda x:-x['ros'])
        repl=L[min(REPL[pos],len(L))-1]['ros'] if L else 0
        for x in L: x['raw']=max(0,x['ros']-repl)*x['left']+0.15*x['ros']*x['left']
    mx=max(x['raw'] for x in rows) or 1
    for x in rows: x['val']=max(1,round(100*(x['raw']/mx)**0.85))
    rows.sort(key=lambda x:-x['val'])
    for x in rows: del x['raw']
    return {'week':played_wk,'rows':rows}
if __name__=='__main__':
    T=build();print('through week',T['week'],'players',len(T['rows']))
    for x in T['rows'][:15]: print(x['val'],x['name'],x['pos'],x['ros'],x['left'],x['sos'],x['inj'])
