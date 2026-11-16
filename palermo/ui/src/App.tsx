import { useEffect, useMemo, useState } from 'react';
import { groupIndex, placeOf, type GameInfo } from './evenings.ts';
import { Home } from './Home.tsx';
import { Table } from './Table.tsx';

// Two screens and the browser's own history (DESIGN.md §7): the page itself is Home, ?file=games/x.json a game. Every URL is
// relative to the page (games/…, avatars/…), so the same build runs at /ui/ (view.py) and in any folder of a static host.
// ?at=N (a still) · ?mode=guess · ?debug=1 · ?live=1 (follow a file the index does not list) ride along on a game URL.
export interface Route { file: string | null; at: number | null; mode: 'watch' | 'guess'; debug: boolean; live: boolean }
const parse = (): Route => {
  const q = new URLSearchParams(location.search);
  return { file: q.get('file'), at: q.has('at') ? Number(q.get('at')) : null, mode: q.get('mode') === 'guess' ? 'guess' : 'watch', debug: q.has('debug'), live: q.has('live') };
};

// games/index.json, polled every 5 s (it is cached on the server; a live game and the next game of an evening show up).
// A static export (view.py --export) marks its index `static`: nothing new will appear, so it is read once.
function useIndex() {
  const [games, setGames] = useState<GameInfo[] | null>(null), [failed, setFailed] = useState(false);
  useEffect(() => {
    let alive = true, t: ReturnType<typeof setInterval> | undefined;
    const load = async () => {
      try {
        const r = await fetch('games/index.json', { cache: 'no-store' });
        if (!r.ok) throw new Error(String(r.status));
        const d = await r.json();
        if (alive) { setGames(d.games); setFailed(false); }
        if (d.static) clearInterval(t);
      } catch { if (alive) setFailed(true); }
    };
    load();
    t = setInterval(load, 5000);
    return () => { alive = false; clearInterval(t); };
  }, []);
  return { index: useMemo(() => (games ? groupIndex(games) : null), [games]), failed };
}

export function App() {
  const [route, setRoute] = useState(parse);
  const { index, failed } = useIndex();
  useEffect(() => {
    const back = () => setRoute(parse());
    addEventListener('popstate', back);
    return () => removeEventListener('popstate', back);
  }, []);
  useEffect(() => { document.documentElement.toggleAttribute('data-still', route.at != null); }, [route.at]);

  const open = (file: string | null) => {   // a new history entry: the back button returns to where you were
    history.pushState(null, '', file ? `?file=${file}` : location.pathname);
    setRoute(parse());
    scrollTo(0, 0);
  };
  if (!route.file) return <Home index={index} failed={failed} onOpen={open} />;
  const place = index ? placeOf(index, route.file) : null;
  return <Table key={route.file} route={route} live={route.live || !!place?.game?.live} place={place} onOpen={open} />;
}
