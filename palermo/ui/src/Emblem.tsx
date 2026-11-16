import type { Role } from './game.ts';

// One flat emblem per role, drawn here (DESIGN.md §5: no stock icons, no emoji). Filled with currentColor on a 48 grid;
// the cut-outs (the badge star, the door) are holes, so the emblem works on any card colour.
const paths: Record<string, string> = {
  // a dagger, point up
  killer: 'M24 3 L29.5 30 H18.5 Z M11 30 H37 A2 2 0 0 1 37 35 H11 A2 2 0 0 1 11 30 Z M21 35 H27 V41 H21 Z M24 41 A3.5 3.5 0 1 1 24 48 A3.5 3.5 0 1 1 24 41 Z',
  // a shield with a five-point star cut out
  officer: 'M24 3 L41 9 V23 C41 34 33.5 41.5 24 45 C14.5 41.5 7 34 7 23 V9 Z M24 13 L26.6 20.4 L34.5 20.6 L28.2 25.3 L30.5 32.9 L24 28.4 L17.5 32.9 L19.8 25.3 L13.5 20.6 L21.4 20.4 Z',
  // a plain cross in a ring
  doctor: 'M24 3 A21 21 0 1 1 24 45 A21 21 0 1 1 24 3 Z M24 7 A17 17 0 1 0 24 41 A17 17 0 1 0 24 7 Z M20.5 12 H27.5 V20.5 H36 V27.5 H27.5 V36 H20.5 V27.5 H12 V20.5 H20.5 Z',
  // a town house with its door cut out
  citizen: 'M24 5 L43 21 V43 H5 V21 Z M20 30 A4 4 0 0 1 28 30 V43 H20 Z',
  // a key
  mayor: 'M15 6 A10 10 0 1 1 15 26 A10 10 0 1 1 15 6 Z M15 11 A5 5 0 1 0 15 21 A5 5 0 1 0 15 11 Z M24.8 13 H44 V19 H40 V25 H35 V19 H24.8 Z',
};
const alias: Record<string, string> = { accomplice: 'killer', police: 'officer' };

export function Emblem({ role, className }: { role: Role | string; className?: string }) {
  const d = paths[alias[role] ?? role] ?? paths.citizen;
  return <svg className={className} viewBox="0 0 48 48" aria-hidden><path d={d} fill="currentColor" fillRule="evenodd" /></svg>;
}
