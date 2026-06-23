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
          <h3 className="card__name">Manuel Trigueros Galdón</h3>
          <p className="card__detail">
            M.Sc. Biomedical Engineering &amp; Medical Physics — TUM
          </p>
        </article>

        {/* // rellenar con nombres reales — supervisores TUM / FRM II */}
        <article className="card card--placeholder">
          <span className="mono card__role">SUPERVISION · TUM / FRM II</span>
          <h3 className="card__name">— to be filled —</h3>
          <p className="card__detail">{/* // rellenar con nombres reales */}Thesis supervisors</p>
        </article>

        {/* // rellenar con nombres reales — colaboradores PTB */}
        <article className="card card--placeholder">
          <span className="mono card__role">COLLABORATION · PTB</span>
          <h3 className="card__name">— to be filled —</h3>
          <p className="card__detail">{/* // rellenar con nombres reales */}Calibration partners</p>
        </article>
      </div>
    </section>
  )
}
