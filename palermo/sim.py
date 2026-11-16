"""Rule balance with no models: thousands of games under random (or mildly skilled) play.  python3 sim.py
nose  = chance a town voter votes for a killer when one is on the ballot (0 = pure random voting)
trust = chance the town follows a living officer who has found a killer"""
import random
from collections import Counter


def play(n=6, killers=1, doctor=True, officer=True, self_protect=True, nose=0.0, trust=0.0, shown=False,
         majority=False, quiet_first_night=False, mayor=False, accomplice=False, hunt=0.0, rng=random):
    """majority: killers win only when they OUTNUMBER the others (default: equal is enough).
    quiet_first_night: no kill on night 1 (roles only). mayor: one citizen's vote counts double (option C).
    accomplice: the second evil seat cannot kill, is the one shown, counts as town for parity; town wins when the
    killer is out (option B). hunt: chance the killers target the mayor (public after the first vote) instead of random."""
    roles = ["killer"] * (killers - accomplice) + ["accomplice"] * accomplice + (["officer"] if officer else []) + (["doctor"] if doctor else [])
    roles += (["mayor"] if mayor else []) + ["citizen"] * (n - len(roles) - mayor)
    rng.shuffle(roles)
    alive = dict(enumerate(roles))
    EVIL = ("killer", "accomplice")
    ks = lambda: [i for i, r in alive.items() if r == "killer"]          # count for the win
    evil = lambda: [i for i, r in alive.items() if r in EVIL]            # vote as a block
    town = lambda: [i for i, r in alive.items() if r not in EVIL]
    known, day = ({next(i for i, r in alive.items() if r == "accomplice")} if accomplice and officer
                  else {ks()[0]} if shown and officer else set()), 0      # evil seats the officer knows
    kwin = lambda: not town() or (len(ks()) > n_alive() - len(ks()) if majority else len(ks()) >= n_alive() - len(ks()))
    n_alive = lambda: len(alive)
    while True:
        day += 1
        mayors = [i for i, r in alive.items() if r == "mayor"]
        victim = None if (quiet_first_night and day == 1) else (mayors[0] if mayors and day > 1 and rng.random() < hunt else rng.choice(town()))
        docs = [i for i, r in alive.items() if r == "doctor"]
        saved = rng.choice([i for i in alive if self_protect or i != docs[0]]) if docs else None
        offs = [i for i, r in alive.items() if r == "officer"]
        pool = [i for i in alive if offs and i != offs[0] and i not in known]
        if pool:
            c = rng.choice(pool)
            if alive[c] == "killer":
                known.add(c)
        if victim is not None and victim != saved:
            del alive[victim]
        if not ks():
            return "town", day
        if kwin():
            return "killer", day
        cands = list(alive)
        for _ in range(2):                                   # vote, then one runoff
            votes = []
            for v in alive:
                others = [c for c in cands if c != v]
                bad = [c for c in cands if alive[c] in EVIL and c != v]
                if alive[v] in EVIL:
                    pick = rng.choice([c for c in others if alive[c] not in EVIL] or others)
                elif [c for c in cands if c in known] and offs and offs[0] in alive and rng.random() < trust:
                    pick = rng.choice([c for c in cands if c in known])
                elif bad and rng.random() < nose:
                    pick = rng.choice(bad)
                else:
                    pick = rng.choice(others)
                votes += [pick] * (2 if alive[v] == "mayor" else 1)
            counts = Counter(votes).most_common()
            top = [c for c, k in counts if k == counts[0][1]]
            if len(top) == 1:
                del alive[top[0]]
                break
            cands = top
        if not ks():
            return "town", day
        if kwin():
            return "killer", day


VARIANTS = {
    "6p 1 killer, officer+doctor (current)": {},
    "same, doctor cannot self-protect": {"self_protect": False},
    "same, no doctor": {"doctor": False},
    "same, no officer": {"officer": False},
    "6p 2 killers": {"killers": 2},
    "6p 2 killers, officer shown one (Palermo)": {"killers": 2, "shown": True},
    "  + killers must outnumber": {"killers": 2, "shown": True, "majority": True},
    "  + no kill on night 1": {"killers": 2, "shown": True, "quiet_first_night": True},
    "  + both": {"killers": 2, "shown": True, "majority": True, "quiet_first_night": True},
    "  + both, no doctor self-protect": {"killers": 2, "shown": True, "majority": True, "quiet_first_night": True, "self_protect": False},
    "C: + mayor + outnumber": {"killers": 2, "shown": True, "quiet_first_night": True, "mayor": True, "majority": True},
    "C, killers hunt the mayor 70%": {"killers": 2, "shown": True, "quiet_first_night": True, "mayor": True, "majority": True, "hunt": 0.7},
    "B: killer + accomplice (shown)": {"killers": 2, "accomplice": True, "quiet_first_night": True},
    "7p 2 killers": {"n": 7, "killers": 2},
    "7p 2 killers, officer shown one (Palermo)": {"n": 7, "killers": 2, "shown": True},
    "  + killers must outnumber": {"n": 7, "killers": 2, "shown": True, "majority": True},
    "8p 2 killers, officer shown one (Palermo)": {"n": 8, "killers": 2, "shown": True},
}

if __name__ == "__main__":
    rng, T = random.Random(1), 20000
    print(f"{'variant':42} {'nose=0':>8} {'nose=.3':>8} {'nose=.5':>8}   (killer win %, trust=0.9; avg days in brackets)")
    for name, kw in VARIANTS.items():
        cells = []
        for nose in (0.0, 0.3, 0.5):
            res = [play(nose=nose, trust=0.9, rng=rng, **kw) for _ in range(T)]
            kw_ = sum(r == "killer" for r, _ in res) / T
            cells.append(f"{100 * kw_:4.0f}% [{sum(d for _, d in res) / T:.1f}]")
        print(f"{name:42} " + " ".join(f"{c:>8}" for c in cells))
