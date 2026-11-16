#!/usr/bin/env python3
"""Serve the viewer and saved games without importing game.py (so it works while the engine is being edited).

  python3 view.py [port]   then open http://localhost:8766/ui/   (the home screen lists every saved game)
  python3 view.py --export DIR [--tags r7a,sun15] [--best N]   a static copy of the viewer and some games (below)

Also serves /games/index.json: one summary per game in games/*.json (not games/lab/ or games/archive/), built on
request and cached by mtime; a game with games/fun/<name>.json carries `fun: {score, why, quote?}`. game.py --serve uses
the same handler (it imports `Quiet` from here).

The viewer uses page-relative URLs (games/…, avatars/…, fonts/…), so the same build works at /ui/ here (translate_path
maps /ui/games/ and /ui/avatars/ to the folders at the root) and from any folder of a static host (--export).
"""
import functools
import http.server
import json
import os
import pathlib
import re
import shutil
import sys
import threading
import time

HERE = pathlib.Path(__file__).resolve().parent
LIVE_SECONDS = 120          # a game with no `end` that was written to this recently is being played right now
STAMP = re.compile(r"^\d{8}-\d{6}$")                 # an old single game: 20261027-044948
MEMBER = re.compile(r"^(?P<tag>.+?)-(?P<n>\d{1,3})$")  # a game of an evening: run81-3, fin71-1, bake-A-2
SKIP = re.compile(r"^(ui-fixture|latest$)")          # hand-made viewer fixtures; latest.json duplicates a real file
KILLER_SIDE = {"killer", "accomplice"}

FUN_SKIP = {"last words", "before the game", "confession"}   # say lines that are not table talk (with `out` and ghosts)

_cache: dict = {}            # path -> (mtime_ns, size, summary or None)
_fun_cache: dict = {}        # fun path -> ((fun mtime_ns, size, game mtime_ns), fun or None)
_lock = threading.Lock()


def tag_of(name):
    """(tag, number) for a game of an evening, (None, None) for a single game."""
    if STAMP.match(name):
        return None, None
    m = MEMBER.match(name)
    return (m["tag"], int(m["n"])) if m else (None, None)


def summarize(events, name, mtime):
    """One game's line in the index, or None when it is not a game (dry, no cast). An unfinished game gets
    "finished": False; games_index decides from the clock whether it is live or abandoned."""
    if not isinstance(events, list) or not events or not isinstance(events[0], dict) or events[0].get("type") != "cast":
        return None
    cast = events[0]
    if cast.get("dry") or name.endswith("-dry"):
        return None
    end = next((e for e in reversed(events) if e.get("type") == "end"), None)
    players = [{"name": p["name"], "model": p.get("model", ""), "role": p.get("role", "")} for p in cast.get("players", [])]
    seconds = max((e.get("t") or 0) for e in events)
    tag, n = tag_of(name)
    return {
        "file": f"games/{name}.json", "name": name, "tag": tag, "n": n,
        "started": round(mtime - seconds),                # the first event's wall time (t counts from it)
        "mtime": round(mtime),
        "seats": len(players), "cast": players,
        "killers": [p["name"] for p in players if p["role"] in KILLER_SIDE],
        "winner": end.get("winner") if end else None,
        "days": sum(1 for e in events if e.get("type") == "phase" and e.get("kind") == "day"),
        "minutes": round(seconds / 60, 1),
        "finished": end is not None,
    }


def table_line(events, at):
    """{name, text} when events[at] is a line of table talk: a living player's `say` during the game (not last words,
    not the line before the game, not the confessions after it, not a ghost line). Otherwise None."""
    if not isinstance(at, int) or isinstance(at, bool) or not 0 <= at < len(events):
        return None
    e = events[at]
    if not isinstance(e, dict) or e.get("type") != "say" or e.get("out") or (e.get("why") or "") in FUN_SKIP:
        return None
    if not isinstance(e.get("text"), str) or not e["text"].strip() or not e.get("name"):
        return None
    if any(isinstance(x, dict) and x.get("type") in ("end", "recap") for x in events[:at]):
        return None
    return {"name": e["name"], "text": e["text"]}


