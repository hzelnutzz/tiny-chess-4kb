import os,json as j,urllib.request as Y
R=(10,-10,1,-1);D=(11,9,-11,-9);K=(21,19,12,8,-8,-12,-19,-21);S=R+D
V={'P':100,'N':320,'B':330,'R':500,'Q':900,'K':0};N=25e4
O={91:2,98:1,95:3,21:8,28:4,25:12}
X="iiiijkkjjklkkmonmprqquwuuyzyiiiighhghiihijkjjklkjklkijkjhiihghhghiihijjiijkjjklkjklkijkjijjihiihiiiijkkjhiihhiihhiihhiihjkkjiiiihiihijjiijkjjklkjklkijkjijjihiihmokimmiggeeeeccccaaacaaacaaacaaa"
def F(f):
 global B,C,P,W
 B=['#']*120;W=[0,0];C=P=0;g=f.split()
 for r in range(2,10):B[r*10+1:r*10+9]=['.']*8
 r=c=0
 for h in g[0]:
  if h=='/':r+=1;c=0
  elif h<'A':c+=int(h)
  else:s=(r+2)*10+c+1;B[s]=h;c+=1
  if h in'Kk':W[h<'a']=s
 for h in g[2]:C|=int(2**'KQkq'.find(h))
 if g[3]!='-':P=(10-int(g[3][1]))*10+ord(g[3][0])-96
 return g[1]>'v'
def A(s,w):
 d=20*w-10
 if 'pP'[w]in(B[s+d-1],B[s+d+1])or'nN'[w]in(B[s+o]for o in K)or'kK'[w]in(B[s+o]for o in S):return 1
 for o in S:
  t=s+o
  while B[t]=='.':t+=o
  if B[t]in('qQ'[w],('bB'[w],'rR'[w])[o in R]):return 1
 return 0
def M(f,t,z):
 global C,P,W
 p=B[f];x=B[t];a=C;e=P;B[f]='.';B[t]=z or p
 if p in'Pp'and e and t==e:g=t+10-20*(p>'Z');x=B[g];B[g]='.'
 elif p in'Kk':
  if abs(t-f)==2:r=t-2+3*(t>f);s=t+1-2*(t>f);B[s]=B[r];B[r]='.'
  W[p<'a']=t
 C=a&~(O.get(f,0)|O.get(t,0));P=p in'Pp'and abs(t-f)==20 and(f+t)//2 or 0
 return f,t,x,p,a,e
def U(u):
 global C,P,W
 f,t,x,p,a,e=u;B[f]=p
 if p in'Pp'and e and t==e:B[t]='.';B[t+10-20*(p>'Z')]=x
 else:B[t]=x
 if p in'Kk':
  if abs(t-f)==2:r=t-2+3*(t>f);s=t+1-2*(t>f);B[r]=B[s];B[s]='.'
  W[p<'a']=f
 C=a;P=e
def G(w,c=0):
 m=[];o=1-w;k='rR'[w];j=('QRBN','qrbn')[o]
 for f in range(120):
  p=B[f]
  if p<'@'or(p<'a')!=w:continue
  q=p.upper()
  if q=='P':
   d=10-20*w;t=f+d;r=f//10
   if B[t]=='.':
    if t//10==2+7*o:m+=[(f,t,x)for x in j]
    else:
     m+=[(f,t,0)]
     if r==3+5*w and B[t+d]=='.':m+=[(f,t+d,0)]
   for e in(d-1,d+1):
    u=f+e;x=B[u]
    if x>'@'and(x<'a')!=w:
     if u//10==2+7*o:m+=[(f,u,x)for x in j]
     else:m+=[(f,u,0)]
    elif x=='.'and u==P and r==6-w:m+=[(f,u,0)]
  elif q in'NK':
   for e in(K,S)[q=='K']:
    t=f+e;x=B[t]
    if x>'#'and(x=='.'or(x<'a')!=w):m+=[(f,t,0)]
   if q=='K'and f==25+70*w and A(f,o)<1:
    m+=[(f,f+2,0)]*(C&1<<2-2*w and B[f+1:f+4]==['.','.',k]and A(f+1,o)<1)
    m+=[(f,f-2,0)]*(C&2<<2-2*w and B[f-4:f]==[k,'.','.','.']and A(f-1,o)<1)
  else:
   for e in(D,S,R)['BQR'.find(q)]:
    t=f+e
    while B[t]=='.':m+=[(f,t,0)];t+=e
    x=B[t]
    if x>'@'and(x<'a')!=w:m+=[(f,t,0)]
 if c:m=[x for x in m if x[2]or B[x[1]]!='.'or x[1]==P]
 return m
def o(m):
 f,t,z=m;x=B[t]
 if x!='.':return-V[x.upper()]*16+V[B[f].upper()]
 if z:return-V[z.upper()]
 return 0
def E(w):
 s=0
 for q in range(120):
  p=B[q]
  if p>'@':
   c=p<'a';u=p.upper()
   s+=(2*c-1)*(V[u]+5*ord(X['PNBRQK'.find(u)*32+((q//10-2)^7*c)*4+min(q%10-1,8-q%10)])-525)
 return s*(2*w-1)
def q(a,b,w):
 global Q,H
 Q+=1;H|=Q>N
 if H:return 0
 v=E(w)
 if v>=b:return b
 a=max(a,v)
 for m in G(w,1):
  u=M(*m)
  if A(W[w],1-w):U(u);continue
  x=-q(-b,-a,1-w);U(u)
  if H:return a
  if x>a:a=x
  if a>=b:return b
 return a
def n(d,a,b,w):
 global Q,H
 Q+=1;H|=Q>N
 if H:return 0
 if d<1:return q(a,b,w)
 r=G(w);r.sort(key=o);v=-9**9
 for m in r:
  u=M(*m)
  if A(W[w],1-w):U(u);continue
  x=-n(d-1,-b,-a,1-w);U(u)
  if H:return v
  if x>v:v=x
  if x>a:a=x
  if a>=b:break
 return v
def T(f):
 global Q,H,BM
 w=F(f);Q=0;H=0;BM=None;d=1
 while not H and d<4:
  b=-9**9;m0=None
  for m in G(w):
   u=M(*m)
   if A(W[w],1-w):U(u);continue
   x=-n(d-1,-9**9,-b,1-w);U(u)
   if H:break
   if x>b:b=x;m0=m
  if not H and m0:BM=m0
  d+=1
 return BM
def c(m):
 f,t,z=m
 return chr(f%10+96)+str(10-f//10)+chr(t%10+96)+str(10-t//10)+(z or'').lower()
def h(p,d=0):return j.load(Y.urlopen(Y.Request(J+p,d and j.dumps(d).encode()or None,{'Content-Type':'application/json'})))
def m():
 global J
 J=os.environ['MAKEFUN_ENV_URL']
 while 1:
  g=h('/game')
  while g.get('status')=='your_move':
   z=T(g['fen'])
   if not z:break
   g=h('/move',{'game':g.get('game',g.get('id')),'move':c(z)})
  if g.get('status')=='done':print(j.dumps(g));return
if __name__=='__main__':m()
