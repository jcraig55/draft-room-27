import json, datetime as dt
P=json.load(open('raw.json'))
REF=dt.date(2027,9,1)
def age(b):
    if not b: return None
    y,m,d=map(int,b.split('-')); return round((REF-dt.date(y,m,d)).days/365.25,1)
POSMEAN={'QB':17,'RB':11,'WR':10.5,'TE':8}
def curve(pos,a,rk):
    f=1.0
    if a is None: return f
    if pos=='RB':
        if a<=23: f*=1.04
        if a>27: f*=0.97**(a-27)
        if a>30: f*=0.93**(a-30)
    elif pos=='WR':
        if a<=24: f*=1.05
        if a>30: f*=0.97**(a-30)
        if a>33: f*=0.93**(a-33)
    elif pos=='TE':
        if a<=25: f*=1.06
        if a>30: f*=0.95**(a-30)
        if a>33: f*=0.9**(a-33)
    elif pos=='QB':
        if a>35: f*=0.95**(a-35)
        if a>39: f*=0.85**(a-39)
    if rk==2026: f*=1.07 if pos in('WR','TE','QB') else 1.04
    return f
for x in P:
    x['age']=age(x['birth'])
    g26,g25=x['g'],x['g25'] or 0
    p26=x['ppg']; p25=(x['ppr25']/g25) if g25 else None
    w26=g26*1.0; w25=g25*(0.45 if g26>=4 else 0.8) if p25 is not None else 0
    if w26+w25==0: base=0
    else: base=((p26*w26 if g26 else 0)+((p25 or 0)*w25))/(w26+w25)
    # shrink small samples
    n=w26+w25; k=3.0 if w25 else 6.0
    base=(base*n+POSMEAN[x['pos']]*0.75*k)/(n+k)
    x['proj']=base*curve(x['pos'],x['age'],x['rookie'])
