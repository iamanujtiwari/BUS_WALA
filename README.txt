# Barsaat Chai — Rainy Lake Music Player

A single HTML file: a music player styled like an old brass radio, sitting over a
rainy lakeside chai-stall photo. Vinyl disc spins while a track plays, live clock
top-left, playlist you scroll through.

![Preview](preview.jpg)

## File
- `rainy-chai-player.html` — the whole thing (HTML, CSS, JS, and the background
  photo) is bundled into one file. Nothing to install, no build step.

## How to open it
Just double-click it, or open from a terminal:
```
open rainy-chai-player.html      # macOS
start rainy-chai-player.html     # Windows
xdg-open rainy-chai-player.html  # Linux
```

## Live link
I can't deploy or host this myself from here, so I don't have a real URL to hand
you — but since it's a single static file, you can get one yourself in under a
minute:

- **[Netlify Drop](https://app.netlify.com/drop)** — drag `rainy-chai-player.html`
  onto the page, get a `https://...netlify.app` link instantly. No account needed.
- **GitHub Pages** — put the file in a repo as `index.html`, turn on Pages in
  Settings, live at `https://<username>.github.io/<repo>/`.
- **Vercel** — `vercel` CLI or drag-and-drop import, gives a `https://...vercel.app`
  link.

## What works
- Clock (top-left) — real time, 12-hour format with AM/PM, updates every second
- Player — spinning disc while playing, stops cleanly when paused
- Playlist — 50 song titles, scrollable
- Seek bar, previous/next, one combined play/pause button
- Rain animation over the photo
- Layout adjusts to smaller screens without things overlapping

## Features
- **Background** — your uploaded chai-stall/lake photo, embedded directly in the
  file (as base64), with rain streaks and a soft vignette over it
- **Clock** — glass pill, top-left, live 12-hour clock with AM/PM and date
- **Player** — elliptical brass bezel, circular vinyl disc that spins only while
  playing, needle arm that lifts/lowers with play state
- **Transport** — previous / play-pause / next, plus a seek bar showing current
  time and total duration
- **Playlist** — scrollable list of 50 song titles (no dates), each row shows a
  time value once a real track is loaded
- **Responsive** — clock and player panel no longer overlap; sizes scale down for
  narrow or short viewports; playlist and panel scroll instead of clipping

## What doesn't
No actual audio is attached — there were no song files to embed, and I can't fetch
copyrighted music. The playlist is a shell: titles are there, but nothing plays
until real audio files are wired in.
