# A-one Caterers & Events — website

Static five-page site (Home, About, Services, Gallery, Contact) for A-one Caterers & Events, Kothamangalam. Plain HTML, CSS and JavaScript, hosted on GitHub Pages.

## Structure
- `*.html` — the live pages
- `assets/css/style.css`, `assets/js/main.js` — styles and interactions
- `assets/img/` — logo, favicon and event photos (`assets/img/events/`)
- `source/` — page templates (`build.py`) used to regenerate the HTML

## Editing
Small text changes can be made directly in the HTML files. To regenerate all pages from the templates:

```
cd source && python3 build.py   # writes dist/ — copy its contents to the repo root
```

Contact form sends enquiries to WhatsApp (+91 95445 41075); no server needed.

Built by Codescape Innovations.

## Instagram reels (Home page)
1. Download the latest reels from @aone_caterers_ (Instagram app → reel → ⋯ → Download, or ask the client for the original videos).
2. Save them as `assets/video/reel-1.mp4` … `reel-4.mp4` (newest first). Keep each under ~8 MB.
3. Paste each reel's link into `REELS` in `source/build.py` and rebuild, or edit the `href` in `index.html`.

Videos autoplay muted when scrolled into view, pause when scrolled away, and have a tap-to-unmute button. Until a video is added, its card shows a photo and opens Instagram.
