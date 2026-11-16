import type { Score } from './evenings.ts';
import { Face } from './Face.tsx';
import css from './Scoreboard.module.css';

// The evening so far (DESIGN.md §5): town wins against killer wins, large; then each player: games won, times a killer.
// The caller decides how far "so far" goes (scoreboard(evening, upTo)), so a later game's result never shows.
export function Scoreboard({ score, title = 'The evening so far' }: { score: Score; title?: string }) {
  if (!score.played) return <section className={css.board}><h3>{title}</h3><p className={css.none}>No game finished yet.</p></section>;
  return (
    <section className={css.board} aria-label={title}>
      <h3>{title}</h3>
      <p className={css.sides}>
        <span data-side="town"><b>{score.town}</b> town</span>
        <span className={css.dash} aria-hidden>–</span>
        <span data-side="killer"><b>{score.killer}</b> killers</span>
        {score.other > 0 && <small> · {score.other} other</small>}
      </p>
      <table>
        <thead><tr><th scope="col">Player</th><th scope="col">Won</th><th scope="col">Killer</th></tr></thead>
        <tbody>
          {score.players.map(p => (
            <tr key={p.name}>
              <th scope="row"><Face name={p.name} /> {p.name}</th>
              <td><b>{p.won}</b> of {p.played}</td>
              <td>{p.killer ? `${p.killer}×` : '–'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
