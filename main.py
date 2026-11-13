import os,json as j,urllib.request as Y
R=(16,-16,1,-1);D=(17,15,-17,-15);K=(33,18,-14,-31,-33,-18,14,31);S=R+D
V={'P':100,'N':320,'B':330,'R':500,'Q':900,'K':0};N=2e4;Z=48000
X='eeeeooooggikffgjeeeifdcefggaeeee[]__]aee_egh_fhi_ehi_fgh]aef[]__acccceeecefgcffgceggcgggcfeeaccceeeefgggdeeedeeedeeedeeedeeeeeefaccdceeeceffdeffeeffcfffcefeaccd_]][_]][_]][_]][a__]caaaiieeikge'
W=[0,0];O={0:8,7:4,112:2,119:1,116:3,4:12};TT={};I=[0]*14400;L=[0]*200
y=lambda s,p:hash((s,ord(p)))
def F(f):
 global B,C,P,W,HK;B=['.#'[0<s&8]for s in range(120)]+['#']*136;g=f.split();r=c=C=P=HK=0
 for h in g[0]:
  if h=='/':r+=1;c=0
  elif h<'A':c+=int(h)
  else:s=r*16+c;B[s]=h;c+=1;HK^=y(s,h)
  if h in'Kk':W[h<'a']=s
 for h in g[2]:C|=dict(K=1,Q=2,k=4,q=8).get(h,0)
 if g[3]!='-':P=ord(g[3][0])-97+(8-int(g[3][1]))*16
 HK^=C^P;return g[1]=='w'
def A(s,w):
 d=32*w-16
 if 'pP'[w]in(B[s+d-1],B[s+d+1])or'nN'[w]in(B[s+o]for o in K)or'kK'[w]in(B[s+o]for o in S):return 1
 for o in S:
  t=s+o
  while B[t]=='.':t+=o
  if B[t]in('qQ'[w],('bB'[w],'rR'[w])[o in R]):return 1
 return 0
def M(f,t,z):
 global C,P,W,HK;p=B[f];x=B[t];a=C;e=P;B[f]='.';B[t]=z or p
 k=y(f,p)^y(t,z or p)
 if p in'Pp'and P and t==P:g=t+32*(p<'a')-16;x=B[g];B[g]='.';k^=y(g,x)
 elif p in'Kk':
  if abs(t-f)==2:r=t-2+3*(t>f);s=t+1-2*(t>f);B[s]=B[r];B[r]='.';k^=y(r,B[s])^y(s,B[s])
  W[p<'a']=t
 elif x!='.':k^=y(t,x)
 C=a&~(O.get(f,0)|O.get(t,0));P=p in'Pp'and abs(t-f)==32 and(f+t)//2 or 0
 k^=a^C^e^P;HK^=k;return(f,t,x,p,a,e,k)
def U(u):
 global C,P,W,HK;f,t,x,p,a,e,k=u;B[f]=p
 if p in'Pp'and e and t==e:B[t]='.';B[t+32*(p<'a')-16]=x
 else:B[t]=x
 if p in'Kk':
  if abs(t-f)==2:r=t-2+3*(t>f);s=t+1-2*(t>f);B[r]=B[s];B[s]='.'
  W[p<'a']=f
 C=a;P=e;HK^=k
def G(w,y=0):
 m=[];k='rR'[w];o=1-w;j=('qrbn','QRBN')[w]
 for f in range(120):
  if f&8or(p:=B[f])=='.'or(p<'a')!=w:continue
  q=p.upper()
  if q=='P':
   d=16-32*w;t=f+d;r=f>>4
   if B[t]=='.':m+=[(f,t+d,0)]*(r==1+5*w and B[t+d]=='.')+([(f,t,0)],[(f,t,x)for x in j])[t>>4==7-7*w]
   for e in(d-1,d+1):
    u=f+e;c=B[u]
    if c>'@'and(c<'a')!=w:m+=([(f,u,0)],[(f,u,x)for x in j])[u>>4==7-7*w]
    elif c=='.'and u==P and r==4-w:m+=[(f,u,0)]
  elif q in'NK':
   for e in(S,K)[q=='N']:
    t=f+e;c=B[t]
    if c>'#'and(c=='.'or(c<'a')!=w):m+=[(f,t,0)]
   if q=='K'and f==4+112*w and A(f,o)<1:m+=[(f,f+2,0)]*(C&4-3*w and B[f+1:f+4]==['.','.',k]and A(f+1,o)<1)+[(f,f-2,0)]*(C&8-6*w and B[f-4:f]==[k,'.','.','.']and A(f-1,o)<1)
  else:
   for e in(D,S,R)['BQR'.find(q)]:
    t=f+e
    while B[t]=='.':m+=[(f,t,0)];t+=e
    if(c:=B[t])>'@'and(c<'a')!=w:m+=[(f,t,0)]
 if y:m=[x for x in m if x[2]or B[x[1]]!='.'or x[1]==P]
 return m
