import os,json,urllib.request as Y
R=(16,-16,1,-1);D=(17,15,-17,-15);K=(33,18,-14,-31,-33,-18,14,31);S=R+D
V={'P':100,'N':320,'B':330,'R':500,'Q':900,'K':0};N=99999;Z=250000
B=0;C=P=Q=H=0;W=[0,0];O={0:8,7:4,112:2,119:1,116:3,4:12}
def F(f):
 global B,C,P,W;B=['.#'[0<s&8]for s in range(120)]+['#']*136;g=f.split();r=c=C=P=0
 for h in g[0]:
  if h=='/':r+=1;c=0
  elif h<'A':c+=int(h)
  else:
   s=r*16+c;B[s]=h;c+=1
   if h in'Kk':W[h<'a']=s
 for h in g[2]:C|=dict(K=1,Q=2,k=4,q=8).get(h,0)
 if g[3]!='-':P=ord(g[3][0])-97+(8-int(g[3][1]))*16
 return g[1]=='w'
def A(s,w):
 d=32*w-16;e=1-w;p='Pp'[e];n='Nn'[e];k='Kk'[e];q='Qq'[e];r='Rr'[e];b='Bb'[e]
 if B[s+d-1]==p or B[s+d+1]==p:return 1
 if n in(B[s+o]for o in K):return 1
 if k in(B[s+o]for o in S):return 1
 for o in S:
  t=s+o
  while B[t]=='.':t+=o
  if B[t]==q or B[t]==(b,r)[o in R]:return 1
 return 0
def M(f,t,z):
 global C,P,W
 p=B[f];x=B[t];a=C;e=P;B[f]='.';B[t]=z or p
 if p in'Pp'and P and t==P:g=t+16-32*(p=='p');x=B[g];B[g]='.'
 elif p in'Kk':
  if abs(t-f)==2:r=t-2+3*(t>f);B[t+1-2*(t>f)]=B[r];B[r]='.'
  W[p<'a']=t
 C&=~(O.get(f,0)|O.get(t,0));P=(f+t)//2 if p in'Pp'and abs(t-f)==32 else 0
 return(f,t,z,x,p,a,e)
def U(u):
 global C,P,W
 f,t,z,x,p,a,e=u;B[f]=p
 if p in'Pp'and e and t==e:B[t]='.';B[t+16-32*(p=='p')]=x
 else:
  B[t]=x
  if p in'Kk'and abs(t-f)==2:r=t-2+3*(t>f);B[r]=B[t+1-2*(t>f)];B[t+1-2*(t>f)]='.'
 if p in'Kk':W[p<'a']=f
 C=a;P=e
def G(w,cs=0):
 m=[];k='rR'[w];o=1-w;j=('qrbn','QRBN')[w]
 for f in range(120):
  p=B[f]
  if f&8 or p=='.'or(p<'a')!=w:continue
  q=p.upper()
  if q=='P':
   d=16-32*w;t=f+d;r=f>>4
   if B[t]=='.':
    if r==1+5*w and B[t+d]=='.':m+=[(f,t+d,0)]
    m+=[(f,t,x)for x in j]if t>>4==7-7*w else[(f,t,0)]
   for e in(d-1,d+1):
    u=f+e;c=B[u]
    if c=='#':continue
    if c!='.'and(c<'a')!=w:m+=[(f,u,x)for x in j]if u>>4==7-7*w else[(f,u,0)]
    elif c=='.'and u==P and r==4-w:m+=[(f,u,0)]
  elif q in'NK':
   for e in(K if q=='N'else S):
    t=f+e;c=B[t]
    if c!='#'and(c=='.'or(c<'a')!=w):m+=[(f,t,0)]
   if q=='K'and f==4+112*w and A(f,o)<1:
    if C&(4,1)[w]and B[f+1:f+4]==['.','.',k]and A(f+1,o)<1:m+=[(f,f+2,0)]
    if C&(8,2)[w]and B[f-4:f]==[k,'.','.','.']and A(f-1,o)<1:m+=[(f,f-2,0)]
  else:
   for e in(R if q=='R'else D if q=='B'else S):
    t=f+e
    while B[t]=='.':m+=[(f,t,0)];t+=e
    c=B[t]
    if c!='#'and(c<'a')!=w:m+=[(f,t,0)]
 if cs:m=[x for x in m if x[2]or B[x[1]]!='.'or x[1]==P]
 return m
def v(m):
 f,t,z=m;c=B[t];return-(10*V[c.upper()]-V[B[f].upper()]if c!='.'else 0)-(V[z.upper()]if z else 0)
def E(w):return(2*w-1)*sum((2*(B[q]<'a')-1)*V[B[q].upper()]for q in range(120)if not q&8 and B[q]!='.')
def q(a,b,w):
 global Q,H;Q+=1;H|=Q>Z
 if H:return 0
 v=E(w)
 if v>=b:return b
 if v>a:a=v
 for m in G(w,1):
  f,t,z=m
  if B[t]in'Kk':return 9999
  u=M(f,t,z)
  if not A(W[w],1-w):
   x=-q(-b,-a,1-w);U(u)
   if x>=b:return b
   if x>a:a=x
  else:U(u)
  if H:break
 return a
def a(d,l,e,w):
 global Q,H;Q+=1;H|=Q>Z
 if H:return 0
 if d<=0:return q(l,e,w)
 r=G(w);r.sort(key=v);b=-N;g=0
 for m in r:
  if H:break
  f,t,z=m;c=B[t]
  if c in'Kk':return 9999
  u=M(f,t,z)
  if A(W[w],1-w):U(u);continue
  g=1;x=-a(d-1,-e,-l,1-w);U(u)
  if x>b:b=x
  if x>l:l=x
  if l>=e:break
 if not g:return -9999 if A(W[w],1-w)else 0
 return b
def T(i):
 global Q,H;w=F(i);r=G(w);r.sort(key=v);Q=0;H=0;b=r[0]
 for d in(1,2,3):
  if H:break
  l=-N;o=r[0]
  for m in r:
   if H:break
   u=M(*m)
   if A(W[w],1-w):U(u);continue
   x=-a(d-1,-N,-l,1-w);U(u)
   if not H and x>l:l=x;o=m
  if not H:b=o;r.remove(o);r.insert(0,o)
 return b
def c(m):
 f,t,z=m;return chr(97+(f&7))+str(8-(f>>4))+chr(97+(t&7))+str(8-(t>>4))+(z and z.lower()or'')
def h(p,d):return json.load(Y.urlopen(Y.Request(J+p,json.dumps(d).encode(),{'Content-Type':'application/json'})))
def m():
 global J;J=os.environ['MAKEFUN_ENV_URL']
 while 1:
  g=h('/game',{})
  while g.get('status')=='your_move':
   z=T(g['fen'])
   if not z:break
   g=h('/move',{'game':g.get('game',g.get('id')),'move':c(z)})
  if g.get('status')=='done':print(json.dumps(g));return
if __name__=='__main__':m()