def fun_of(game_path, fun_path):
    """The index's `fun` for one game from games/fun/<name>.json (funmeter.py): {score, why} plus `quote`, the first of
    the file's moments that points at a line of table talk in the game itself (the player's own words). None when there is
    no fun file or it has no numeric score. Cached by both files' mtimes; call with _lock held."""
    try:
        fst, gst = fun_path.stat(), game_path.stat()
    except OSError:
        return None
    key = (fst.st_mtime_ns, fst.st_size, gst.st_mtime_ns)
    hit = _fun_cache.get(str(fun_path))
    if hit and hit[0] == key:
        return hit[1]
    fun = None
    try:
        data = json.loads(fun_path.read_text())
        score = data.get("score") if isinstance(data, dict) else None
        if isinstance(score, (int, float)) and not isinstance(score, bool):
            fun = {"score": score, "why": str(data.get("why") or "")}
            moments = data.get("moments") if isinstance(data.get("moments"), list) else []
            events = json.loads(game_path.read_text()) if moments else []
            for m in moments:
                quote = table_line(events, m.get("at")) if isinstance(m, dict) else None
                if quote:
                    fun["quote"] = quote
                    break
    except (OSError, ValueError):
        fun = hit[1] if hit else None                   # caught mid-write: keep what we had
    _fun_cache[str(fun_path)] = (key, fun)
    return fun


def games_index(folder=None, now=None):
    """Every listable game in folder (default games/), newest first. Cached by (mtime, size); a file caught mid-write
    keeps its previous summary."""
    folder = pathlib.Path(folder or HERE / "games")
    now = time.time() if now is None else now
    games = []
    with _lock:
        for path in folder.glob("*.json"):
            name = path.stem
            if SKIP.match(name):
                continue
            try:
                st = path.stat()
            except OSError:
                continue
            key = str(path)
            hit = _cache.get(key)
            if hit and hit[0] == st.st_mtime_ns and hit[1] == st.st_size:
                summary = hit[2]
            else:
                try:
                    summary = summarize(json.loads(path.read_text()), name, st.st_mtime)
                except (OSError, ValueError):
                    summary = hit[2] if hit else None    # caught mid-write: keep what we had
                _cache[key] = (st.st_mtime_ns, st.st_size, summary)
            if not summary:
                continue
            live = not summary["finished"] and now - st.st_mtime < LIVE_SECONDS
            if not summary["finished"] and not live:
                continue                                  # unfinished and nobody is writing it any more
            fun = fun_of(path, folder / "fun" / path.name)
            games.append({**summary, "live": live, **({"fun": fun} if fun else {})})
    games.sort(key=lambda g: (g["started"], g["n"] or 0), reverse=True)
    return {"generated": round(now), "games": games}


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        if self.path.split("?")[0] in ("/games/index.json", "/ui/games/index.json"):
            body = json.dumps(games_index(pathlib.Path(self.directory) / "games")).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def translate_path(self, path):
        """/ui/… is the built React app (ui/dist); anything that is not a file there gets its index.html. The app asks for
        games and avatars relative to its page, so /ui/games/… and /ui/avatars/… (and /ui/art/…) are the root folders."""
        if re.match(r"/ui/(games|avatars|art)/", path):
            return super().translate_path(path[3:])
        if not re.match(r"/ui(/|\?|$)", path):
            return super().translate_path(path)
        fs = super().translate_path("/ui/dist" + path[3:])
        return fs if os.path.exists(fs) else str(pathlib.Path(self.directory) / "ui" / "dist" / "index.html")


def evenings_newest_first(games):
    """[(tag, [games])] for the finished games of evenings, the evening written to last first."""
    by = {}
    for g in games:
        if g["tag"] and g["finished"]:
            by.setdefault(g["tag"], []).append(g)
    return sorted(by.items(), key=lambda kv: max(g["mtime"] for g in kv[1]), reverse=True)


