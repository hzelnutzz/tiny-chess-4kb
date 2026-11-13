import os,json as j,urllib.request as Y
R=(16,-16,1,-1);D=(17,15,-17,-15);K=(33,18,-14,-31,-33,-18,14,31);S=R+D
V={'P':100,'N':320,'B':330,'R':500,'Q':900,'K':0};N=2e4;Z=250000
X='eeeeooooggikffgjeeeifdcefggaeeee[]__]aee_egh_fhi_ehi_fgh]aef[]__acccceeecefgcffgceggcgggcfeeaccceeeefgggdeeedeeedeeedeeedeeeeeefaccdceeeceffdeffeeffcfffcefeaccd_]][_]][_]][_]][a__]caaaiieeikge'
W=[0,0];O={0:8,7:4,112:2,119:1,116:3,4:12}
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
 d=32*w-16
 if 'pP'[w]in(B[s+d-1],B[s+d+1])or'nN'[w]in(B[s+o]for o in K)or'kK'[w]in(B[s+o]for o in S):return 1
 for o in S:
  t=s+o
  while B[t]=='.':t+=o
  if B[t]in('qQ'[w],('bB'[w],'rR'[w])[o in R]):return 1
 return 0
def M(f,t,z):
 global C,P,W;p=B[f];x=B[t];a=C;e=P;B[f]='.';B[t]=z or p
 if p in'Pp'and P and t==P:g=t+32*(p<'a')-16;x=B[g];B[g]='.'
 elif p in'Kk':
  if abs(t-f)==2:r=t-2+3*(t>f);B[t+1-2*(t>f)]=B[r];B[r]='.'
  W[p<'a']=t
 C&=~(O.get(f,0)|O.get(t,0));P=p in'Pp'and abs(t-f)==32 and(f+t)//2 or 0;return(f,t,z,x,p,a,e)
def U(u):
 global C,P,W;f,t,z,x,p,a,e=u;B[f]=p
 if p in'Pp'and e and t==e:B[t]='.';B[t+32*(p<'a')-16]=x
 else:B[t]=x
 if p in'Kk'and abs(t-f)==2:r=t-2+3*(t>f);s=t+1-2*(t>f);B[r]=B[s];B[s]='.'
 if p in'Kk':W[p<'a']=f
 C=a;P=e
def G(w,y=0):
 m=[];k='rR'[w];o=1-w;j=('qrbn','QRBN')[w]
 for f in range(120):
  if f&8 or(p:=B[f])=='.'or(p<'a')!=w:continue
  q=p.upper()
  if q=='P':
   d=16-32*w;t=f+d;r=f>>4
   if B[t]=='.':m+=[(f,t+d,0)]*(r==1+5*w and B[t+d]=='.')+(t>>4==7-7*w and[(f,t,x)for x in j]or[(f,t,0)])
   for e in(d-1,d+1):
    u=f+e;c=B[u]
    if c>'@'and(c<'a')!=w:m+=u>>4==7-7*w and[(f,u,x)for x in j]or[(f,u,0)]
    elif c=='.'and u==P and r==4-w:m+=[(f,u,0)]
  elif q in'NK':
   for e in(q=='N'and K or S):
    t=f+e;c=B[t]
    if c>'#'and(c=='.'or(c<'a')!=w):m+=[(f,t,0)]
   if q=='K'and f==4+112*w and A(f,o)<1:m+=[(f,f+2,0)]*(C&(4,1)[w]and B[f+1:f+4]==['.','.',k]and A(f+1,o)<1)+[(f,f-2,0)]*(C&(8,2)[w]and B[f-4:f]==[k,'.','.','.']and A(f-1,o)<1)
  else:
   for e in(q=='R'and R or q=='B'and D or S):
    t=f+e
    while B[t]=='.':m+=[(f,t,0)];t+=e
    if(c:=B[t])>'@'and(c<'a')!=w:m+=[(f,t,0)]
 if y:m=[x for x in m if x[2]or B[x[1]]!='.'or x[1]==P]
 return m
def v(m):f,t,z=m;c=B[t];return-(c!='.'and 10*V[c.upper()]-V[B[f].upper()]or 0)-(z and V[z.upper()]or 0)
def E(w):
 s=0
 for q in range(120):
  if not q&8 and(p:=B[q])!='.':c=p<'a';u=p.upper();s+=(2*c-1)*(V[u]+5*ord(X['PNBRQK'.find(u)*32+(q>>4^7-7*c)*4+min(q&7,7-q&7)])-505)
 return s*(2*w-1)
def q(a,b,w):
 global Q,H;Q+=1;H|=Q>Z
 if H:return 0
 if(v:=E(w))>=b:return b
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
def a(d,l,e,w):
 global Q,H;Q+=1;H|=Q>Z
 if H:return 0
 if d<=0:return q(l,e,w)
 r=G(w);r.sort(key=v);b=-N;g=0
 for m in r:
  if H:break
  u=M(*m)
  if A(W[w],1-w):U(u);continue
  g=1;x=-a(d-1,-e,-l,1-w);U(u)
  b=max(b,x);l=max(l,x)
  if l>=e:break
 if not g:return A(W[w],1-w)and-9999 or 0
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
  if not H:b=o;r.remove(o);r[:0]=[o]
 return b
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
