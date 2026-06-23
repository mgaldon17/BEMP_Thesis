import { THESIS_PDF } from './content'

export default function Hero() {
  return (
    <section className="section section--hero" id="hero">
      <div className="hero__content">
        <span className="mono eyebrow">☢ MANUEL GALDÓN · MASTER&apos;S THESIS · TUM · FRM II</span>

        <h1 className="hero__title">
          Characterization of <span className="accent">Neutron</span> Response
          of Ionization Chambers
        </h1>

        <p className="hero__subtitle">
          Atmospheric corrosion alters how magnesium ionization chambers respond
          to fast-neutron therapy beams — quantifying that dosimetric drift.
        </p>

        <div className="hero__actions">
          <a className="btn btn--primary" href={THESIS_PDF} target="_blank" rel="noreferrer">
            Read the thesis
          </a>
        </div>
      </div>

      <span className="mono hero__scroll-hint">scroll to decompose ↓</span>
    </section>
  )
}
