
import json, os, sys, urllib.request, urllib.error

ENV_URL = os.environ.get("MAKEFUN_ENV_URL") or sys.exit("MAKEFUN_ENV_URL is not set")

def post(path, body):
    req = urllib.request.Request(ENV_URL + path, data=json.dumps(body).encode(),
        headers={"content-type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r: return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"{path}: HTTP {e.code} {e.read().decode(errors='replace')}")

VAL = {"p":100,"n":320,"b":330,"r":500,"q":900,"k":0}
PST = {
"p":(0,0,0,0,0,0,0,0, 50,50,50,50,50,50,50,50, 10,10,20,30,30,20,10,10,
     5,5,10,25,25,10,5,5, 0,0,0,20,20,0,0,0, 5,-5,-10,0,0,-10,-5,5, 5,10,10,-20,-20,10,10,5, 0,0,0,0,0,0,0,0),
"n":(-50,-40,-30,-30,-30,-30,-40,-50, -40,-20,0,0,0,0,-20,-40, -30,0,10,15,15,10,0,-30,
     -30,5,15,20,20,15,5,-30, -30,0,15,20,20,15,0,-30, -30,5,10,15,15,10,5,-30, -40,-20,0,5,5,0,-20,-40, -50,-40,-30,-30,-30,-30,-40,-50),
"b":(-20,-10,-10,-10,-10,-10,-10,-20, -10,0,0,0,0,0,0,-10, -10,0,5,10,10,5,0,-10,
     -10,5,5,10,10,5,5,-10, -10,0,10,10,10,10,0,-10, -10,10,10,10,10,10,10,-10, -10,5,0,0,0,0,5,-10, -20,-10,-10,-10,-10,-10,-10,-20),
"r":(0,0,0,0,0,0,0,0, 5,10,10,10,10,10,10,5, -5,0,0,0,0,0,0,-5, -5,0,0,0,0,0,0,-5,
     -5,0,0,0,0,0,0,-5, -5,0,0,0,0,0,0,-5, -5,0,0,0,0,0,0,-5, 0,0,0,5,5,0,0,0),
"q":(-20,-10,-10,-5,-5,-10,-10,-20, -10,0,0,0,0,0,0,-10, -10,0,5,5,5,5,0,-10, -5,0,5,5,5,5,0,-5,
     0,0,5,5,5,5,0,-5, -10,5,5,5,5,5,0,-10, -10,0,5,5,5,5,0,-10, -20,-10,-10,-5,-5,-10,-10,-20),
"k":(-30,-40,-40,-50,-50,-40,-40,-30, -30,-40,-40,-50,-50,-40,-40,-30, -30,-40,-40,-50,-50,-40,-40,-30,
     -30,-40,-40,-50,-50,-40,-40,-30, -20,-30,-30,-40,-40,-30,-30,-20, -10,-20,-20,-20,-20,-20,-20,-10, 20,20,0,0,0,0,20,20, 20,30,10,0,0,10,30,20)}

def parse(fen):
    board = {}; idx = 0
    for row in fen.split()[0].split("/"):
        for c in row:
            if c.isdigit(): idx += int(c)
            else: board[idx] = c; idx += 1
    return board, fen.split()[1] == "w"

def attacked(b, sq, by_white):
    r, f = divmod(sq, 8)
    own = str.isupper if by_white else str.islower
    for df in (-1, 1):
        rr, ff = (r-1, f+df) if by_white else (r+1, f+df)
        if 0<=rr<8 and 0<=ff<8:
            p = b.get(rr*8+ff)
            if p and own(p) and p.lower()=="p": return True
    for dr, df in ((1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)):
        rr, ff = r+dr, f+df
        if 0<=rr<8 and 0<=ff<8:
            p = b.get(rr*8+ff)
            if p and own(p) and p.lower()=="n": return True
    for dr in (-1,0,1):
        for df in (-1,0,1):
            if dr==df==0: continue
            rr, ff = r+dr, f+df
            if 0<=rr<8 and 0<=ff<8:
                p = b.get(rr*8+ff)
                if p and own(p) and p.lower()=="k": return True
    for dr, df, ks in ((1,0,"rq"),(-1,0,"rq"),(0,1,"rq"),(0,-1,"rq"),
                        (1,1,"bq"),(1,-1,"bq"),(-1,1,"bq"),(-1,-1,"bq")):
        rr, ff = r+dr, f+df
        while 0<=rr<8 and 0<=ff<8:
            p = b.get(rr*8+ff)
            if p:
                if own(p) and p.lower() in ks: return True
                break
            rr += dr; ff += df
    return False

def gen(b, white):
    own = str.isupper if white else str.islower
    ms = []
    for sq, p in list(b.items()):
        if not own(p): continue
        pl = p.lower(); r, f = divmod(sq, 8)
        if pl=="p":
            d = -1 if white else 1; start = 6 if white else 1; last = 0 if white else 7
            rr = r+d
            if 0<=rr<8 and rr*8+f not in b:
                if rr==last:
                    for pr in "qrbn": ms.append((sq, rr*8+f, pr))
                else:
                    ms.append((sq, rr*8+f, None))
                    if r==start and (r+2*d)*8+f not in b: ms.append((sq, (r+2*d)*8+f, None))
            for df in (-1,1):
                ff=f+df
                if 0<=ff<8 and 0<=rr<8:
                    t=rr*8+ff; tp=b.get(t)
                    if tp and not own(tp):
                        if rr==last:
                            for pr in "qrbn": ms.append((sq,t,pr))
                        else: ms.append((sq,t,None))
        elif pl=="n":
            for dr,df in ((1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)):
                rr,ff=r+dr,f+df
                if 0<=rr<8 and 0<=ff<8:
                    t=rr*8+ff; tp=b.get(t)
                    if not tp or not own(tp): ms.append((sq,t,None))
        elif pl=="k":
            for dr in (-1,0,1):
                for df in (-1,0,1):
                    if dr==df==0: continue
                    rr,ff=r+dr,f+df
                    if 0<=rr<8 and 0<=ff<8:
                        t=rr*8+ff; tp=b.get(t)
                        if not tp or not own(tp): ms.append((sq,t,None))
        else:
            dirs = {"r":((1,0),(-1,0),(0,1),(0,-1)),"b":((1,1),(1,-1),(-1,1),(-1,-1)),
                    "q":((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1))}[pl]
            for dr,df in dirs:
                rr,ff=r+dr,f+df
                while 0<=rr<8 and 0<=ff<8:
                    t=rr*8+ff; tp=b.get(t)
                    if not tp: ms.append((sq,t,None))
                    else:
                        if not own(tp): ms.append((sq,t,None))
                        break
                    rr+=dr; ff+=df
    return ms

def make(b, m, white):
    frm, to, pr = m
    cap = b.get(to)
    moved = (pr.upper() if white else pr) if pr else b[frm]
    b[to] = moved; del b[frm]
    return cap, moved

def unmake(b, m, cap, moved):
    frm, to, pr = m
    del b[to]
    b[frm] = moved
    if cap is not None: b[to] = cap

def king_sq(b, white):
    k = "K" if white else "k"
    for s, p in b.items():
        if p == k: return s
    return -1

def legal(b, white):
    out = []
    for m in gen(b, white):
        cap, moved = make(b, m, white)
        ks = king_sq(b, white)
        ok = ks >= 0 and not attacked(b, ks, not white)
        unmake(b, m, cap, moved)
        if ok: out.append(m)
    return out

def evaluate(b, white):
    s = 0
    for sq, p in b.items():
        pl = p.lower(); r, f = divmod(sq, 8)
        i = (7-r)*8+f if p.isupper() else r*8+f
        v = VAL[pl] + PST[pl][i]
        s += v if p.isupper() else -v
    return s if white else -s

NODES = 15000
nodes = 0
stop = False

def search(b, white, depth, alpha, beta, ply):
    global nodes, stop
    if stop: return evaluate(b, white)
    nodes += 1
    if nodes > NODES:
        stop = True
        return evaluate(b, white)
    if depth == 0:
        return evaluate(b, white)
    ms = gen(b, white)
    if not ms:
        return 0
    best = -10**9
    def key(m):
        cap = b.get(m[1])
        s = (10*VAL[cap.lower()] - VAL[b[m[0]].lower()]) if cap else 0
        return -s - (800 if m[2] else 0)
    for m in sorted(ms, key=key):
        cap = b.get(m[1])
        # king capture = previous move left king in check: score as mate
        if cap and cap.lower() == "k":
            return -9999 + ply
        cap, moved = make(b, m, white)
        sc = -search(b, not white, depth-1, -beta, -alpha, ply+1)
        unmake(b, m, cap, moved)
        if sc > best: best = sc
        if best > alpha: alpha = best
        if alpha >= beta: break
        if stop: break
    return best

def uci(m):
    frm, to, pr = m
    return "abcdefgh"[frm%8]+str(8-frm//8)+"abcdefgh"[to%8]+str(8-to//8)+(pr or "")

def think(fen, legal_uci):
    global nodes, stop
    b, white = parse(fen)
    lms = legal(b, white)
    by_u = {uci(m): m for m in lms}
    cand = [u for u in legal_uci if u in by_u] or legal_uci
    if not cand: return None
    def key(u):
        m = by_u[u]; cap = b.get(m[1])
        s = (10*VAL[cap.lower()] - VAL[b[m[0]].lower()]) if cap else 0
        return -s - (800 if m[2] else 0)
    order = sorted(cand, key=key)
    best_u = order[0]
    # iterative deepening: depth 1, 2, 3 — keep best from each completed depth
    for depth in (1, 2, 3):
        nodes = 0; stop = False
        alpha, beta = -10**9, 10**9
        cur_best, cur_s = None, -10**9
        aborted = False
        for u in order:
            m = by_u[u]
            cap, moved = make(b, m, white)
            sc = -search(b, not white, depth, -beta, -alpha, 1)
            unmake(b, m, cap, moved)
            if stop:
                aborted = True
                break
            if sc > cur_s: cur_s, cur_best = sc, u
            if alpha >= beta: break
        if cur_best and not aborted:
            best_u = cur_best
            # put best first for next iteration
            order = [cur_best] + [u for u in order if u != cur_best]
        if aborted or nodes > NODES:
            break
    return best_u

def main():
    while True:
        g = post("/game", {})
        if g.get("status") == "done":
            print("done", g.get("wins"), g.get("draws"), g.get("losses"))
            return
        while g.get("status") == "your_move":
            mv = think(g["fen"], g["legal_moves"])
            g = post("/move", {"game": g["game"], "move": mv})

main()
