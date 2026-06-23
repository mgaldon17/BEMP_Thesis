# CLAUDE.md

Guidance for working in this repository.

## What this repo is

The master's thesis **"Characterization of Neutron Response of Ionization
Chambers"** (Manuel Galdón, TUM · FRM II, 2024) plus its supporting code. It
holds three distinct things:

1. **Python MCNP toolkit** (`Python/`) — prepares, runs and analyses Monte Carlo
   neutron/gamma simulations (MCNP6) studying how an atmospheric corrosion layer
   (hydromagnesite) alters the response of PTW **TM33054** (Mg) and **TM33053**
   (A-150) ionization chambers. Includes a Twitter notification bot.
2. **The thesis** (`Master Thesis/`) — LaTeX source + compiled
   `BEMP_Thesis_of_Manuel_Galdon.pdf`. Auxiliary analysis in `MATLAB/`.
3. **Web landing** (`web/`) — a one-page WebGL site presenting the thesis.

## Layout

```
Python/MCNPSimulationScripts/simulation/
  MEDAPP_simulations/        # chamber w/ and w/o corrosion (MEDAPP source)
  strontium_simulations/     # Sr-90 source
  analysis/                  # output parsing -> result.txt
  notification_bot/          # tweepy "simulation finished" notifier
Master Thesis/               # LaTeX + thesis PDF
MATLAB/                      # auxiliary plotting
web/                         # Vite + React + three.js landing
.github/workflows/           # notification, deploy, unpublish, maintenance
```

## Python toolkit

- `pip install -r requirements.txt`. Running simulations needs an **MCNP6
  license** (LANL); the **analysis** stage runs without one.
- Simulations are launched from a `run.py` in each simulation dir; it builds the
  MCNP input, runs `mpiexec -np 96 mcnp6.mpi`, then triggers analysis.
- `analysis.py` parses tallies into value/error pairs (sweeping argon-gas
  density in the cavity) and writes `result.txt`.
- The notification bot reads Twitter/X credentials from `.env` (see
  `.env.example`); **never commit `.env`**. The bot is optional.

## Web landing (`web/`)

Stack: **Vite · React 18 · three.js** (`@react-three/fiber`, `@react-three/drei`,
`@react-three/postprocessing`) · **Lenis** smooth scroll · **Zustand** store.

```bash
cd web && npm install
npm run dev      # http://localhost:5173
npm run build    # -> web/dist
```

Key files:
- `src/scene/DecomposeParticles.jsx` — the core effect. Rasterises a subject
  (default `public/atom.jpg`, procedural fallback if missing), one particle per
  `PARTICLE_STEP` px, into a custom `ShaderMaterial`. Tunables are exported at
  the top (`PARTICLE_STEP`, `AMPLITUDE`, `FREQ`, `BLOOM_INTENSITY`, `SUBJECT`).
- `src/scene/shaders/` — `curlNoise.glsl` (divergence-free flow), `vertex.glsl`
  (staggered decompose), `fragment.glsl`. Imported with `?raw`.
- `src/store.js` — Lenis writes normalized scroll (0..1); the shader damps
  toward it in `useFrame`. **Rotation is driven only by scroll** so scrolling
  back to the top returns the atom to its exact original state (no idle drift).
- `src/sections/` — content sections. `src/StateScreen.jsx` + `maintenance.html`
  / `unpublish.html` are the frozen-atom Pages variants (multi-page Vite build).

### Content honesty rule (important)

All landing copy must come from **verified facts only** — the thesis PDF or the
repo source. **Do not invent** results, awards, figures, or names. Verify claims
against `Master Thesis/BEMP_Thesis_of_Manuel_Galdon.pdf` (use `pdftotext
-layout`) before writing them. Verified people: Dr. Tobias Chemnitz (FRM II
supervision), Prof. Dr. Peter Müller-Buschbaum (TUM supervisor), Dr. Lucas
Sommer (FRM II), Dr. Ralf Nolte (PTB calibration). The FRM II neutron beam
(MEDAPP) enables **Fast Neutron Therapy** (palliative treatment) — it was **not**
used for imaging. PTB is a calibration facility, not a "method".

## Deployment (GitHub Pages)

`web/vite.config.js` sets `base: '/<REPO_NAME>/'` in production — edit
`REPO_NAME` if the repo is renamed. Workflows build from `web/` and publish
`web/dist`. `deploy.yml` runs on push to `main`; `unpublish.yml` and
`maintenance.yml` are manual (the latter also has a weekly audit/link-check
cron). They pass `enablement: true` to auto-enable Pages on first run.

## Conventions

- Commit/push only when asked; branch off `main` first if needed.
- Build the landing (`npm run build`) after changing `web/` to confirm it
  compiles before finishing.
