# One Night in Palermo, the short
A 62 s vertical video (1080×1920, 30 fps) about game `palermo/games/fun9-4.json`, made with HyperFrames (HTML + GSAP).
`index.html` places the scenes in `compositions/`; every colour and font sits in `assets/palermo.css`.
Re-render (in this folder, after `npm install`):
`HYPERFRAMES_NO_TELEMETRY=1 npx hyperframes render --quality delivery --fps 30 -o out/render-raw.mp4`
then `ffmpeg -i out/render-raw.mp4 -c copy -movflags +faststart out/palermo-short.mp4`.
`python3 scripts/quotes.py` fills and checks every quote against the game file (verbatim).
`node scripts/screenshot.mjs` re-captures the end-card viewer still (viewer served at localhost:8766);
`node scripts/readme-shots.mjs` re-captures the two README screenshots in `palermo/docs/`.
Output: `out/palermo-short.mp4`, `out/poster.jpg`, `out/sheet.jpg`, `out/frames/s01..s13.jpg`.
