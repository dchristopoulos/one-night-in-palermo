#!/usr/bin/env python3
"""Checks for stats.py on a tiny hand-made game.   python3 stats_test.py"""
import unittest

from stats import analyse, d1kind, fate

CAST = {"type": "cast", "players": [
    {"name": "A", "role": "killer", "shown": True}, {"name": "B", "role": "killer", "shown": False},
    {"name": "C", "role": "officer"}, {"name": "D", "role": "doctor"}, {"name": "E", "role": "citizen"},
    {"name": "F", "role": "citizen"}, {"name": "G", "role": "citizen"}]}
SAY = lambda who, text, **kw: {"type": "say", "name": who, "text": text, **kw}
GAME = [CAST,
        {"type": "phase", "text": "Night 1", "kind": "night"},
        {"type": "phase", "text": "Day 1", "kind": "day"},
        {"type": "clock", "left": 4, "total": 4},
        SAY("E", "Who is it?"), {"type": "clock", "left": 3, "total": 4},
        SAY("C", "I am the officer and A is a killer.", claim="officer"), {"type": "clock", "left": 2, "total": 4},
        SAY("B", "I am the officer, C lies.", claim="officer"), {"type": "clock", "left": 1, "total": 4},
        {"type": "votes", "runoff": False, "votes": [["B", "A", ""], ["C", "A", ""], ["A", "C", ""]]},
        SAY("A", "Fine.", why="last words"),
        {"type": "death", "name": "A", "how": "vote", "role": "killer"},
        {"type": "phase", "text": "Night 2", "kind": "night"},
        {"type": "night_action", "name": "B", "action": "kill", "target": "C"},
        {"type": "night_action", "name": "D", "action": "save", "target": "C"},
        {"type": "phase", "text": "Day 2", "kind": "day"},
        {"type": "clock", "left": 4, "total": 4},
        SAY("C", "It was B, the line was cut…"), {"type": "clock", "left": 0, "total": 4},
        {"type": "votes", "runoff": False, "votes": [["B", "C", ""], ["C", "B", ""]]},
        {"type": "votes", "runoff": True, "votes": [["B", "C", ""], ["C", "B", ""], ["E", "B", ""]]},
        {"type": "death", "name": "B", "how": "vote", "role": "killer"},
        {"type": "end", "winner": "town", "t": 600}]


class Stats(unittest.TestCase):
    def setUp(self):
        self.g = analyse(GAME, "t-1")

    def test_ending(self):
        self.assertEqual(self.g["winner"], "town")
        self.assertEqual(self.g["ending"], "last killer voted out day 2")
        self.assertEqual(self.g["minutes"], 10)

    def test_days(self):
        d1, d2 = self.g["days"][1], self.g["days"][2]
        self.assertEqual((d1["lines"], d1["budget"], d1["left"], d1["runoffs"]), (3, 4, 1, 0))   # early vote
        self.assertEqual((d2["lines"], d2["left"], d2["runoffs"]), (1, 0, 1))                    # at budget, tie

    def test_officer_and_killers(self):
        self.assertEqual(self.g["claims"], [("C", 1, 2, True), ("B", 1, 3, False)])
        self.assertEqual(fate(self.g, "C"), "alive")
        self.assertEqual(fate(self.g, "B"), "voted out day 2")
        self.assertEqual(d1kind(self.g), "shown killer")
        self.assertTrue(self.g["bus"])

    def test_doctor_and_talk(self):
        self.assertEqual(self.g["saves"], 1)
        self.assertEqual(self.g["guards"], [(2, "C", True)])
        self.assertEqual(self.g["cut"], 1)
        self.assertEqual(self.g["lines"]["C"], 2)          # last words are not day talk

    def test_unfinished_is_skipped(self):
        self.assertIsNone(analyse(GAME[:-1]))
        self.assertIsNone(analyse(GAME[:-1] + [{"type": "end", "winner": "stopped"}]))


if __name__ == "__main__":
    unittest.main()
