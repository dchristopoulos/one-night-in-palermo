import type { CSSProperties } from 'react';
import { isKiller, modelName, type SeatState } from './game.ts';
import { avatar, Face } from './Face.tsx';
import { Emblem } from './Emblem.tsx';
import css from './Seat.module.css';

// A seat says little, clearly (DESIGN.md §5): face, name, model; the role when the viewer knows it; out = grey face plus
// the turned card; speaker glow; addressed ring. One extra: the faces of everyone leaning on this seat (light while they
// talk, solid with a count at the vote). `row`: top seats put the portrait against the table edge below their label.
// `ballots`: false hides the voters' faces of a secret ballot (Guess mode), leaving the count.
export function Seat({ seat, showRole, leaners, row, ballots = true }: { seat: SeatState; showRole: boolean; leaners: string[]; row?: 'top' | 'bottom'; ballots?: boolean }) {
  const role = showRole || seat.revealed ? seat.role : null;
  const faces = seat.tally ? (seat.tally.secret && !ballots ? [] : seat.tally.voters) : leaners;
  return (
    <figure className={css.seat} data-row={row} data-ring={seat.ring ?? undefined} data-dead={seat.dead || undefined}
      data-killer={(role && isKiller(role)) || undefined} style={{ '--seat-color': `var(--seat-${seat.seat % 7})` } as CSSProperties}>
      <div className={css.head}>
        <div className={css.portrait}>
          <img decoding="sync" src={avatar(seat.name)} alt="" />
          {seat.claim && !seat.dead && <span className={css.mark} title={`says ${seat.claim}`}><Emblem role={seat.claim} /></span>}
        </div>
        {/* the pile hangs under the portrait, in a slot that is always there, so the face is never covered and nothing jumps */}
        <div className={css.slot}>
          {(faces.length > 0 || seat.tally) && (
            <span className={css.pile} data-vote={seat.tally ? true : undefined} title={`${faces.length} ${seat.tally ? 'votes' : 'leaning on ' + seat.name}`}>
              {faces.map((v, i) => <Face key={i} name={v} />)}
              {seat.tally && <b>{seat.tally.count}</b>}
            </span>
          )}
        </div>
      </div>
      <figcaption>
        <div className={css.name}>{seat.name}</div>
        <div className={css.meta}>{modelName(seat.model)}</div>
        <div className={css.tags}>
          {role && (seat.dead ? <span className={css.turned} data-role={role}><Emblem role={role} />{role}</span>
            : <span className={css.role} data-role={role}>{role}</span>)}
          {seat.dead && !role && <span className={css.down}>card face down</span>}
          {seat.claim && !seat.dead && <span className={css.claim}>says {seat.claim}</span>}
        </div>
      </figcaption>
    </figure>
  );
}
