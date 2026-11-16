"""The games index (view.py): python3 -m unittest view_test"""
import json
import os
import pathlib
import tempfile
import time
import unittest

import view

CAST = {"type": "cast", "dry": False, "players": [
    {"name": "Sonnet", "model": "claude:sonnet", "role": "killer", "seat": 0},
    {"name": "Haiku", "model": "claude:haiku", "role": "citizen", "seat": 1},
    {"name": "Gemma", "model": "local:gemma", "role": "officer", "seat": 2}]}


def game(winner="town", days=2, t=600.0, dry=False):
    ev = [{**CAST, "dry": dry, "t": 0}]
    for d in range(1, days + 1):
        ev += [{"type": "phase", "text": f"Night {d}", "kind": "night", "t": 1}, {"type": "phase", "text": f"Day {d}", "kind": "day", "t": 2}]
    return ev + ([{"type": "end", "winner": winner, "t": t}] if winner else [{"type": "say", "name": "Haiku", "text": "hm", "t": t}])


class Index(unittest.TestCase):
    def setUp(self):
        view._cache.clear()
        self.dir = pathlib.Path(tempfile.mkdtemp())
        self.now = time.time()

    def put(self, name, events, age=3600):
        p = self.dir / f"{name}.json"
        p.write_text(json.dumps(events) if not isinstance(events, str) else events)
        os.utime(p, (self.now - age, self.now - age))
        return p

    def index(self):
        return {g["name"]: g for g in view.games_index(self.dir, now=self.now)["games"]}

    def test_summary_fields(self):
        self.put("run81-3", game("killer", days=3, t=669.3))
        g = self.index()["run81-3"]
        self.assertEqual((g["tag"], g["n"], g["file"]), ("run81", 3, "games/run81-3.json"))
        self.assertEqual((g["winner"], g["days"], g["minutes"], g["seats"]), ("killer", 3, 11.2, 3))
        self.assertEqual(g["killers"], ["Sonnet"])
        self.assertEqual(g["cast"][2], {"name": "Gemma", "model": "local:gemma", "role": "officer"})
        self.assertFalse(g["live"])
        self.assertAlmostEqual(g["started"], self.now - 3600 - 669.3, delta=1)

    def test_tags(self):
        self.assertEqual(view.tag_of("fin71-4"), ("fin71", 4))
        self.assertEqual(view.tag_of("bake-A-2"), ("bake-A", 2))
        self.assertEqual(view.tag_of("20261027-044948"), (None, None))
        self.assertEqual(view.tag_of("showcase"), (None, None))

    def test_skips_dry_fixtures_and_junk(self):
        self.put("dry-1", game(dry=True))
        self.put("20261027-044906-dry", game())
        self.put("ui-fixture-7", game())
        self.put("broken", "{not json")
        self.put("notes", {"a": 1})
        self.assertEqual(self.index(), {})

    def test_live_and_abandoned(self):
        self.put("run81-4", game(None), age=30)        # being written
        self.put("run81-2", game(None), age=3600)      # abandoned an hour ago
        ix = self.index()
        self.assertTrue(ix["run81-4"]["live"])
        self.assertIsNone(ix["run81-4"]["winner"])
        self.assertNotIn("run81-2", ix)

    def test_live_expires_without_a_new_write(self):
        self.put("run81-5", game(None), age=30)
        self.assertIn("run81-5", self.index())
        self.now += view.LIVE_SECONDS                    # the engine stopped writing
        self.assertNotIn("run81-5", self.index())

    def test_cache_and_mid_write(self):
        p = self.put("eve41-1", game("town"))
        self.assertEqual(self.index()["eve41-1"]["winner"], "town")
        p.write_text('[{"type": "cast"')                # caught mid-write: the last good summary stays
        self.assertEqual(self.index()["eve41-1"]["winner"], "town")
        self.put("eve41-1", game("killer"))
        self.assertEqual(self.index()["eve41-1"]["winner"], "killer")

    def test_newest_first(self):
        self.put("a-1", game(), age=7200)
        self.put("a-2", game(), age=60)
        self.assertEqual([g["name"] for g in view.games_index(self.dir, now=self.now)["games"]], ["a-2", "a-1"])

    def talk(self):
        """A finished game whose events are: 0 cast, 1 before the game, 2 day phase, 3 a ghost, 4 an out player, 5 last
        words, 6 table talk (Haiku), 7 table talk (Gemma), 8 end, 9 a confession."""
        return [{**CAST, "t": 0},
                {"type": "say", "name": "Gemma", "text": "Good luck all.", "why": "before the game", "t": 1},
                {"type": "phase", "text": "Day 1", "kind": "day", "t": 2},
                {"type": "ghost", "name": "Sonnet", "text": "They will never see it.", "t": 3},
                {"type": "say", "name": "Sonnet", "text": "I was framed.", "out": True, "t": 4},
                {"type": "say", "name": "Sonnet", "text": "Remember me.", "why": "last words", "t": 5},
                {"type": "say", "name": "Haiku", "text": "Sonnet voted last, and fast.", "why": "takes the floor", "t": 6},
                {"type": "say", "name": "Gemma", "text": "I agree with Haiku.", "why": "answers Haiku", "t": 7},
                {"type": "end", "winner": "town", "t": 8},
                {"type": "say", "name": "Sonnet", "text": "It was me.", "why": "confession", "t": 9}]

    def put_fun(self, name, data):
        (self.dir / "fun").mkdir(exist_ok=True)
        (self.dir / "fun" / f"{name}.json").write_text(json.dumps(data) if not isinstance(data, str) else data)

    def test_fun_score_and_quote(self):
        self.put("sun15-2", self.talk())
        self.put("sun15-3", self.talk())
        self.put_fun("sun15-2", {"name": "sun15-2", "score": 81, "why": "A late swing.", "dull": [],
                                 "moments": [{"at": 1, "text": "x"}, {"at": 3, "text": "x"}, {"at": 4, "text": "x"},
                                             {"at": 5, "text": "x"}, {"at": 9, "text": "x"}, {"at": 99, "text": "x"},
                                             {"at": 7, "text": "agrees"}, {"at": 6, "text": "the tell"}]})
        ix = self.index()
        self.assertEqual(ix["sun15-2"]["fun"], {"score": 81, "why": "A late swing.",
                                                "quote": {"name": "Gemma", "text": "I agree with Haiku."}})
        self.assertNotIn("fun", ix["sun15-3"])           # no fun file: no key at all

    def test_fun_without_a_talk_moment_has_no_quote(self):
        self.put("sun15-4", self.talk())
        self.put_fun("sun15-4", {"score": 40, "why": "Flat.", "moments": [{"at": 5, "text": "last words"}, {"at": 9}]})
        self.assertEqual(self.index()["sun15-4"]["fun"], {"score": 40, "why": "Flat."})

    def test_fun_file_broken_or_unscored_is_ignored(self):
        self.put("sun15-5", self.talk())
        self.put("sun15-6", self.talk())
        self.put_fun("sun15-5", "{not json")
        self.put_fun("sun15-6", {"why": "no score"})
        ix = self.index()
        self.assertNotIn("fun", ix["sun15-5"])
        self.assertNotIn("fun", ix["sun15-6"])

    def test_fun_follows_the_file(self):
        self.put("sun15-7", self.talk())
        self.put_fun("sun15-7", {"score": 10, "why": "a"})
        self.assertEqual(self.index()["sun15-7"]["fun"]["score"], 10)
        p = self.dir / "fun" / "sun15-7.json"
        p.write_text(json.dumps({"score": 90, "why": "b"}))
        os.utime(p, (self.now + 5, self.now + 5))
        self.assertEqual(self.index()["sun15-7"]["fun"]["score"], 90)


