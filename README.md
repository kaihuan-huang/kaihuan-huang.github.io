# kaihuan-huang.github.io

**Live:** https://kaihuan-huang.github.io/

Personal portfolio: six live demos shown as measured works, three case studies of production and private work, a web résumé, and notes. English / 中文, light and dark.

## Edit and build

All copy and every metric live in `content/site.json`; each metric names its source. Rebuild with:

```sh
python3 build.py   # writes index.html, resume.html and works/*.html (standard library only)
```

Hand-written files: `assets/css/folio.css`, `assets/js/folio.js`, `assets/img/plate.svg` (the FIG. 01 drawing), `404.html`, `notes/`.

To use a portrait, add `assets/img/portrait.jpg` (4:5). It replaces the drawn FIG. 01 plate on the homepage automatically.
