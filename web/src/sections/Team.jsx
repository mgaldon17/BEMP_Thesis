export default function Team() {
  return (
    <section className="section section--team" id="team">
      <div className="section__head">
        <span className="mono section__num">[ 03 ]</span>
        <h2 className="section__title">Acknowledgements</h2>
      </div>

      <div className="team__grid">
        {/* Author — verified */}
        <article className="card card--author">
          <span className="mono card__role">AUTHOR</span>
          <h3 className="card__name">Manuel Galdón</h3>
          <p className="card__detail">
            M.Sc. Biomedical Engineering &amp; Medical Physics — TUM
          </p>
        </article>

        {/* Supervision — from the thesis acknowledgements */}
        <article className="card">
          <span className="mono card__role">SUPERVISION · FRM II / TUM</span>
          <h3 className="card__name">Dr. Tobias Chemnitz</h3>
          <p className="card__detail">
            Continuous supervision (FRM II) · Prof. Dr. Peter Müller-Buschbaum,
            supervisor (TUM)
          </p>
        </article>

        {/* Collaboration — from the thesis acknowledgements */}
        <article className="card">
          <span className="mono card__role">COLLABORATION · FRM II / PTB</span>
          <h3 className="card__name">Dr. Lucas Sommer</h3>
          <p className="card__detail">
            Neutron-dosimetry simulations (FRM II) · Dr. Ralf Nolte, PTB
            calibration
          </p>
        </article>
      </div>
    </section>
  )
}
