const ITEMS = [
  { sym: 'Σ', name: 'MCNP6', tag: 'MONTE CARLO', desc: 'Neutron / gamma transport simulation of the chamber response.' },
  { sym: 'λ', name: 'Python', tag: 'AUTOMATION', desc: 'Toolkit that builds, runs and analyses the MCNP simulations.' },
  { sym: '∫', name: 'LaTeX', tag: 'THESIS', desc: 'The written thesis and its typesetting.' },
  { sym: 'f(x)', name: 'MATLAB', tag: 'ANALYSIS', desc: 'Auxiliary analysis and plotting of results.' },
  { sym: '⚖', name: 'PTB calibration', tag: 'METROLOGY', desc: 'Traceable calibration of the chambers, performed at the PTB.' },
  { sym: '◎', name: 'Neutron / X-ray CT', tag: 'IMAGING', desc: 'Imaging the atmospheric corrosion layer on the chambers.' },
]

export default function Stack() {
  return (
    <section className="section section--stack" id="stack">
      <div className="section__head">
        <span className="mono section__num">[ 04 ]</span>
        <h2 className="section__title">Stack &amp; methods</h2>
      </div>

      <div className="stack__grid">
        {ITEMS.map((it) => (
          <article className="material" key={it.name}>
            <span className="material__sym">{it.sym}</span>
            <span className="mono material__tag">{it.tag}</span>
            <h3 className="material__name">{it.name}</h3>
            <p className="material__desc">{it.desc}</p>
          </article>
        ))}
      </div>
    </section>
  )
}
