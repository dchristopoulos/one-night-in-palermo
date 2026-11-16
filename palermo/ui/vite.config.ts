import { defineConfig, type Plugin } from 'vite';

// Built into ui/dist with page-relative URLs (base './'): view.py serves it at /ui/ (and maps /ui/games/, /ui/avatars/
// to the folders at the root), `view.py --export DIR` copies it into a static site that works from any folder of any
// host. Data and images are asked for relative to the page: games/…, avatars/…, never /games/….
//
// relativeUrls: a guard. The build fails if a source file asks for data or images from the server root.
function relativeUrls(): Plugin {
  const left = /(['"`])\/(games|avatars|art)\/|=> '\/' \+ /;
  return {
    name: 'palermo-relative-urls',
    enforce: 'pre',
    transform(code, id) {
      if (!/\/src\/[^/]+\.tsx?$/.test(id) || /\.test\.ts$/.test(id)) return null;
      if (left.test(code)) this.error(`${id}: a root-absolute URL is left; use a page-relative one (games/…, avatars/…)`);
      return null;
    },
  };
}

export default defineConfig({ base: './', plugins: [relativeUrls()] });
