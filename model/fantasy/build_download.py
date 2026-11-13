# Builds the Draft Room page + dated download, removing older downloads.
import glob,os,datetime
import pandas as _pd
WEEK=str(int(_pd.read_csv('/home/claude/nfldata/stats26.csv',usecols=['week']).week.max()))
DATE_LONG=datetime.date.today().strftime('%b %-d, %Y')
D=datetime.date.today().strftime('%b %-d')
t=open('/home/claude/fantasy/template.html').read()
t=t.replace('__PLAYERS__',open('/home/claude/fantasy/players.json').read()).replace('__BREAK__',open('/home/claude/fantasy/breakouts.json').read()).replace('__BADGES__',open('/home/claude/fantasy/badges.json').read()).replace('__WEEK__',WEEK).replace('__DATE__',DATE_LONG)
open('/home/claude/fantasy/draft-room-2027.html','w').write(t)
for f in glob.glob('/home/claude/downloads/draft-room-2027*.html'): os.remove(f)
i=t.index('</style>')+8
out=f'/home/claude/downloads/draft-room-2027 ({D}).html'
open(out,'w',encoding='utf-8').write('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<style>[hidden]{display:none!important}:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}img{max-width:100%}</style>\n'+t[:i]+'\n</head>\n<body>\n'+t[i:]+'\n</body>\n</html>\n')
print(out)

import subprocess; subprocess.run(['python3','/home/claude/fantasy/build_app.py'])
