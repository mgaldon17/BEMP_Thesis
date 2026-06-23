export default function About() {
  return (
    <section className="section section--about" id="about">
      <div className="section__head">
        <span className="mono section__num">[ 01 ]</span>
        <h2 className="section__title">The problem</h2>
      </div>

      <div className="prose">
        <p>
          Magnesium ionization chambers are used to measure dose in{' '}
          <strong>fast-neutron therapy</strong>. Over time, their magnesium
          surfaces develop an atmospheric{' '}
          <strong>corrosion layer (hydromagnesite)</strong> that changes the
          chamber&apos;s <strong>sensitivity</strong> to radiation — introducing
          uncertainty into dosimetric measurements where accuracy is critical.
        </p>
        <p>
          This thesis characterizes that effect by combining{' '}
          <strong>neutron / X-ray CT imaging</strong> to inspect the corrosion,{' '}
          <strong>Monte Carlo simulations with MCNP6</strong> to model the
          chamber response, and a traceable{' '}
          <strong>calibration at the PTB</strong> (Physikalisch-Technische
          Bundesanstalt). Two PTW chambers are studied: the{' '}
          <strong>TM33054</strong> (magnesium) and the{' '}
          <strong>TM33053</strong> (tissue-equivalent, A-150).
        </p>
        <p>
          A reproducible <strong>Python automation toolkit</strong> prepares,
          runs and analyses the MCNP simulations end to end — closing the loop
          from input deck to plotted result.
        </p>
      </div>

      <ul className="microdata">
        <li className="mono"><span>INSTITUTION</span>TUM · FRM II / MLZ</li>
        <li className="mono"><span>YEAR</span>2024</li>
        <li className="mono"><span>METHODS</span>MCNP6 · CT · PTB</li>
      </ul>
    </section>
  )
}
