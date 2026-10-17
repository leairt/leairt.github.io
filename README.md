# Lea Irt — personal portfolio

A static, seven-page portfolio built with HTML and CSS. No npm dependencies or framework are required.

## Preview

```sh
python3 server.py --port 8765
```

Open http://127.0.0.1:8765. The server builds the site first and serves only `dist/client`. After editing a source file, run `python3 scripts/build.py` and refresh the browser; the running server picks up the new output.

## Source layout

- `index.html` — introduction, education, skills, experience, hobbies and contact.
- `projects/index.html` — the thesis, Slavuj, Artist Classification, the CLP thesis, BoMGerman and upcoming work.
- `projects/3d-reconstruction/index.html` — a technical case study covering the problem, dataset, architecture, training, evaluation, limitations and source documents, with section navigation.
- `projects/slavuj/index.html` — the music discovery application, six playable demos and implementation overview.
- `styles/slavuj.css` — the Slavuj header, demo cards and implementation summary.
- `styles/base.css` — shared typography, colours, navigation and contact.
- `styles/home.css` — homepage layout and responsive rules.
- `styles/projects.css` — project pages and responsive research figures.
- `assets/` — the original logo, portraits, organisation logos and hobby images, plus local fonts, research figures, the finished stop-motion animation and the two research PDFs. Replace `assets/art.jpeg` to update the art photograph, then rebuild.
- `.openai/hosting.json` — retained Site identity and static deployment directory.

## Build and validate

```sh
python3 scripts/build.py          # Validate and build dist/client
python3 scripts/build.py --check  # Check references and anchors without rebuilding
python3 scripts/build.py --list   # List every required website file
```

The build follows local HTML and CSS references from the seven pages. Missing files, duplicate HTML IDs and broken page anchors fail the build. Unreferenced assets and development files are never copied to `dist/client`.

## Adding projects

Add another `<a class="project-card">` inside `.project-grid` in `projects/index.html`, before the non-clickable upcoming card. Include a preview image, full title, project type and year. A small corner arrow signals that the card is a link. A short description appears over the darkened image on hover or keyboard focus. Touch devices keep the image and corner arrow visible. The entire card is a single keyboard-accessible link. Give each title a unique ID and reference it in the card’s `aria-labelledby` attribute. Cards stack on smaller screens.

## Research figures

The project page shows recorded RGB reconstructions from thesis Figure 23 and predicted normal/depth maps from the original research, alongside the training models and geometry preparation. The renders are cropped to remove unused margins and slide borders, with input/output pairs kept at matching scale. These are static results, not live model inference.

The website summarises the research in English; the linked thesis and presentation are the original Serbian documents. The homepage animation is the existing 12-frame boomerang WebP; its subjects are unchanged.

## Slavuj demos

`assets/slavuj/` contains six silent H.264 MP4 recordings and WebP posters. The videos play at twice the original speed with audio tracks removed, with browser chrome cropped out and frames resized to 1600 × 850. MP4 metadata is placed at the beginning for streaming. Native controls support playback, seeking and fullscreen; `preload="none"` prevents downloading the videos until requested. The local preview server supports byte-range requests for seeking without downloading the entire recording.

The description follows the supplied project brief, recorded demonstrations and implementation documentation. It identifies the work as a team project.

## Additional project case studies

`projects/artist-classification/` and `projects/bomgerman/` present the original GitHub projects. Shared case-study styles are in `styles/case-studies.css`. Original art is composed with inline SVG viewports, preserving the source images.

Artist Classification results follow the Serbian report at commit `55a9310e57d359fbc52b50efecb83b52eae5e538`. Training curves, test accuracy (82.5%), the test confusion matrix and prediction examples come from Figures 17, 21 and 22. Augmentation examples come from Figure 15. The decorative artwork gallery retains the original dataset images. Notebook-specific split sizes, hyperparameters and metrics are not used in the case study. Source: https://github.com/leairt/Artist-Classification-Using-Convolutional-Neural-Network

BoMGerman character sheets and gameplay come from commit `e37a7e4b23af67584559e125a0e56ff44f1062e3`. The gameplay MP4 is remuxed for streaming without re-encoding. Source: https://github.com/leairt/BoMGerman

The 2022 CLP thesis is presented at `projects/clp/`. Its text and original magic hexagon figure come from the Serbian thesis in https://github.com/leairt/Using-CLP-in-Third-Generation-Programming-Languages (commit `17c8e579dfbb78e4508e86300112436a1923263a`).

Slavuj’s documentation summary is based on the project specification, SSU documents and database specification supplied with the project. CLP content follows the graduation thesis chapters 2–8, rather than repository code or README claims.

Project pages share keyword labels and SR markers for Serbian documents. CLP includes original puzzle images from slides 3–5, a local thesis PDF and the original presentation as PPTX. The CLP presentation also has a PDF export and 18 local slide previews. The original PPTX is retained as an editable source.

## Document previews and mobile layout

`styles/document-preview.css` and `assets/document-preview.js` implement compact local document previews. Papers scroll inside their cards; presentations use buttons, keyboard arrows and swipe navigation. Previews use WebP files in `assets/document-previews/`; links open the complete PDF. Reduced-motion preferences disable page transitions.

Mobile rules keep navigation and controls touch-friendly, wrap contact links, stack project sections and show project summaries without hover. The original CLP PPTX is a source asset for future slide exports, even though it is not copied to the published site.
