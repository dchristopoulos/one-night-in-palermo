"""Night-1 probe: how predictable is the first night?  python3 probe.py [N] [--blind] [--roles ...]
Runs opening lines + the real night 1 N times with the real models (no day) and prints how often the
doctor saves the victim, the officer finds a killer, and (Palermo) whether the hidden killer agrees."""
import collections, json, sys
USER_ARGS = sys.argv[1:]
sys.argv = [sys.argv[0], "--fast", "--tag", "probe", "--kill-night1"] + [a for a in USER_ARGS if not a.isdigit() and a != "--blind"]   # it probes the night-1 kill
import game

BLIND = "--blind" in USER_ARGS


def one():
    g = game.Game()
    g.files = []
    if not BLIND:
        g.intro()
    g.night(1)
    acts = {(e["action"], e["name"]): e["target"] for e in g.events if e["type"] == "night_action"}
    role = {p["name"]: p["role"] for p in g.players}
    kill = next(t for (a, n), t in acts.items() if a == "kill")
    save = next((t for (a, n), t in acts.items() if a == "save"), None)
    check = next((t for (a, n), t in acts.items() if a == "check"), None)
    proposal = next((t for (a, n), t in acts.items() if a == "propose"), None)
    return {"killers": [p["name"] + ("*" if p.get("shown") else "") for p in g.players if p["role"] == "killer"],
            "doctor": next((p["name"] for p in g.players if p["role"] == "doctor"), None),
            "officer": next((p["name"] for p in g.players if p["role"] == "officer"), None),
            "proposal": proposal, "kill": kill, "save": save, "check": check,
            "check_role": role.get(check), "hidden_agreed": (proposal == kill) if proposal else None}


if __name__ == "__main__":
    N = int(next((a for a in USER_ARGS if a.isdigit()), 8))
    game.ensure_local({p["model"].partition(":")[2] for p in game.Game().players if p["model"].startswith("local:")})
    rows = []
    for i in range(N):
        r = one()
        rows.append(r)
        print(i + 1, json.dumps(r), flush=True)
    saved = sum(r["kill"] == r["save"] for r in rows)
    hit = sum(r["check_role"] == "killer" for r in rows)
    selfp = sum(r["save"] == r["doctor"] for r in rows)
    agreed = [r["hidden_agreed"] for r in rows if r["hidden_agreed"] is not None]
    print(f"\nN={N}  doctor saved the victim: {saved}/{N}  officer found a killer: {hit}/{N}  doctor self-protect: {selfp}/{N}"
          + (f"  hidden killer agreed with the proposal: {sum(agreed)}/{len(agreed)}" if agreed else ""))
    print("kill targets:", dict(collections.Counter(r["kill"] for r in rows)))
    print("save targets:", dict(collections.Counter(r["save"] for r in rows)))
    print("check targets:", dict(collections.Counter(r["check"] for r in rows)))
