import { useStore } from '../store'

// Full-screen --void loading screen with an animated Cherenkov bar.
// Fades out (and stops capturing pointer events) once the scene reports loaded.
export default function Loader() {
  const loaded = useStore((s) => s.loaded)

  return (
    <div className={`loader ${loaded ? 'loader--hidden' : ''}`}>
      <div className="loader__inner">
        <span className="mono loader__label">☢ INITIALIZING REACTOR CORE</span>
        <div className="loader__bar">
          <div className="loader__fill" />
        </div>
      </div>
    </div>
  )
}
