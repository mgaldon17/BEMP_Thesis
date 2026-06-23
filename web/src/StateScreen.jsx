import { useEffect } from 'react'
import { useStore } from './store'
import Scene from './scene/Scene'
import Loader from './ui/Loader'
import Grain from './ui/Grain'
import Vignette from './ui/Vignette'

// Frozen-atom screens reused by the GitHub Actions workflows:
//  - "maintenance" : atom decomposed to 26% (the 0.26 scroll mark)
//  - "unpublished" : atom fully decomposed (1.0)
// Same Scene / DecomposeParticles as the landing — no scroll, no sections.
const STATES = {
  maintenance: {
    progress: 0.26,
    eyebrow: '☢ SCHEDULED MAINTENANCE',
    title: 'Under maintenance',
    sub: 'The landing is being updated. Back online shortly.',
  },
  unpublished: {
    progress: 1.0,
    eyebrow: '☢ REACTOR OFFLINE',
    title: 'Unpublished page',
    sub: 'This page has been unpublished.',
  },
}

export default function StateScreen({ variant }) {
  const cfg = STATES[variant] || STATES.maintenance
  const setScroll = useStore((s) => s.setScroll)
  const setMouse = useStore((s) => s.setMouse)

  // Pin the decompose progress; DecomposeParticles damps the atom toward it
  // on load (giving a brief assemble->decompose intro), then holds.
  useEffect(() => {
    setScroll(cfg.progress)
  }, [cfg.progress, setScroll])

  // Keep the mouse parallax — the only interactivity on these pages.
  useEffect(() => {
    const onMove = (e) => {
      const x = (e.clientX / window.innerWidth) * 2 - 1
      const y = (e.clientY / window.innerHeight) * 2 - 1
      setMouse([x, y])
    }
    window.addEventListener('pointermove', onMove)
    return () => window.removeEventListener('pointermove', onMove)
  }, [setMouse])

  return (
    <>
      <Scene />
      <Loader />
      <Grain />
      <Vignette />

      <div className="state-screen">
        <span className="mono eyebrow">{cfg.eyebrow}</span>
        <h1 className="state-screen__title">{cfg.title}</h1>
        <p className="state-screen__sub">{cfg.sub}</p>
      </div>
    </>
  )
}
