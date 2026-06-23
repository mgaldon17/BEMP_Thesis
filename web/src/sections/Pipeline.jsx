// The simulation pipeline as an inline SVG flow diagram.
// Flow:  Input deck -> run.py -> MCNP6 -> Output -> analysis.py
//        -> result.txt -> Plots ;  side branch: run.py -> notification bot.
// Palette: graphite boxes, fine steel borders, --cherenkov flow,
//          --uranium accents on the result nodes. Mono labels throughout.
export default function Pipeline() {
  return (
    <section className="section section--pipeline" id="pipeline">
      <div className="section__head">
        <span className="mono section__num">[ 05 ]</span>
        <h2 className="section__title">The simulation pipeline</h2>
      </div>

      <p className="prose pipeline__intro">
        Every run is generated, executed and analysed by the Python toolkit —
        from the MCNP input deck through transport to the final plotted vectors.
      </p>

      <div className="pipeline__diagram">
        <svg viewBox="0 0 940 760" role="img" aria-label="Simulation pipeline diagram" preserveAspectRatio="xMidYMin meet">
          <defs>
            <marker id="arrow" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto" markerUnits="strokeWidth">
              <path d="M0,0 L6,3 L0,6 Z" fill="#2bd6ff" />
            </marker>
            <marker id="arrowDim" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto" markerUnits="strokeWidth">
              <path d="M0,0 L6,3 L0,6 Z" fill="#7e8c94" />
            </marker>
          </defs>

          {/* ── Input deck ─────────────────────────────────────────── */}
          <g className="node">
            <rect x="250" y="20" width="440" height="180" rx="6" className="box" />
            <text x="270" y="48" className="dlabel dlabel--accent">INPUT DECK</text>
            <text x="270" y="78" className="ditem">Source · MEDAPP / Sr-90</text>
            <text x="270" y="102" className="ditem">Materials · hydromagnesite (varying % water)</text>
            <text x="270" y="126" className="ditem">Geometry / Planes</text>
            <text x="270" y="150" className="ditem">Tallies · Mode</text>
            <text x="270" y="174" className="ditem">N particles ≈ 1e9</text>
          </g>
          <line x1="470" y1="200" x2="470" y2="244" className="flow" markerEnd="url(#arrow)" />

          {/* ── run.py ─────────────────────────────────────────────── */}
          <g className="node">
            <rect x="350" y="248" width="240" height="56" rx="6" className="box box--run" />
            <text x="470" y="272" className="dlabel dlabel--accent" textAnchor="middle">run.py</text>
            <text x="470" y="292" className="ditem" textAnchor="middle">build · launch · trigger analysis</text>
          </g>
          <line x1="470" y1="304" x2="470" y2="348" className="flow" markerEnd="url(#arrow)" />

          {/* side branch -> notification bot */}
          <path d="M590,276 H760" className="flow flow--dim" markerEnd="url(#arrowDim)" />
          <g className="node">
            <rect x="760" y="248" width="160" height="56" rx="6" className="box box--ghost" />
            <text x="840" y="272" className="dlabel" textAnchor="middle">notification bot</text>
            <text x="840" y="292" className="ditem ditem--dim" textAnchor="middle">“simulation finished”</text>
          </g>

          {/* ── MCNP6 ──────────────────────────────────────────────── */}
          <g className="node">
            <rect x="350" y="352" width="240" height="56" rx="6" className="box" />
            <text x="470" y="376" className="dlabel" textAnchor="middle">MCNP6</text>
            <text x="470" y="396" className="ditem" textAnchor="middle">Monte Carlo n / γ transport</text>
          </g>
          <line x1="470" y1="408" x2="470" y2="452" className="flow" markerEnd="url(#arrow)" />

          {/* ── Output ─────────────────────────────────────────────── */}
          <g className="node">
            <rect x="350" y="456" width="240" height="56" rx="6" className="box" />
            <text x="470" y="480" className="dlabel" textAnchor="middle">Output</text>
            <text x="470" y="500" className="ditem" textAnchor="middle">.o / mctal</text>
          </g>
          <line x1="470" y1="512" x2="470" y2="556" className="flow" markerEnd="url(#arrow)" />

          {/* ── analysis.py ────────────────────────────────────────── */}
          <g className="node">
            <rect x="320" y="560" width="300" height="60" rx="6" className="box box--run" />
            <text x="470" y="584" className="dlabel dlabel--accent" textAnchor="middle">analysis.py</text>
            <text x="470" y="604" className="ditem" textAnchor="middle">parse tallies → value/error · argon-density sweep</text>
          </g>
          <line x1="470" y1="620" x2="470" y2="664" className="flow" markerEnd="url(#arrow)" />

          {/* ── result.txt + Plots (result nodes, uranium accent) ──── */}
          <g className="node">
            <rect x="250" y="668" width="190" height="56" rx="6" className="box box--result" />
            <text x="345" y="692" className="dlabel dlabel--result" textAnchor="middle">result.txt</text>
            <text x="345" y="712" className="ditem" textAnchor="middle">vectors</text>
          </g>
          <line x1="440" y1="696" x2="498" y2="696" className="flow flow--result" markerEnd="url(#arrow)" />
          <g className="node">
            <rect x="500" y="668" width="190" height="56" rx="6" className="box box--result" />
            <text x="595" y="692" className="dlabel dlabel--result" textAnchor="middle">Plots</text>
            <text x="595" y="712" className="ditem" textAnchor="middle">MATLAB / Python</text>
          </g>
        </svg>
      </div>
    </section>
  )
}