def pick(games, tags=None, best=None):
    """The games an export carries: those of `tags` (all evenings when None), then `best` N of them by fun score when
    games/fun/ scored any (otherwise the newest evening among them). Default: the two newest evenings."""
    games = [g for g in games if g["finished"] and g["winner"] != "stopped"]
    if tags:
        games = [g for g in games if g["tag"] in tags]
    if best:
        scored = sorted((g for g in games if g.get("fun")), key=lambda g: (-g["fun"]["score"], -g["started"]))
        if scored:
            return scored[:best]
        evenings = evenings_newest_first(games)
        return evenings[0][1] if evenings else []
    if tags:
        return games
    return [g for _, gs in evenings_newest_first(games)[:2] for g in gs]


def export(dest, tags=None, best=None, folder=None, dist=None):
    """Write a static site to dest: the built viewer (ui/dist, built with base './'), the avatars, the chosen games and a
    prebuilt games/index.json marked `static` (no live games, the viewer stops polling). Works from any folder of any
    static host. Returns the list of exported game names."""
    folder = pathlib.Path(folder or HERE / "games")
    dist = pathlib.Path(dist or HERE / "ui" / "dist")
    page = dist / "index.html"
    if not page.exists():
        raise SystemExit(f"no built viewer at {dist}: run `npm run build` in ui/ first")
    if re.search(r'(src|href)="/(?!/)', page.read_text()):
        raise SystemExit(f"{page} uses root-absolute URLs: rebuild it (`npm run build` in ui/, vite base './')")
    newest_src = max((p.stat().st_mtime for p in (HERE / "ui" / "src").rglob("*") if p.is_file()), default=0)
    if newest_src > page.stat().st_mtime:
        print("warning: ui/src changed after the last build; run `npm run build` in ui/ for the newest viewer", file=sys.stderr)
    chosen = pick(games_index(folder)["games"], tags=tags, best=best)
    if not chosen:
        raise SystemExit("no finished games match: nothing exported")
    dest = pathlib.Path(dest).resolve()
    if dest == HERE or dest in HERE.parents or dest.parent == HERE:
        raise SystemExit(f"{dest}: export to a folder of its own (not palermo/ itself, a parent, or a folder in palermo/)")
    if dest.exists() and any(dest.iterdir()) and not (dest / "games" / "index.json").exists():
        raise SystemExit(f"{dest} is not empty and not an earlier export: choose an empty folder")
    shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(dist, dest)
    shutil.copytree(HERE / "avatars", dest / "avatars", ignore=shutil.ignore_patterns(".*"))
    (dest / "games").mkdir()
    for g in chosen:
        shutil.copy2(folder / f"{g['name']}.json", dest / "games" / f"{g['name']}.json")
    games = sorted(({**g, "live": False} for g in chosen), key=lambda g: (g["started"], g["n"] or 0), reverse=True)
    index = {"generated": round(time.time()), "static": True, "games": games}
    (dest / "games" / "index.json").write_text(json.dumps(index, ensure_ascii=False))
    (dest / ".nojekyll").write_text("")                  # GitHub Pages: serve the folder as it is
    return [g["name"] for g in games]


def main(argv):
    if argv and argv[0] == "--export":
        args, opts = argv[1:], {}
        if not args or args[0].startswith("--"):
            raise SystemExit("usage: python3 view.py --export DIR [--tags r7a,sun15] [--best N]")
        dest, rest = args[0], args[1:]
        while rest:
            flag = rest.pop(0)
            if flag not in ("--tags", "--best") or not rest:
                raise SystemExit(f"unknown or incomplete option {flag!r}; usage: python3 view.py --export DIR [--tags a,b] [--best N]")
            opts[flag] = rest.pop(0)
        tags = [t for t in opts.get("--tags", "").split(",") if t] or None
        best = int(opts["--best"]) if "--best" in opts else None
        names = export(dest, tags=tags, best=best)
        size = sum(p.stat().st_size for p in pathlib.Path(dest).rglob("*") if p.is_file())
        print(f"exported {len(names)} games to {pathlib.Path(dest).resolve()} ({size / 1e6:.1f} MB): {', '.join(names)}")
        return
    port = int(argv[0]) if argv else 8766
    print(f"Viewer: http://localhost:{port}/ui/", flush=True)
    http.server.ThreadingHTTPServer(("127.0.0.1", port), handler()).serve_forever()


def handler(directory=HERE):
    return functools.partial(Quiet, directory=str(directory))


if __name__ == "__main__":
    main(sys.argv[1:])