# ---- situational adjustments (multipliers on projected PPR/G), with the note shown in the bio
ADJ={
 'Aaron Rodgers':(0.55,'Turns 44 in December; retirement risk for 2027 is high.'),
 'Travis Kelce':(0.75,'Turns 38 in the 2027 season; retirement risk and declining role.'),
 'Kirk Cousins':(0.8,'Turns 39; the Raiders drafted Fernando Mendoza No. 1 in 2026, so 2027 starting job is in doubt.'),
 'Geno Smith':(0.8,'Turns 37; Jets are projected to draft a QB early in 2027.'),
 'Jacoby Brissett':(0.6,'Bridge starter; Arizona is expected to turn to a younger QB.'),
 'Matthew Stafford':(0.85,'Turns 39 in 2027 with no long-term successor; production still strong.'),
 'Tyler Shough':(0.85,'Strong volume but 4.8 yds/att in recent weeks; job security uncertain.'),
 'Derrick Henry':(1.1,'Turns 33 before 2027. Still a goal-line monster: league-high goal-line usage.'),
 'Davante Adams':(0.85,'Turns 35 in 2027 but still the Rams’ top red-zone target.'),
 'Mike Evans':(0.9,'Turns 34; thriving in San Francisco as a top target.'),
 'Josh Jacobs':(0.85,'Started 2026 on the Commissioner’s Exempt List pending an NFL review; reported Oct 19 to be set for a full practice week.'),
 'Jalen Hurts':(0.92,'On IR with blood clots in 2026; health is the 2027 question.'),
 'Saquon Barkley':(1.25,'Hamstring injury in Week 4 cost him multiple games; turns 30 in 2027.'),
 'Christian McCaffrey':(0.92,'Turns 31; still a top-10 back when on the field.'),
 'Kenneth Walker III':(0.97,'Free-agent signing in Kansas City; among the NFL rushing leaders.'),
 'Marvin Harrison Jr.':(1.15,'Traded to Houston Oct 11, reuniting with C.J. Stroud. Only 5 catches in four Arizona games.'),
 'Justin Herbert':(0.95,'Career-worst 2026: 59.4% completions and 68.8 rating with a new coordinator.'),
 'Fernando Mendoza':(1.0,'2026 No. 1 overall pick; has thrown only 8 passes behind Kirk Cousins.'),
 'Jayden Daniels':(1.0,'Elite rushing (9.7 yds/carry) but has played only 3 games.'),
 'Caleb Williams':(1.05,'Bears average 45 points in his two full starts.'),
 'Lamar Jackson':(1.0,'Missed time in 2026; led the league at 10.1 yds/att when healthy.'),
 'Puka Nacua':(1.0,'Missed games but leads the Rams in targets per game.'),
 'Jaxon Smith-Njigba':(1.0,'Reigning Offensive Player of the Year; leads the NFL in target share.'),
 'Brock Bowers':(1.0,'Missed time but averages over 20 PPR points per game when active.'),
 'Isaiah Likely':(0.95,'Breakout with the Giants: a top-three target share among tight ends.'),
 'Christian Watson':(0.97,'Career year built on a high touchdown rate that will likely cool.'),
 'Javonte Williams':(0.92,'7 rushing TDs on 3.7 yds/carry; scoring is carrying the line.'),
 'Kyle Monangai':(1.0,'5.4 yds/carry; splitting work with D’Andre Swift.'),
 'Malik Washington':(0.9,'28% target share but only 7.7 PPR/G in a weak Miami offense.'),
 'Isaiah Pacheco':(0.9,'No 2026 games; on reserve with Detroit.'),
 'Zach Charbonnet':(0.95,'On PUP to start 2026.'),
 'Joe Flacco':(0.4,'No 2026 snaps; turns 42.'),
 'Nick Chubb':(0.5,'No 2026 games; turns 31.'),
 'Kareem Hunt':(0.5,'No 2026 games; turns 32.'),
 'Justin Fields':(0.6,'Backup in Kansas City in 2026.'),
}
for x in P:
    if x['name'] in ADJ:
        m,n=ADJ[x['name']]; x['proj']*=m; x['note']=n
    else: x['note']=''
