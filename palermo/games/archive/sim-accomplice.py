import random
from collections import Counter

def play(n=6, nose=0.0, trust=0.9, shown="accomplice", rng=random):
    """One killer + one accomplice (evil vote and whispers, cannot kill, does not count for the evil win).
    Quiet night 1. The officer is shown one evil player (`shown`) at the start and checks nightly (checks reveal the killer only)."""
    roles = ["killer", "accomplice", "officer", "doctor"] + ["citizen"] * (n - 4)
    rng.shuffle(roles); alive = dict(enumerate(roles)); day = 0
    evil = lambda: [i for i, r in alive.items() if r in ("killer", "accomplice")]
    town = lambda: [i for i, r in alive.items() if r not in ("killer", "accomplice")]
    killer = lambda: [i for i, r in alive.items() if r == "killer"]
    known = {next(i for i, r in alive.items() if r == shown)}
    while True:
        day += 1
        if day > 1 and killer():
            victim = rng.choice(town())
            docs = [i for i, r in alive.items() if r == "doctor"]
            saved = rng.choice(list(alive)) if docs else None
            if victim != saved: del alive[victim]
        offs = [i for i, r in alive.items() if r == "officer"]
        pool = [i for i in alive if offs and i != offs[0] and i not in known]
        if pool:
            c = rng.choice(pool)
            if alive[c] == "killer": known.add(c)
        if not killer(): return "town", day
        if len(town()) <= len(evil()): return "killer", day
        cands = list(alive)
        for _ in range(3):
            votes = Counter()
            for v in alive:
                others = [c for c in cands if c != v]; bad = [c for c in cands if alive[c] in ("killer", "accomplice") and c != v]
                lead = [c for c in cands if c in known]
                if alive[v] in ("killer", "accomplice"): pick = rng.choice([c for c in others if alive[c] not in ("killer", "accomplice")] or others)
                elif lead and offs and offs[0] in alive and rng.random() < trust: pick = rng.choice(lead)
                elif bad and rng.random() < nose: pick = rng.choice(bad)
                else: pick = rng.choice(others)
                votes[pick] += 1
            counts = votes.most_common(); top = [c for c, k in counts if k == counts[0][1]]
            if len(top) == 1: del alive[top[0]]; break
            cands = top
        if not killer(): return "town", day
        if len(town()) <= len(evil()): return "killer", day

rng = random.Random(5); T = 20000
print(f"{'6 seats: killer + accomplice, quiet night 1':48} {'nose=0':>8} {'nose=.3':>8} {'nose=.5':>8}")
for name, kw in {"officer shown the accomplice": {}, "officer shown the killer": {"shown": "killer"}}.items():
    cells = []
    for nose in (0, .3, .5):
        res = [play(nose=nose, rng=rng, **kw) for _ in range(T)]
        cells.append(f"{100 * sum(r == 'killer' for r, _ in res) / T:4.0f}% [{sum(d for _, d in res) / T:.1f}]")
    print(f"{name:48} " + " ".join(f"{c:>8}" for c in cells))
