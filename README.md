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
