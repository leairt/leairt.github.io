# Lea Irt — personal portfolio

Run `python3 server.py` and open http://localhost:8000.

- `index.html`: full home page, education, experience, skills, awards, interests, community and contact.
- `projects/index.html`: six complete project cards with gallery areas.
- `portfolio.css`: shared responsive layout and colors.
- `portfolio.js`: pixel interference animation adapted from the original canvas, with reduced-motion support. No custom cursor.
- `scripts/redesign.py`: generates the redesigned pages and retired-route redirects. Edit this generator when changing page content and run it again.
- `python3 scripts/build.py`: builds static assets and the Worker entrypoint.

School polaroids use typographic artwork. Project covers are abstract title cards, not screenshots; gallery areas are explicitly marked as awaiting images. Add real supplied images there when available. Historical Framer reference files and personalization scripts are retained for reference; do not run `localize.py` or `build-profile-pages.py` on the redesign.