def o(m):
 f,t,z=m
 if m==PV:return -N
 c=B[t]
 if c!='.'or z:return-(c!='.'and 10*V[c.upper()]-V[B[f].upper()]or 0)-(z and V[z.upper()]or 0)
 u=f*120+t
 if u==L[PL]or u==L[PL+1]:return-50
 return-min(I[u],49)
def E(w):
 s=0
 for q in range(120):
  if not q&8and(p:=B[q])!='.':c=p<'a';u=p.upper();s+=(2*c-1)*(V[u]+5*ord(X['PNBRQK'.find(u)*32+(q>>4^7-7*c)*4+min(q&7,7-q&7)])-505)
 return s*(2*w-1)+10
def q(a,b,w):
 global Q,H;Q+=1;H|=Q>Z
 if H:return 0
 v=E(w)
 if v>=b:return b
 a=max(a,v)
 for m in G(w,1):
  u=M(*m)
  if not A(W[w],1-w):
   x=-q(-b,-a,1-w)
   if x>=b:U(u);return b
   a=max(a,x)
  U(u)
  if H:break
 return a
def n(d,a,b,w,p):
 global Q,H,PV,PL,BM
 Q+=1;H|=Q>Z
 if H:return 0
 k=HK*2+w
 if v:=TT.get(k):
  if v[0]>=d and(not v[1]or(v[1]<0 and v[2]>=b)or(v[1]>1 and v[2]<=a)):return v[2]
  PV=v[3]
 else:PV=0
 if d<1:return q(a,b,w)
 PL=p;r=G(w);r.sort(key=o)
 oa=a;bs=-N;bm=0;ft=1
 for m in r:
  u=M(*m)
  if A(W[w],1-w):U(u);continue
  if ft:x=-n(d-1,-b,-a,1-w,p+1);ft=0
  else:
   x=-n(d-1,-a-1,-a,1-w,p+1)
   if x>a and x<b:x=-n(d-1,-b,-a,1-w,p+1)
  U(u)
  if H:break
  if x>bs:bs=x;bm=m
  if x>a:a=x
  if a>=b:
   if B[m[1]]=='.'and not m[2]:v=m[0]*120+m[1];L[p*2+1]=L[p*2];L[p*2]=v;I[v]+=1
   break
 if bs==-N:bs=-N if A(W[w],1-w)else 0;bm=0
 if not H:TT[k]=(d,(bs<=oa)*2-(bs>=b),bs,bm);p<1 and(BM:=bm);len(TT)>8000 and TT.clear()
 return bs
def T(i):
 global Q,H,BM
 w=F(i);Q=0;H=0;BM=G(w)[0];d=1
 while not H and d<99:n(d,-N,N,w,0);d+=1
 return BM
def c(m):f,t,z=m;return chr(f%8+97)+str(8-f//16)+chr(t%8+97)+str(8-t//16)+(z or'').lower()
def h(p,d):return j.load(Y.urlopen(Y.Request(J+p,j.dumps(d).encode(),{'Content-Type':'application/json'})))
def m():
 global J;J=os.environ['MAKEFUN_ENV_URL']
 while 1:
  g=h('/game',{})
  while g.get('status')=='your_move':
   if not(z:=T(g['fen'])):break
   g=h('/move',{'game':g.get('game',g.get('id')),'move':c(z)})
  if g.get('status')=='done':print(j.dumps(g));return
if __name__=='__main__':m()