# ---- 2027 rookies (projected landing spot from War Room base mock)
ROOK=[
 ('Jeremiah Smith','WR','LAC',1,'Ohio State',76,222,'2007-02-08',15.0,'52 rec · 984 yds · 12 TD at Ohio State','Rare size with deep speed and twitch; compared to Julio Jones.'),
 ('Jadan Baugh','RB','CLE',21,'Florida',73,225,'2005-09-01',12.0,'763 rush yds · 13 TD · 5.7 per carry','Bell-cow build with vision, burst and a mean stiff-arm.'),
 ('Charlie Becker','WR','NYJ',7,'Indiana',76,207,'2005-06-01',11.0,'39 rec · 694 yds · 8 TD','Big receiver with real second-gear speed; Alec Pierce comp.'),
 ('Drew Mestemaker','QB','NYJ',6,'Oklahoma State',75,211,'2005-01-01',14.5,'1,940 pass yds · 16 TD · 6 INT','Best physical toolbox in the QB class plus real running ability.'),
 ('Darian Mensah','QB','ARI',9,'Miami (FL)',75,205,'2005-01-01',14.0,'1,764 pass yds · 18 TD · 1 INT · 203.9 rating','Elite accuracy and poise; Heisman frontrunner.'),
 ('Cam Coleman','WR','HOU',12,'Texas',75,204,'2006-01-01',8.8,'20 rec · 336 yds · 6 TD','Vertical boundary playmaker with red-zone body control.'),
 ('Nick Marsh','WR','SEA',16,'Indiana',75,213,'2005-06-01',8.3,'32 rec · 585 yds · 7 TD','Physical route runner who wins contested catches (7 of 9 in 2026).'),
 ('Trinidad Chambliss','QB','CLE',14,'Ole Miss',72,210,'2003-01-01',13.5,'1,676 pass yds · 14 TD · 4 INT','Dual-threat creator who makes off-script plays.'),
 ('Ryan Coleman-Williams','WR','BAL',23,'Alabama',72,182,'2006-01-01',7.8,'23 rec · 415 yds · 4 TD','Explosive after the catch.'),
 ('KJ Duff','WR','DEN',25,'Rutgers',78,225,'2005-01-01',7.8,'42 rec · 741 yds · 9 TD','6-6 mismatch with big-play ability.'),
 ('Jamari Johnson','TE','KC',32,'Oregon',77,255,'2005-01-01',6.8,'17 rec · 224 yds · 2 TD','Three-down tight end body; could inherit the Kelce role.'),
 ('Trey’Dez Green','TE','NE',28,'LSU',79,237,'2006-01-01',6.3,'14 rec · 222 yds · 1 TD','Seam-stretching 6-7 mismatch.'),
 ('Kewan Lacy','RB','BAL',55,'Ole Miss',71,205,'2005-01-01',8.0,'352 rush yds · 5 TD (2025: 1,567 yds · 24 TD)','Quick, shifty, tough between the tackles; Henry successor in this mock.'),
 ('Arch Manning','QB','PHI',13,'Texas',76,225,'2005-04-27',11.0,'1,295 pass yds · 11 TD · 5 INT','Prototype tools; may return to school.'),
]
for (n,pos,tm,pick,col,ht,wt,b,pp,line,strg) in ROOK:
    P.append(dict(pid='r-'+n.lower().replace(' ','-').replace('’',''),name=n,pos=pos,team=tm,teams=[],birth=b,ht=ht,wt=wt,college=col,rookie=2027,status='PROSPECT',draft=[2027,1 if pick<=32 else 2,pick],
      g=0,ppr=0,ppg=0,cmp=0,att=0,pyd=0,ptd=0,pint=0,car=0,ryd=0,rtd=0,tgt=0,rec=0,yds=0,tdr=0,ts=0,ays=None,snap=None,g25=None,ppr25=None,l25={},
      age=age(b) if not b.endswith('-01-01') else None,proj=pp,note=f'2027 rookie. Projected No. {pick} pick to {tm} in the War Room base mock.',col26=line,strg=strg))
# ---- manual adds: players missing from the stats pool
if not any(x['name']=='Jordyn Tyson' for x in P): P.append(dict(pid='m-jordyn-tyson',name='Jordyn Tyson',pos='WR',team='NO',teams=[],birth='2004-08-12',ht=74,wt=200,college='Arizona State',rookie=2026,status='ACT',draft=[2026,1,8],
  g=1,ppr=5.0,ppg=5.0,cmp=0,att=0,pyd=0,ptd=0,pint=0,car=0,ryd=0,rtd=0,tgt=5,rec=4,yds=30,tdr=0,ts=None,ays=None,snap=None,g25=None,ppr25=None,l25={},
  age=age('2004-08-12'),proj=11.0,col26='Week 9 debut vs. Cleveland: 4 rec · 30 yds on 5 targets (missed Weeks 1–8)',strg='No. 8 overall pick in 2026; 1,101 yds and 10 TDs at Arizona State in 2024.',
  note='Activated from IR Nov. 7 after an August hamstring injury. Injury history: 2022 knee (ACL, MCL, PCL), 2024 collarbone, 2025 hamstring and ankle.'))
# ---- games & season points
GP={'QB':16,'RB':14.5,'WR':15.5,'TE':15.5}
for x in P:
    x['pts']=x['proj']*GP[x['pos']]
