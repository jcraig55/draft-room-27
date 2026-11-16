# Builds fantasy/frozen/history.json: week-by-week PPR points for past seasons (regular season), for every player in the pool.
# Downloads nflverse stats_player_week_{year}.csv into nfldata/hist/ if missing. Static data; rerun only to add a finished season.
import pandas as pd,json,os,subprocess
B='https://github.com/nflverse/nflverse-data/releases/download/stats_player'
D='/home/claude/nfldata/hist';os.makedirs(D,exist_ok=True)
F='/home/claude/fantasy/'
ids=set(r[0] for r in json.load(open(F+'frozen/players.json')))|set(r[0] for r in json.load(open(F+'players.json')))
H={}
for y in range(2015,2026):
    f=f'{D}/w{y}.csv'
    if not os.path.exists(f): subprocess.run(['curl','-sSfL','-o',f,f'{B}/stats_player_week_{y}.csv'],check=True)
    d=pd.read_csv(f,usecols=['player_id','week','season_type','team','opponent_team','fantasy_points_ppr'],low_memory=False)
    d=d[(d.season_type=='REG')&d.player_id.isin(ids)]
    for pid,g in d.groupby('player_id'):
        g=g.sort_values('week')
        H.setdefault(pid,{})[str(y)]=[[int(w),o,round(float(p),1),t] for w,o,p,t in zip(g.week,g.opponent_team,g.fantasy_points_ppr.fillna(0),g.team)]
open(F+'frozen/history.json','w').write(json.dumps(H,separators=(',',':')))
print('history for',len(H),'players')
