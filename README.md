<div align="center">

# ☢️ Characterization of Neutron Response of Ionization Chambers

**Master's Thesis — Manuel Trigueros Galdón**
Technical University of Munich (TUM) · Department of Physics · FRM II

[![Read the Thesis](https://img.shields.io/badge/📄_Read_the_Thesis-PDF-red?style=for-the-badge)](Master%20Thesis/BEMP_Thesis_of_Manuel_Galdon.pdf)

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)
![MCNP6](https://img.shields.io/badge/MCNP6-Monte_Carlo-orange?style=flat-square)
![LaTeX](https://img.shields.io/badge/LaTeX-Thesis-008080?style=flat-square&logo=latex&logoColor=white)
![License](https://img.shields.io/badge/MCNP-License_Required-lightgrey?style=flat-square)

*A Python automation toolkit for running and analyzing Monte Carlo N-Particle (MCNP) simulations
that study how a corrosion layer alters the neutron and gamma response of dosimetry ionization chambers.*

</div>

---

## 📖 About

Magnesium ionization chambers used in fast-neutron therapy develop an atmospheric **corrosion layer**
(hydromagnesite) that changes their **sensitivity** to radiation, introducing uncertainty in dosimetric
measurements. This work combines neutron/X-ray CT imaging, MCNP Monte Carlo simulations and a PTB
calibration to characterize that effect on the PTW **TM33054** (magnesium) and **TM33053** (A-150 tissue
equivalent) chambers.

> 📄 **The full thesis is available here → [`BEMP_Thesis_of_Manuel_Galdon.pdf`](Master%20Thesis/BEMP_Thesis_of_Manuel_Galdon.pdf)**

## 📑 Table of Contents

- [Prerequisites](#-prerequisites)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Configuration (.env)](#-configuration-env)
- [Running the Simulations](#-running-the-simulations)
- [Notification Bot](#-notification-bot)
- [Understanding the Results](#-understanding-the-results)
- [The Thesis Document](#-the-thesis-document)
- [Contributing](#-contributing)

## ✅ Prerequisites

| Requirement | Notes |
|---|---|
| 🐍 **Python 3.x** | Install dependencies with `pip install -r requirements.txt` |
| ⚛️ **MCNP6 license** | MCNP is licensed software from Los Alamos National Laboratory. Running simulations requires a valid license — see the [official MCNP website](https://mcnp.lanl.gov/). |
| 📊 **Data files** | The nuclear data files needed for analysis are included in this repository, so the **analysis** stage can be run without an MCNP license. |

## 🗂️ Project Structure

```
BEMP_Thesis/
├── Master Thesis/                 # LaTeX source + compiled thesis PDF
│   └── BEMP_Thesis_of_Manuel_Galdon.pdf
├── Python/
│   └── MCNPSimulationScripts/
│       └── simulation/
│           ├── MEDAPP_simulations/      # Chamber w/ and w/o corrosion (MEDAPP source)
│           ├── strontium_simulations/   # Chamber irradiated by a Sr-90 source
│           ├── analysis/                # Output parsing & plotting
│           └── notification_bot/        # Twitter/X "simulation finished" notifier
├── MATLAB/                        # Auxiliary plotting/analysis
├── .env.example                  # Template for Twitter/X credentials
└── requirements.txt
```

## 🚀 Getting Started

```bash
# 1. Clone
git clone https://github.com/mgaldon17/BEMP_Thesis.git
cd BEMP_Thesis

# 2. (recommended) create a virtual environment
python -m venv .venv && source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

## 🔐 Configuration (.env)

The optional notification bot posts to Twitter/X when a simulation finishes. Credentials are read from a
**`.env` file** (never committed). To enable it:

```bash
cp .env.example .env
```

Then fill in your own Twitter/X API credentials in `.env`:

```dotenv
CONSUMER_KEY=your_consumer_key
CONSUMER_SECRET=your_consumer_secret
ACCESS_TOKEN=your_access_token
ACCESS_TOKEN_SECRET=your_access_token_secret
BEARER_TOKEN=your_bearer_token
```

> 🔒 `.env` is listed in `.gitignore`, so your secrets stay local. Get the keys/tokens from the
> [Twitter/X Developer Portal](https://developer.twitter.com/). The bot is fully optional — the
> simulations run without it.

## ▶️ Running the Simulations

Use the `run.py` script in the relevant simulation directory. It sets up the MCNP input, runs the
simulation and triggers the analysis. The input parameters can be customized:

| Parameter | Type | Description | Example |
|---|---|---|---|
| **Source** | List | The source input file | `["resources/MEDAPP_Source.txt"]` |
| **Materials** | List | The materials input files | `["/hydromagnesite/materials_0%_water + 100%_hydro.txt", ...]` |
| **Target Material** | String | Corrosion-layer material (use `"Mg"` for no layer) | `"hydromagnesite"` |
| **Number of Particles** | String | Number of particles to simulate | `"10E8"` |
| **Tallies** | String | The tallies input file | `"resources/tallies.txt"` |
| **Planes** | String | The planes input file | `"resources/planes_with_corrosion"` |
| **Mode** | String | The mode input file | `"resources/mode.txt"` |

The files in the `resources` folder reproduce the exact input used in the thesis, but the tool can run
MCNP for **any** geometry, source or material — just provide the input files and adjust `run.py`.

```bash
python run.py
```

## 🤖 Notification Bot

When a run finishes, the bot (`notification_bot/message_center.py`) sends a tweet such as
*"Simulation finished at HH:MM:SS"*. It loads credentials from `.env` via
[`python-dotenv`](https://pypi.org/project/python-dotenv/).

- ✅ Configure it by copying `.env.example` → `.env` (see [Configuration](#-configuration-env)).
- 🚫 To disable notifications, comment out the `MessageCenter(...).send_tweet()` call in your `run.py`.

## 📈 Understanding the Results

MCNP executions generate output files (e.g. the `.o` / `mctal` files in `resources/simulation_result`).
The toolkit runs multiple executions across a varying argon-gas density in the chamber cavity, then:

1. **`analysis.py`** (in `Python/MCNPSimulationScripts/simulation/analysis`) reads the output, processes the
   tallies and writes a `result.txt`.
2. For each tally it writes a value/error pair:
   `y_<tally>_<particle> = <value>` and `y_err_<tally>_<particle> = <error>`,
   followed by a **Simulation Details** section.
3. The resulting vectors are stored as plain text so you can plot them with the tool of your choice.

```bash
cd Python/MCNPSimulationScripts/simulation/analysis
python analysis_IC-33051.py
```

## 📚 The Thesis Document

The compiled thesis lives in the **`Master Thesis/`** directory:

📄 **[BEMP_Thesis_of_Manuel_Galdon.pdf](Master%20Thesis/BEMP_Thesis_of_Manuel_Galdon.pdf)**

To rebuild it from the LaTeX source:

```bash
cd "Master Thesis"
latexmk -pdf -shell-escape -jobname=BEMP_Thesis_of_Manuel_Galdon main.tex
```

> Requires a TeX distribution (e.g. TeX Live / TinyTeX) and Ghostscript for the EPS logo conversion.

## 🤝 Contributing

Contributions are welcome — feel free to open an issue or a pull request. Please update tests and
documentation as appropriate.

---

<div align="center">
<sub>Built for the Master's Thesis at the Heinz Maier-Leibnitz Zentrum (FRM II), TUM.</sub>
</div>
