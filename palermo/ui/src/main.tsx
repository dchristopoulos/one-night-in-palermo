import { createRoot } from 'react-dom/client';
import './tokens.css';
import { App } from './App.tsx';

// ?at=N holds a still (App keeps data-still in step with the URL): no motion, so a screenshot shows the settled frame
if (new URLSearchParams(location.search).has('at')) document.documentElement.dataset.still = '';
// a seat can carry any name (anyone can seat their own models), so a portrait may not exist: a plain figure stands in
const NOBODY = 'data:image/svg+xml,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96"><rect width="96" height="96" fill="#F1E7D0"/><circle cx="48" cy="38" r="17" fill="#565B78"/><path d="M14 96c2-22 16-33 34-33s32 11 34 33z" fill="#565B78"/></svg>');
addEventListener('error', e => {
  const img = e.target;
  if (img instanceof HTMLImageElement && /\bavatars\b/.test(img.src) && img.src !== NOBODY) img.src = NOBODY;
}, true);
createRoot(document.getElementById('root')!).render(<App />);
