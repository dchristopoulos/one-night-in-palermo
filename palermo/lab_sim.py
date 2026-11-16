"""Balance sim for the optional rule switches, no models.  python3 lab_sim.py
(random play; nose = chance a town voter picks a killer; trust = chance town follows the officer's known killer)."""
import random
from collections import Counter

def play(n=6, nose=0.0, trust=0.9, quiet=True, hunter=False, will=False, ghost=False, self_save=True, jester=False, rng=random):
    roles = ["killer", "killer", "officer", "doctor"] + (["jester"] if jester else [])
    roles += ["citizen"] * (n - len(roles))
    rng.shuffle(roles)
    alive = dict(enumerate(roles))
    ks = lambda: [i for i, r in alive.items() if r == "killer"]
    town = lambda: [i for i, r in alive.items() if r != "killer"]
    known = {ks()[0]}
    officer_voice = True          # the officer's knowledge can still reach the table
    ghosts = []                   # roles of dead players with an unused vote
    def kwin():
        k, o = len(ks()), len(alive) - len(ks())
        return k > o or (k == 1 == o)
    def pick_for(role, me, cands):
        others = [c for c in cands if c != me]
        bad = [c for c in cands if alive.get(c) == "killer" and c != me]
        if role == "killer":
            return rng.choice([c for c in others if alive[c] != "killer"] or others)
        if role == "jester":
            return rng.choice(others)
        kn = [c for c in cands if c in known]
        if kn and officer_voice and rng.random() < trust:
            return rng.choice(kn)
        if bad and rng.random() < nose:
            return rng.choice(bad)
        return rng.choice(others)
    day = 0
    while True:
        day += 1
        victim = None if (quiet and day == 1) else rng.choice(town())
        docs = [i for i, r in alive.items() if r == "doctor"]
        saved = rng.choice([i for i in alive if self_save or i != docs[0]]) if docs else None
        offs = [i for i, r in alive.items() if r == "officer"]
        pool = [i for i in alive if offs and i != offs[0] and i not in known]
        if pool:
            c = rng.choice(pool)
            if alive[c] == "killer":
                known.add(c)
        if victim is not None and victim != saved:
            if alive[victim] == "officer" and not will:
                officer_voice = False
            ghosts.append(alive.pop(victim))
        if not ks(): return "town", day
        if kwin(): return "killer", day
        cands = list(alive)
        use_ghosts = ghost and len(alive) <= 4
        for _ in range(2):
            votes = [pick_for(alive[v], v, cands) for v in alive]
            if use_ghosts:
                votes += [pick_for(g, None, cands) for g in ghosts]
            counts = Counter(votes).most_common()
            top = [c for c, k in counts if k == counts[0][1]]
            if len(top) == 1:
                role = alive[top[0]]
                if role == "jester": return "jester", day
                if role == "officer": officer_voice = False   # voted out: nobody believed them
                shooter = top[0]
                ghosts.append(alive.pop(shooter))
                if hunter and len(alive) > 2:
                    cands2 = list(alive)
                    alive[shooter] = role                      # so pick_for sees the role
                    tgt = pick_for(role, shooter, cands2)
                    del alive[shooter]
                    if alive[tgt] == "officer": officer_voice = False
                    ghosts.append(alive.pop(tgt))
                break
            cands = top
        if use_ghosts: ghosts = []
        if not ks(): return "town", day
        if kwin(): return "killer", day

V = {
 "today's default (quiet night 1, outnumber, 1v1)": {},
 "kill on night 1": {"quiet": False},
 "no doctor self-save": {"self_save": False},
 "will (a dead officer's knowledge survives a night kill)": {"will": True},
 "hunter (voted-out takes one along)": {"hunter": True},
 "ghost votes (dead vote once, when 4 are left)": {"ghost": True},
 "will + ghost votes": {"will": True, "ghost": True},
 "will + hunter": {"will": True, "hunter": True},
 "kill night 1 + will + ghost votes": {"quiet": False, "will": True, "ghost": True},
 "jester replaces a citizen": {"jester": True},
 "7 seats": {"n": 7},
 "7 seats + jester": {"n": 7, "jester": True},
 "7 seats, kill on night 1": {"n": 7, "quiet": False},
 "7 seats + will": {"n": 7, "will": True},
 "7 seats, kill on night 1 + will": {"n": 7, "quiet": False, "will": True},
 "7 seats + hunter": {"n": 7, "hunter": True},
}
rng, T = random.Random(1), 20000
print(f"{'variant':58} {'follow officer 30%':>26} {'follow officer 90%':>26}")
print(f"{'':58} {'nose 0':>8} {'nose .3':>8} {'days':>5}   {'nose 0':>8} {'nose .3':>8} {'days':>5}")
for name, kw in V.items():
    row = []
    for trust in (0.3, 0.9):
        for nose in (0.0, 0.3):
            res = [play(nose=nose, trust=trust, rng=rng, **kw) for _ in range(T)]
            k = sum(r == "killer" for r, _ in res) / T
            j = sum(r == "jester" for r, _ in res) / T
            row.append(f"{100*k:3.0f}%" + (f"/j{100*j:.0f}" if j else ""))
        row.append(f"{sum(d for _, d in res)/T:.1f}")
    print(f"{name:58} {row[0]:>8} {row[1]:>8} {row[2]:>5}   {row[3]:>8} {row[4]:>8} {row[5]:>5}")
