#!/usr/bin/env python3
"""Unit tests for funmeter.py on a hand-made game; no model call."""
import json, unittest
import funmeter as fm

P = [dict(name=n, role=r, shown=s) for n, r, s in [("Ann", "killer", True), ("Bob", "killer", False), ("Cat", "officer", False),
                                                     ("Dan", "doctor", False), ("Eve", "citizen", False)]]
EV = [
    {"type": "cast", "players": P},                                                         # 0
    {"type": "phase", "text": "Night 1", "kind": "night"},                                  # 1
    {"type": "thought", "name": "Ann", "text": "Stay calm."},                               # 2
    {"type": "whisper", "name": "Ann", "to": "Bob", "text": "Lie low."},                    # 3
    {"type": "phase", "text": "Day 1", "kind": "day"},                                      # 4
    {"type": "thought", "name": "Cat", "text": "Ann is the shown one."},                    # 5
    {"type": "say", "name": "Cat", "text": "I am the officer and Ann was shown to me.", "claim": "officer", "lean": "Ann"},
    {"type": "thought", "name": "Eve", "text": "Hmm."},                                     # 7
    {"type": "say", "name": "Bob", "text": "Cat is lying, I am the real officer here.", "claim": "officer", "lean": "Cat"},
    {"type": "say", "name": "Dan", "text": "I believe Cat completely.", "lean": "Ann"},     # 9  leader Ann (2)
    {"type": "say", "name": "Eve", "text": "Bob makes sense to me.", "lean": "Cat"},
    {"type": "say", "name": "Ann", "text": "Vote Cat, she lies.", "lean": "Cat"},          # 11 leader Cat (3): a shift
    {"type": "say", "name": "Eve", "text": "Bob makes total sense to me honestly.", "lean": "Cat"},  # near repeat of 10
    {"type": "memory", "name": "Eve", "text": "x"},
    {"type": "clock", "left": 3, "total": 30},
    {"type": "votes", "votes": [["Ann", "Cat", ""], ["Bob", "Cat", ""], ["Eve", "Cat", ""], ["Cat", "Ann", ""], ["Dan", "Ann", ""]]},
    {"type": "say", "name": "Cat", "text": "You will regret this.", "why": "last words"},
    {"type": "death", "name": "Cat", "role": "officer", "how": "vote"},
    {"type": "ghost", "name": "Cat", "text": "Told you."},
    {"type": "ghost", "name": "Cat", "text": "…"},
    {"type": "phase", "text": "Night 2", "kind": "night"},
    {"type": "night_action", "name": "Bob", "action": "kill", "target": "Dan"},
    {"type": "death", "name": "Dan", "role": None, "how": "night"},
    {"type": "gm", "text": "Killers win.", "aside": True},
    {"type": "recap", "text": "Bob lied."},
    {"type": "end", "winner": "killer", "t": 120},
]


class Render(unittest.TestCase):
    def setUp(self):
        self.text = fm.render(EV)

    def test_roles_and_order(self):
        self.assertIn("Ann killer (shown to the officer)", self.text)
        self.assertIn("Bob killer (hidden)", self.text)
        lines = self.text.splitlines()[1:]
        idx = [int(l[1:l.index("]")]) for l in lines]
        self.assertEqual(idx, sorted(idx))

    def test_thought_only_with_own_line(self):
        self.assertIn('[3] Ann whispers to Bob: "Lie low." [thinks: Stay calm.]', self.text)
        self.assertIn("[thinks: Ann is the shown one.]", self.text)
        self.assertNotIn("Hmm.", self.text)              # Eve's thought is followed by Bob's line, not hers

    def test_hidden_internals_and_cards(self):
        for gone in ("memory", "clock", "night_action", "…"):
            self.assertNotIn(gone, self.text)
        self.assertIn("VOTE: Cat 3 (Ann, Bob, Eve); Ann 2 (Cat, Dan)", self.text)
        self.assertIn("card turned: OFFICER", self.text)
        self.assertIn("Dan (killed in the night), card stays face down", self.text)
        self.assertIn("(last words)", self.text)
        self.assertIn("<claims officer>", self.text)
        self.assertIn("(dead, to the audience only): \"Told you.\"", self.text)
        self.assertIn("HOST (aside): Killers win.", self.text)
        self.assertIn("END: the killers win.", self.text)


GOOD = {"criteria": {k: {"score": 3, "evidence": "x"} for k in fm.KEYS}, "score": 64,
        "moments": [{"at": 6, "text": "claim"}, {"at": 999, "text": "bad index"}],
        "dull": [{"from": 9, "to": 12, "why": "slow"}, {"from": 12, "to": 9, "why": "backwards"}], "why": "ok"}


class Validate(unittest.TestCase):
    idx = {6, 9, 12}

    def test_good_with_prose_around(self):
        d = fm.validate("Sure:\n" + json.dumps(GOOD) + "\nDone.", self.idx)
        self.assertEqual(d["score"], 64)
        self.assertEqual([m["at"] for m in d["moments"]], [6])
        self.assertEqual(d["dull"], [{"from": 9, "to": 12, "why": "slow"}])

    def test_bad(self):
        for bad in ("no json", json.dumps({**GOOD, "score": 140}),
                    json.dumps({**GOOD, "criteria": {**GOOD["criteria"], "irony": {"score": 7}}}),
                    json.dumps({k: v for k, v in GOOD.items() if k != "criteria"})):
            with self.assertRaises(ValueError):
                fm.validate(bad, self.idx)

    def test_retry_once(self):
        replies = iter(["garbage", json.dumps(GOOD)])
        d = fm.judge_one("m", "text", self.idx, ask=lambda m, p: next(replies))
        self.assertEqual(d["score"], 64)
        with self.assertRaises(RuntimeError):
            fm.judge_one("m", "text", self.idx, ask=lambda m, p: "garbage")

    def test_combine_means(self):
        a = fm.validate(json.dumps(GOOD), self.idx)
        b = json.loads(json.dumps(a))
        b["score"], b["criteria"]["irony"]["score"] = 80, 5
        r = fm.combine("g-1", {"j1": a, "j2": b}, {})
        self.assertEqual(r["score"], 72)
        self.assertEqual(r["criteria"]["irony"]["score"], 4)
        self.assertEqual(set(r), {"name", "score", "why", "moments", "dull", "criteria", "judges", "signals"})


class Signals(unittest.TestCase):
    def test_signals(self):
        s = fm.signals(EV)
        self.assertEqual(s["days"], 1)
        self.assertEqual(s["lean_shifts"], [1])
        self.assertEqual(s["counter_claims"], 1)
        self.assertEqual(s["wrong_voteouts"], 1)
        self.assertEqual(s["vote_margin_mean"], 1)
        self.assertEqual(s["day_lines"], 6)
        self.assertAlmostEqual(s["repeat_share"], round(1 / 6, 3))
        self.assertTrue(s["hidden_survived"])
        self.assertEqual(s["minutes"], 2.0)
        self.assertEqual(s["winner"], "killer")

    def test_spearman(self):
        self.assertAlmostEqual(fm.spearman([1, 2, 3, 4], [10, 20, 30, 40]), 1)
        self.assertAlmostEqual(fm.spearman([1, 2, 3, 4], [4, 3, 2, 1]), -1)


if __name__ == "__main__":
    unittest.main()
