# Lea Irt — personal portfolio

Personalized from the original Framer reference at https://mazurbartek.com/.
Profile source: https://www.linkedin.com/in/lea-irt-5a658329a/ (accessed 2026-09-17).

Run `python3 server.py` and open http://localhost:8000. Use HTTP, not `file://`, because the original site uses ES modules.

## Personal content

- `content/profile.json` contains the profile, verified education, LinkedIn destination and five selected projects.
- `scripts/personalize.py` updates both original HTML and compiled Framer text so hydration preserves the personal content.
- `profile.css` and `profile.js` replace reference photography/mockups with typographic covers, substitute graduation-year labels, route project links and disable the original form.
- `scripts/build-profile-pages.py` generates project listings and detail pages from the profile. Original project URLs remain usable.
- `scripts/localize.py` regenerates pages, then reapplies personalization.
- `python3 scripts/build.py` creates the deployment output.

Original hero canvas, pointer effects and motion components remain in `assets/modules/`. Personal project covers are abstract title cards, not screenshots. No profile photo, e-mail address, CV or GitHub URL was supplied; LinkedIn is the contact destination. No form submits to the reference author.

`reference/` contains untouched historical snapshots for regeneration, not pages served as the portfolio. The old downloaded media remain for the preserved animation runtime but are not presented as Lea's photos or projects. The in-app browser was unavailable during the initial setup; visual and pointer interaction parity has not been verified.
