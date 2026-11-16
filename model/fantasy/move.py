# usage: python3 move.py --top|--draft|--both "Name=rank" ...  -> list-style move: remove, insert at target, everyone else slides.
#   --top   : Top 125 only (top_order.json, frozen Nov 16). Draft board untouched.
#   --draft : draft board only (draft_order.json, frozen Nov 13). Top 125 untouched.
#   --both  : both lists.
# Weekly stat updates never change either order; only this script (or the user's in-app moves) does.
import json,sys
MODE=sys.argv[1] if len(sys.argv)>1 else ''
assert MODE in ('--top','--draft','--both'),'First argument must be --top, --draft or --both'
T={a.split('=')[0]:int(a.split('=')[1]) for a in sys.argv[2:]}
F='/home/claude/fantasy/'
NM={r[1]:r[0] for r in json.load(open(F+'frozen/players.json'))}
NM.update({r[1]:r[0] for r in json.load(open(F+'players.json')) if r[1] not in NM})
for n in T: assert n in NM, f'Unknown player: {n}'
def apply(fn):
    D=json.load(open(F+fn)); nm=D.setdefault('names',['']*len(D['ids']))
    for n in sorted(T,key=lambda n:T[n]):
        i=NM[n]
        if i in D['ids']:
            k=D['ids'].index(i);D['ids'].pop(k);nm.pop(k)
        elif n in nm:
            k=nm.index(n);D['ids'].pop(k);nm.pop(k)
        D['ids'].insert(T[n]-1,i);nm.insert(T[n]-1,n)
    json.dump(D,open(F+fn,'w'))
    print(fn,'updated:',', '.join(f'{n} -> {D["ids"].index(NM[n])+1}' for n in T))
if MODE in('--top','--both'): apply('top_order.json')
if MODE in('--draft','--both'): apply('draft_order.json')