class Export(unittest.TestCase):
    def g(self, name, mtime, score=None, finished=True):
        tag, n = view.tag_of(name)
        return {"name": name, "tag": tag, "n": n, "started": mtime - 600, "mtime": mtime, "finished": finished,
                "winner": "town" if finished else None, **({"fun": {"score": score, "why": ""}} if score is not None else {})}

    def test_pick(self):
        games = [self.g("a-1", 100), self.g("a-2", 110, 50), self.g("b-1", 200), self.g("b-2", 210, 90),
                 self.g("c-1", 300), self.g("c-2", 310, finished=False), self.g("20261027-044948", 400)]
        names = lambda gs: sorted(g["name"] for g in gs)
        self.assertEqual(names(view.pick(games)), ["b-1", "b-2", "c-1"])                 # the two newest evenings
        self.assertEqual(names(view.pick(games, tags=["a"])), ["a-1", "a-2"])
        self.assertEqual([g["name"] for g in view.pick(games, best=1)], ["b-2"])          # highest score
        self.assertEqual([g["name"] for g in view.pick(games, best=5)], ["b-2", "a-2"])
        self.assertEqual(names(view.pick(games, tags=["c"], best=3)), ["c-1"])           # nothing scored: newest evening

    def test_export_writes_a_static_site(self):
        root = pathlib.Path(tempfile.mkdtemp())
        dist, games = root / "dist", root / "games"
        (dist / "assets").mkdir(parents=True)
        (dist / "index.html").write_text('<script type="module" src="./assets/index.js"></script>')
        (dist / "assets" / "index.js").write_text("")
        games.mkdir()
        (games / "r7a-1.json").write_text(json.dumps(game("town")))
        names = view.export(root / "site", tags=["r7a"], folder=games, dist=dist)
        self.assertEqual(names, ["r7a-1"])
        ix = json.loads((root / "site" / "games" / "index.json").read_text())
        self.assertTrue(ix["static"])
        self.assertEqual([(g["file"], g["live"]) for g in ix["games"]], [("games/r7a-1.json", False)])
        for f in ("index.html", "assets/index.js", "games/r7a-1.json", "avatars/Opus.png"):
            self.assertTrue((root / "site" / f).exists(), f)


if __name__ == "__main__":
    unittest.main()
