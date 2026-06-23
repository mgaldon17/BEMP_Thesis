# Thesis landing — *Characterization of Neutron Response of Ionization Chambers*

A one-page WebGL landing for the master's thesis. A particle-built atom
**decomposes** along a curl-noise flow as you scroll and **reassembles** as you
scroll back up, with a subtle Cherenkov-blue bloom — the atom "emits radiation".

## Stack

Vite · React 18 · three.js (`@react-three/fiber`) · `@react-three/drei` ·
`@react-three/postprocessing` (Bloom) · Lenis (smooth scroll) · Zustand (scroll store).

## Develop

```bash
cd web
npm install
npm run dev      # http://localhost:5173
npm run build    # -> web/dist
npm run preview
```

## The decompose effect

`src/scene/DecomposeParticles.jsx` rasterises a subject (default
`public/atom.jpg`) onto an offscreen canvas, samples one particle per
`PARTICLE_STEP` px, and feeds positions/colours into a custom `ShaderMaterial`.
The vertex shader displaces each particle along a **curl-noise** field
(`src/scene/shaders/curlNoise.glsl`) with a staggered per-particle delay.
Lenis writes normalized scroll into the Zustand store; the shader damps toward
it in `useFrame`.

Tunables live at the top of `DecomposeParticles.jsx`:
`PARTICLE_STEP`, `AMPLITUDE`, `FREQ`, `BLOOM_INTENSITY`, `SUBJECT`.

> If `public/atom.jpg` is missing the component draws a procedural atom as a
> fallback, so the effect always works. Drop a real HD render at
> `public/atom.jpg` to override it.

## Images

- `public/atom.jpg` — the particle subject. Replaceable.
- `public/frmii.jpg` — *"View in the pool of FRM II"*, photo **© Bernhard
  Ludewig / TUM**, from
  [mep.tum.de](https://www.mep.tum.de/cnsi/projekte/conversion-of-frm-ii/),
  with visible credit in `src/sections/FrmII.jsx`. Swap it for a Wikimedia
  Commons / MLZ press-kit image if reuse rights are ever a concern.

## State pages (frozen atom)

The site is **multi-page** (`vite.config.js` → `index.html`,
`maintenance.html`, `unpublish.html`). The two extra pages reuse the *same*
`Scene` / `DecomposeParticles`: `src/main.jsx` reads `data-state` on `#root`
and renders `src/StateScreen.jsx`, which pins the decompose progress and shows
a centred message — no scroll, no sections.

- `maintenance.html` → atom frozen at **26%** decompose · "Under maintenance"
- `unpublish.html` → atom **fully decomposed (100%)** · "Unpublished page"

## Deployment (GitHub Pages, project page)

`vite.config.js` sets `base: '/<REPO_NAME>/'` in production. Edit `REPO_NAME`
there if the repository is renamed. Workflows live in `../.github/workflows/`:

- **deploy.yml** — builds `web/` and publishes `web/dist` on push to `main`.
- **unpublish.yml** — manual (type `OFFLINE` to confirm); builds and promotes
  `unpublish.html` to `index.html` so the URL shows the fully-decomposed atom.
- **maintenance.yml** — manual `on` (promotes `maintenance.html`) / `off`
  (re-deploys the normal build); weekly cron runs `npm audit` + a link-check
  and opens an issue on failure without touching production.

The workflows pass `enablement: true` to `actions/configure-pages`, so Pages is
auto-enabled on the first run. If that's blocked, enable it once under
**Settings → Pages → Source: GitHub Actions**.
