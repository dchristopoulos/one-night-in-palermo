"""Role comprehension, no game: every seat answers the narrator privately. ~20 s.
python3 check_roles.py [--roles killer=2,officer,doctor] [--seed N]"""
import sys
USER_ARGS = sys.argv[1:]
sys.argv = [sys.argv[0], "--fast", "--tag", "check"] + USER_ARGS
import game

g = game.Game()
g.files = []
game.ensure_local({p["model"].partition(":")[2] for p in g.players if p["model"].startswith("local:")})
q = ("Answer the narrator privately in three short sentences: (1) your role and your team; (2) what you know for "
     "sure about other players and where that knowledge comes from; (3) what you will do tonight and why. "
     "Nobody else hears this.")
for p, r in zip(g.players, g.parallel([lambda p=p: g.act(p, q, "ANSWER") for p in g.players])):
    print(f"\n{p['name']} [{p['role']}{' SHOWN' if p.get('shown') else ''}]: {r['text']}")
