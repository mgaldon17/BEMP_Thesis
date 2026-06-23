// Film-grain overlay using an SVG feTurbulence pattern. pointer-events: none.
export default function Grain() {
  return (
    <div className="grain" aria-hidden="true">
      <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
        <filter id="grain-noise">
          <feTurbulence
            type="fractalNoise"
            baseFrequency="0.8"
            numOctaves="2"
            stitchTiles="stitch"
          />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="100%" height="100%" filter="url(#grain-noise)" />
      </svg>
    </div>
  )
}
