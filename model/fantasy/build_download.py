import sys;sys.path.insert(0,'/home/claude/fantasy')
import json
# Builds the Draft Room page + local standalone test copy, then the app.
import glob,os,datetime
import pandas as _pd
WEEK=str(int(_pd.read_csv('/home/claude/nfldata/stats26.csv',usecols=['week']).week.max()))
DATE_LONG=datetime.date.today().strftime('%b %-d, %Y')
D=datetime.date.today().strftime('%b %-d')
t=open('/home/claude/fantasy/template.html').read()
FZ='/home/claude/fantasy/frozen/'
FMETA=json.load(open(FZ+'meta.json'))
def _order(fn):
    # Frozen order file (draft_order.json / top_order.json). If a player's NFL id changed, remap by name in memory; the order never changes.
    D=json.load(open('/home/claude/fantasy/'+fn));pool={r[1]:r[0] for r in json.load(open(FZ+'players.json'))};ids=set(pool.values())
    names=D.get('names',[]);out=[]
    for k,i in enumerate(D['ids']):
        if i not in ids and k<len(names) and names[k] in pool: i=pool[names[k]]
        out.append(i)
    return {'set':D['set'],'ids':out}
def _live():
    # Weekly-updated Player stats page ONLY (independent of the Top 125 and draft board orders):
    # rows of [id, name, pos, team, games, 2026 PPG, 2025 PPG, 2027 proj, pos rank by PPG]
    B=json.load(open('/home/claude/fantasy/badges.json'))
    return {'rows':[[r[0],r[1],r[2],r[3],r[9],r[11],B.get(r[0],{}).get('p25'),r[16],B.get(r[0],{}).get('pr')] for r in json.load(open('/home/claude/fantasy/players.json'))]}
def _draft_ids():
    # Frozen draft order. If a player's NFL id changed (e.g. a rookie placeholder id), remap by name in memory; the order never changes.
    D=json.load(open('/home/claude/fantasy/draft_order.json'));pool={r[1]:r[0] for r in json.load(open('/home/claude/fantasy/players.json'))};ids=set(pool.values())
    names=D.get('names',[]);out=[]
    for k,i in enumerate(D['ids']):
        if i not in ids and k<len(names) and names[k] in pool: i=pool[names[k]]
        out.append(i)
    return {'set':D['set'],'ids':out}
t=t.replace('__PLAYERS__',open(FZ+'players.json').read()).replace('__BREAK__',open(FZ+'breakouts.json').read()).replace('__BADGES__',open(FZ+'badges.json').read()).replace('__TOPORDER__',json.dumps(_order('top_order.json'))).replace('__LIVE__',json.dumps(_live())).replace('__FWEEK__',str(FMETA['week'])).replace('__HIST__',open(FZ+'history.json').read()).replace('__TRADE__',json.dumps(__import__('trade_data').build(),separators=(',',':'))).replace('__DRAFT__',json.dumps(_order('draft_order.json'))).replace('__DRAFTSET__',json.load(open('/home/claude/fantasy/draft_order.json'))['set']).replace('__WEEK__',WEEK).replace('__DATE__',DATE_LONG)
open('/home/claude/fantasy/draft-room-2027.html','w').write(t)
for f in glob.glob('/home/claude/downloads/draft-room-2027*.html'): os.remove(f)
i=t.index('</style>')+8
out='/home/claude/fantasy/standalone.html'  # local test copy; dated HTML downloads retired (the app is the single version)
open(out,'w',encoding='utf-8').write('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<style>[hidden]{display:none!important}:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}img{max-width:100%}</style>\n'+t[:i]+'\n</head>\n<body>\n'+t[i:]+'\n</body>\n</html>\n')
print(out)

import subprocess; subprocess.run(['python3','/home/claude/fantasy/build_app.py'])
