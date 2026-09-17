# Portfolio reference replica

Local reproduction of https://mazurbartek.com/ using its publicly served HTML, Framer runtime, fonts, media, canvas effects and motion settings. The original names, project content and contact destinations are intentionally retained to match the requested reference.

Run `python3 server.py`, then visit http://localhost:8000. Use an HTTP server, not `file://`, because the site uses ES modules. Root and nine subpages are included.

- `index.html`: original layout and responsive styles, localized resource URLs.
- `assets/modules/`: original compiled Framer components, motion and canvas code.
- `assets/media/`: downloaded images, fonts and video.
- `reference/`: downloaded HTML snapshots.
- `scripts/localize.py`: regenerates local pages from snapshots.
- `assets/manifest.json`: upstream-to-local resource mapping.

The original standalone analytics tag and editor bootstrap are removed; pages are marked noindex. Some third-party links and framework services may still require internet. Contact links still belong to the reference author. The in-app browser was unavailable, so visual parity and runtime interactions have not been verified in a browser.
