# The Rack

A 5-day strength split as a swipeable, installable training app. Browse the full catalog of 1,324 exercises (grouped by muscle), build your own workout per section, train from a swipeable card deck with live animations, and track your streak and weekly progress.

Built as a single static PWA — no backend, no build step. All exercise data is bundled into `index.html`, so it loads instantly and works offline. Exercise images/animations stream from the jsDelivr CDN and are cached for offline use after first view.

## Files (keep them all in the repo root, flat)

```
index.html        the entire app + bundled exercise data
manifest.json     PWA manifest (name, icons, theme)
sw.js             service worker (offline caching)
vercel.json       headers (service worker + caching)
icon-192.png      app icons
icon-512.png
icon-180.png      apple touch icon
```

All paths inside the app are relative (`./sw.js`, `./manifest.json`, …), so every file must sit next to `index.html`.

## Deploy (GitHub → Vercel)

1. Push all files to the repo root.
2. In Vercel: **New Project → import this repo**. Framework preset: **Other**. No build command, output directory `./`. It's pure static.
3. Deploy. You'll get a `the-rack.vercel.app` URL.
4. On your phone (Safari): open the URL → Share → **Add to Home Screen**. Install + offline activate here (the service worker needs the https URL; it won't run from a local file).

## Updating it later

The service worker caches the app shell, so after a redeploy you must **bump the cache version** or installed devices may keep serving the old build:

In `sw.js`, change:
```js
const SHELL='rack-shell-v1';   // -> 'rack-shell-v2'
const MEDIA='rack-media-v1';   // bump only if you change image sources
```
Commit + push. On next visit the new worker installs and clears the old cache.

## How it works

- **Home** — the five sections + a streak/progress card.
- **Section → Catalog tab** — every relevant exercise, grouped by sub-muscle. Tap ＋ to add to your workout. A "This section / All exercises" toggle lets you pull from the whole library.
- **My Workout tab** — your picks as a swipeable deck. Mark Doing / Done in any order, edit sets×reps, remove. Only the cards near you are mounted (virtualized), and the centered card plays its animation.
- **Progress** — streak, weekly chart, totals, per-section breakdown. Every "Done" is logged to `localStorage`.

Your workout, sets/reps, daily progress, and history are all stored on-device. Nothing leaves your phone.

## Data & credits

Exercise dataset (names, muscles, instructions, images, animations) from
[hasaneyldrm/exercises-dataset](https://github.com/hasaneyldrm/exercises-dataset), served via jsDelivr.

## Tech notes

- No framework, no bundler — one HTML file with inline CSS/JS.
- Design: light "liquid glass" UI, aurora background, per-section accent colors.
- Fonts: Bricolage Grotesque, Inter, JetBrains Mono (Google Fonts).
- Offline: service worker (cache-first shell + runtime image cache).
