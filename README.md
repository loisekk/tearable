<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:0a3d4a,100:00c896&height=200&section=header&text=Cloth%20Simulation&fontSize=60&fontColor=ffffff&fontAlignY=38&desc=Real-Time%20Pygame%20Physics%20Engine&descAlignY=58&descColor=cccccc" width="100%"/>

<br/>

![Python](https://img.shields.io/badge/PYTHON-3776AB?style=flat-square&logo=python&logoColor=white)
![Python Version](https://img.shields.io/badge/3.7+-blue?style=flat-square)
![Pygame](https://img.shields.io/badge/PYGAME-2.1+-green?style=flat-square)
![Physics](https://img.shields.io/badge/VERLET_INTEGRATION-orange?style=flat-square)
![License](https://img.shields.io/badge/LICENSE-MIT-purple?style=flat-square)
![Status](https://img.shields.io/badge/STATUS-ACTIVE-brightgreen?style=flat-square)

<br/>

<pre align="center">
░█████╗░██╗░░░░░░█████╗░████████╗██╗░░██╗
██╔══██╗██║░░░░░██╔══██╗╚══██╔══╝██║░░██║
██║░░╚═╝██║░░░░░██║░░██║░░░██║░░░███████║
██║░░██╗██║░░░░░██║░░██║░░░██║░░░██╔══██║
╚█████╔╝███████╗╚█████╔╝░░░██║░░░██║░░██║
░╚════╝░╚══════╝░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝
</pre>

<p align="center"><em>Three forces. One fabric. Infinite tears.</em><br/>
Production-grade cloth simulation with Verlet integration, real-time tearing, wind dynamics, and tension-aware rendering.</p>

</div>

---

![Cloth Simulation Demo](cloth_simulation_demo.gif)

---

## Features

- **Verlet physics** — stable, accurate point-mass simulation with configurable damping
- **Gravity** — cloth naturally drapes and falls under gravitational force
- **Anchor points** — top row pinned at every 4th point to act as a curtain rail
- **Wind system** — sinusoidal oscillating wind force toggled on/off at runtime
- **Drag interaction** — attract cloth toward the cursor with left-click
- **Tear / cut mode** — right-click or switch to cut mode to slice through the fabric
- **Auto-tear** — sticks that stretch beyond 2.8× their rest length snap automatically
- **Tension coloring** — sticks shift from green → yellow → red based on current stretch
- **Boundary collisions** — points bounce off all four screen edges
- **On-screen HUD** — live FPS counter and control reference overlay

---

## Requirements

- Python 3.7+
- Pygame 2.1+

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running

```bash
python cloth_simulation.py
```
<p align="center">
  <img src="https://raw.githubusercontent.com/loisekk/tearable/main/cloth_simulation_demo.gif" width="80%">
</p>
---

## Controls

| Key / Input | Action |
|---|---|
| `R` | Reset the cloth to its original state |
| `W` | Toggle wind on / off |
| `C` | Switch between **drag** and **cut** mode |
| `Esc` | Quit |
| Left-click | Attract cloth toward cursor (drag mode) |
| Right-click | Tear cloth at cursor (always active) |
| Left-click | Cut cloth at cursor (cut mode only) |

---

## How It Works

### Verlet Integration

Each point stores its current and previous position. Velocity is implicit — derived from the difference between the two. This makes the simulation naturally stable and energy-conserving.

```
velocity  = (current - previous) × damping
previous  = current
current  += velocity + acceleration
```

### Stick Constraints

Each connection between adjacent points enforces a rest length. On every frame, constraints are solved iteratively (5 passes) — the two endpoints are nudged apart or together to satisfy the target distance. Locked anchor points are immovable.

### Tearing

A stick is removed when its current length exceeds `REST_LENGTH × 2.8`. Mouse-based cutting removes sticks whose midpoint falls within a radius of the cursor.

### Tension Coloring

Stretch factor = `current_length / rest_length − 1`. This is mapped `[0, 0.25]` → green to red, giving instant visual feedback on stressed regions.

---

## Project Structure

```
cloth_simulation/
├── cloth_simulation.py     # Main simulation script
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── cloth_simulation_demo.gif
```

---

## Configuration

Key constants at the top of `cloth_simulation.py`:

| Constant | Default | Description |
|---|---|---|
| `COLS` | `40` | Number of cloth columns |
| `ROWS` | `25` | Number of cloth rows |
| `REST` | `18` | Rest length of each stick (px) |
| `GRAVITY` | `0.5` | Downward acceleration per frame |
| `DAMPING` | `0.99` | Velocity retention factor (0–1) |
| `ITERATIONS` | `5` | Constraint solving passes per frame |
| `TEAR_DIST` | `REST × 2.8` | Auto-tear threshold |
| `CUT_RADIUS` | `28` | Mouse cut influence radius (px) |

---

## License

MIT — free to use, modify, and distribute.
