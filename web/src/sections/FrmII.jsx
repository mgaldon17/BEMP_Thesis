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
            PLACEHOLDER IMAGE — public/frmii.jpg
            Replace with a properly-licensed photo of the FRM II / Garching
            campus: use a Wikimedia Commons image (free licence) or one from
            the official MLZ press kit, and update the attribution caption
            below to match. Do NOT hotlink Google Images results.
          */}
          <img
            className="frmii__img"
            src={`${import.meta.env.BASE_URL}frmii.jpg`}
            alt="The FRM II research neutron source in Garching"
            loading="lazy"
          />
          <figcaption className="mono frmii__credit">
            {/* // rellenar atribución real: e.g. "Photo: <author>, Wikimedia Commons, CC BY-SA 4.0" */}
            IMAGE PLACEHOLDER · replace with licensed photo + attribution
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
            Its intense neutron beams enable the imaging and irradiation work
            behind this thesis — including the neutron CT used to inspect the
            corrosion layer on the chambers.
          </p>
        </div>
      </div>
    </section>
  )
}
