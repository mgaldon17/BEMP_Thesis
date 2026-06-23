import { THESIS_PDF, REPO } from './content'

export default function Cta() {
  return (
    <section className="section section--cta" id="cta">
      <h2 className="cta__title">
        Read the full <span className="accent">thesis</span>.
      </h2>
      <p className="cta__sub">
        A real metrology problem in neutron dosimetry — tackled with CT imaging,
        96-core MPI Monte Carlo simulation (MCNP6) and traceable PTB calibration.
      </p>
      <div className="cta__actions">
        <a className="btn btn--primary" href={THESIS_PDF} target="_blank" rel="noreferrer">
          Thesis PDF
        </a>
        <a className="btn btn--ghost" href={REPO} target="_blank" rel="noreferrer">
          Project repository
        </a>
      </div>
    </section>
  )
}