# ---- VOR for 16 teams, QB/RB/2WR/TE/2FLEX
T=16
bypos={k:sorted([x for x in P if x['pos']==k],key=lambda x:-x['pts']) for k in GP}
start={'QB':T,'RB':T,'WR':2*T,'TE':T}
rem=[]
for k in bypos: rem+=bypos[k][start[k]:]
rem.sort(key=lambda x:-x['pts'])
flex=[x for x in rem if x['pos']!='QB'][:2*T]
cnt={k:start[k]+sum(1 for x in flex if x['pos']==k) for k in GP}
# replacement = bench-depth aware: starters + ~35% of starter count
repl={k:bypos[k][min(len(bypos[k])-1,int(cnt[k]*1.25))]['pts'] for k in GP}
MKT={'QB':0.8,'RB':1.0,'WR':1.0,'TE':0.95}
for x in P: x['vor']=(x['pts']-repl[x['pos']])*(MKT[x['pos']] if x['pts']>repl[x['pos']] else 1)
P.sort(key=lambda x:-x['vor'])
for _i,_x in enumerate(P): _x['mrank']=_i+1
# ---- manual rank overrides: proven names whose small or down 2026 samples undersell their 2027 value
OVR={'Drake London': 21, 'Justin Jefferson': 25, 'Bucky Irving': 17, 'Luther Burden III': 20, 'Josh Allen': 23, 'Bhayshul Tuten': 24, 'Chris Olave': 28, 'Derrick Henry': 31, 'Jonah Coleman': 33, 'Jeremiyah Love': 34, 'Garrett Wilson': 37, 'Breece Hall': 38, 'Emeka Egbuka': 46, 'Quinshon Judkins': 52, 'Carnell Tate': 69, 'Jordyn Tyson': 68, 'Isaiah Likely': 44, 'Kenneth Walker III': 3, 'Matthew Golden': 30, 'Saquon Barkley': 57, 'Josh Jacobs': 51, 'Ladd McConkey': 62, 'Marvin Harrison Jr.': 64, 'Brian Thomas Jr.': 86, 'Jaylen Warren': 27, 'Javonte Williams': 39, 'Jahmyr Gibbs': 2, 'Bijan Robinson': 5, 'Chuba Hubbard': 45, 'Blake Corum': 83, 'Woody Marks': 100, 'Lamar Jackson': 55, 'Colston Loveland': 66, 'DJ Moore': 70}
DOWN={'Tee Higgins': 16, 'Trey McBride': 19, 'Brock Bowers': 18, "De'Von Achane": 26, 'Jeremiah Smith': 32, 'Christian Watson': 29, 'Rashee Rice': 35, 'Nico Collins': 40, "D'Andre Swift": 15, 'George Pickens': 36, "Wan'Dale Robinson": 106, 'Joe Burrow': 41, 'Jaxon Smith-Njigba': 1, 'Jahmyr Gibbs': 2, 'Bijan Robinson': 5, 'Ashton Jeanty': 22, 'RJ Harvey': 145, 'Michael Pittman': 135}
OVR.update(DOWN)
moved=[x for x in P if x['name'] in OVR]
P=[x for x in P if x['name'] not in OVR]
for x in sorted(moved,key=lambda x:OVR[x['name']]):
    P.insert(OVR[x['name']]-1,x); x['adj']=1
    if x['name'] not in DOWN and x['name']!='Chris Olave': x['note']=(x['note']+' ' if x['note'] else '')+'Ranked on track record and draft-market value, above where 2026 stats alone would put him.'
for i,x in enumerate(P): x['rank']=i+1
# where each adjusted player would sit if only HIS override were removed (others kept)
_base=[x['name'] for x in sorted(P,key=lambda x:x['mrank'])]
def _place(o):
    L=[n for n in _base if n not in o]
    for n in sorted(o,key=lambda n:o[n]): L.insert(o[n]-1,n)
    return L
for x in P:
    if x.get('adj'):
        x['nat']=_place({k:v for k,v in OVR.items() if k!=x['name']}).index(x['name'])+1
pr={}
for x in P:
    pr[x['pos']]=pr.get(x['pos'],0)+1; x['prank']=pr[x['pos']]
json.dump(P,open('proj.json','w'))
