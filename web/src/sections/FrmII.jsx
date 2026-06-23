export default function FrmII() {
  return (
    <section className="section section--frmii" id="frmii">
      <div className="section__head">
        <span className="mono section__num">[ 02 ]</span>
        <h2 className="section__title">FRM II · Garching</h2>
      </div>

      <div className="frmii__layout">
        <figure className="frmii__figure">
          {/*
            "View in the pool of FRM II" — photo © Bernhard Ludewig / TUM.
            Source: https://www.mep.tum.de/cnsi/projekte/conversion-of-frm-ii/
            Used here with visible credit. If reuse rights are ever a concern,
            replace public/frmii.jpg with a Wikimedia Commons / MLZ press-kit
            image and update the caption below to match.
          */}
          <img
            className="frmii__img"
            src={`${import.meta.env.BASE_URL}frmii.jpg`}
            alt="View in the pool of the FRM II research neutron source, Garching"
            loading="lazy"
          />
          <figcaption className="mono frmii__credit">
            Photo: © Bernhard Ludewig / TUM ·{' '}
            <a href="https://www.mep.tum.de/cnsi/projekte/conversion-of-frm-ii/" target="_blank" rel="noreferrer">
              mep.tum.de
            </a>
          </figcaption>
        </figure>

        <div className="prose frmii__text">
          <p>
            The <strong>FRM II</strong> (Forschungs-Neutronenquelle Heinz
            Maier-Leibnitz) is the research neutron source operated by the
            Technical University of Munich in Garching, at the heart of the{' '}
            <strong>Heinz Maier-Leibnitz Zentrum (MLZ)</strong>.
          </p>
          <p>
            Its medical application facility, <strong>MEDAPP</strong>, supplies
            a beam of fast neutrons produced by{' '}
            <strong><sup>235</sup>U fission</strong> —
            used for <strong>Fast Neutron Therapy</strong>, the palliative
            treatment of shallow tumours that is the clinical context this
            thesis is built around.
          </p>
        </div>
      </div>
    </section>
  )
}
