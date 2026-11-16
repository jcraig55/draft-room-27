# usage: python3 move.py --top|--draft|--both "Name=rank" ...  -> list-style move: remove, insert at target, everyone else slides.
#   --top   : Top 125 / weekly ranks only (pins in proj.py OVR/DOWN). Draft board untouched.
#   --draft : frozen draft board only (draft_order.json). Top 125 untouched.
#   --both  : both lists.
import re,json,sys,subprocess
MODE=sys.argv[1] if len(sys.argv)>1 else ''
assert MODE in ('--top','--draft','--both'),'First argument must be --top, --draft or --both'
T={a.split('=')[0]:int(a.split('=')[1]) for a in sys.argv[2:]}
TOP=MODE in('--top','--both');DRAFT=MODE in('--draft','--both')
if TOP:
 P=json.load(open('/home/claude/fantasy/proj.json')); L=[x['name'] for x in P]; mr={x['name']:x['mrank'] for x in P}
 for n in T: assert n in L,n
 L=[n for n in L if n not in T]
 for n in sorted(T,key=lambda n:T[n]): L.insert(T[n]-1,n)
 idx={n:i+1 for i,n in enumerate(L)}
 p='/home/claude/fantasy/proj.py'; s=open(p).read()
 D={}
 for name in ['OVR','DOWN']:
     m=re.search(r"^%s=(\{.*\})$"%name,s,re.M); D[name]=eval(m.group(1))
 for n in T:
     if n not in D['OVR'] and n not in D['DOWN']: D['OVR' if T[n]<mr[n] else 'DOWN'][n]=0
 for name in D: D[name]={k:idx[k] for k in D[name]}
 for name in ['OVR','DOWN']:
     m=re.search(r"^%s=(\{.*\})$"%name,s,re.M); s=s[:m.start(1)]+repr(D[name])+s[m.end(1):]
 open(p,'w').write(s)
 subprocess.run(['python3','/home/claude/fantasy/final.py'],capture_output=True)
 NP=[x['name'] for x in json.load(open('/home/claude/fantasy/proj.json'))]
 bad=[(i+1,a,b) for i,(a,b) in enumerate(zip(L,NP)) if a!=b][:10]
 print('matches intended order' if not bad else ('MISMATCH',bad))
# Frozen draft order (draft_order.json), which weekly updates never touch.
if DRAFT:
 NM={r[1]:r[0] for r in json.load(open('/home/claude/fantasy/players.json'))}
 D=json.load(open('/home/claude/fantasy/draft_order.json'))
 for n in sorted(T,key=lambda n:T[n]):
     i=NM.get(n)
     if i is None: continue
     nm=D.setdefault('names',['']*len(D['ids']))
     if i in D['ids']:
         k=D['ids'].index(i);D['ids'].pop(k);nm.pop(k)
     D['ids'].insert(T[n]-1,i);nm.insert(T[n]-1,n)
 json.dump(D,open('/home/claude/fantasy/draft_order.json','w'))
 print('draft order updated:',', '.join(f'{n} -> {D["ids"].index(NM[n])+1}' for n in T if n in NM))
