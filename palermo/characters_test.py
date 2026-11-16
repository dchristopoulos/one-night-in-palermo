#!/usr/bin/env python3
"""Checks for characters.py on a tiny hand-made game.   python3 characters_test.py"""
import json, os, tempfile, unittest

from characters import read, tables, tally, walk
from stats import analyse

CAST = {"type": "cast", "players": [
    {"name": "A", "role": "killer", "shown": True}, {"name": "B", "role": "killer", "shown": False},
    {"name": "C", "role": "officer"}, {"name": "D", "role": "doctor"}, {"name": "E", "role": "citizen"},
    {"name": "F", "role": "citizen"}, {"name": "G", "role": "citizen"}]}
SAY = lambda who, text, **kw: {"type": "say", "name": who, "text": text, **kw}
VOTE = lambda pairs, runoff=False: {"type": "votes", "runoff": runoff, "votes": [[v, t, ""] for v, t in pairs]}
GAME = [CAST,
        SAY("E", "Good luck to all of you.", why="before the game"),
        {"type": "phase", "text": "Night 1", "kind": "night"},
        {"type": "phase", "text": "Day 1", "kind": "day"},
        SAY("E", "Who is it then?", lean="F"),
        SAY("C", "I am the officer and A is a killer.", claim="officer", lean="A"),
        SAY("A", "I am the officer, C lies.", claim="officer", lean="C"),
        SAY("E", "I believe C here.", lean="A"),
        {"type": "pass", "name": "F"},
        VOTE([("A", "C"), ("B", "A"), ("C", "A"), ("D", "A"), ("E", "A"), ("F", "A"), ("G", "C")]),
        SAY("A", "You will regret this.", why="last words"),
        {"type": "death", "name": "A", "how": "vote", "role": "killer"},
        {"type": "phase", "text": "Night 2", "kind": "night"},
        {"type": "night_action", "name": "B", "action": "kill", "target": "C"},
        {"type": "night_action", "name": "D", "action": "save", "target": "C"},
        {"type": "phase", "text": "Day 2", "kind": "day"},
        SAY("C", "Nobody died, so B is next.", lean="B"),
        VOTE([("B", "E"), ("C", "B"), ("D", "B"), ("E", "B"), ("F", "E"), ("G", "E")]),
        VOTE([("B", "E"), ("C", "B"), ("D", "B"), ("E", "B"), ("F", "B"), ("G", "E")], runoff=True),
        {"type": "death", "name": "B", "how": "vote", "role": "killer"},
        {"type": "end", "winner": "town", "t": 600}]


class Characters(unittest.TestCase):
    def setUp(self):
        self.S, self.out_days = tally([(analyse(GAME, "t-1"), GAME)])

    def test_killers(self):
        a, b = self.S["A"], self.S["B"]
        self.assertEqual((a["k games"], a["k won"], a["k voted out"], a["k claimed"], a["k shown"]), (1, 0, 1, 1, 1))
        self.assertEqual((a["k received"], a["k faced"]), (5, 1))
        self.assertEqual((b["k received"], b["k faced"]), (3, 2))       # the runoff is not a vote faced
        self.assertEqual((b["k on partner"], b["k cast"]), (1, 2))      # B voted A, the partner, on day 1
        self.assertEqual(self.out_days["B"], [2])

    def test_town(self):
        c, e = self.S["C"], self.S["E"]
        self.assertEqual((c["t games"], c["t won"], c["t on killer"], c["t cast"]), (1, 1, 2, 2))
        self.assertEqual((e["t on killer"], e["t cast"], e["t received"], e["t faced"]), (2, 2, 3, 2))
        self.assertEqual(sum(self.S[w]["t false claim"] for w in "DEFG"), 0)

    def test_officer_and_doctor(self):
        c, d = self.S["C"], self.S["D"]
        self.assertEqual((c["o games"], c["o claimed"], c["o named d1"], c["o voted out"], c["o shown out"]),
                         (1, 1, 1, 0, 1))
        self.assertEqual((d["d games"], d["d acted"], d["d saves"]), (1, 1, 1))

    def test_talk_and_leans(self):
        f = walk(GAME)
        self.assertEqual(self.S["E"]["lines"], 2)                    # the before-the-game line is not day talk
        self.assertEqual(self.S["E"]["words"], 8)
        self.assertEqual(self.S["F"]["passes"], 1)
        self.assertEqual(f["lean1"], {"E": "A", "C": "A", "A": "C"})   # the last lean of day 1 counts
        self.assertEqual((self.S["E"]["lean1"], self.S["E"]["lean1 out"]), (1, 1))
        self.assertEqual((self.S["A"]["lean1"], self.S["A"]["lean1 out"]), (1, 0))
        self.assertEqual(sum(self.S[w]["k games"] for w in self.S), 2)
        self.assertEqual(len(tables(self.S, self.out_days, 1)), 4)

    def test_unfinished_and_broken_files_are_skipped(self):
        with tempfile.TemporaryDirectory() as d:
            paths = [os.path.join(d, n) for n in ("t-1.json", "t-2.json", "t-3.json")]
            for path, text in zip(paths, (json.dumps(GAME), json.dumps(GAME[:-1]),   # finished; no end event yet
                                          json.dumps(GAME)[:200])):                # still being written
                with open(path, "w") as fh:
                    fh.write(text)
            self.assertEqual([g["name"] for g, _ in read(paths)], ["t-1"])


if __name__ == "__main__":
    unittest.main()
