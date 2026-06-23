import { useEffect, useRef } from 'react'
import Lenis from 'lenis'
import { useStore } from './store'
import Scene from './scene/Scene'

import Loader from './ui/Loader'
import Grain from './ui/Grain'
import Vignette from './ui/Vignette'
import ScrollProgress from './ui/ScrollProgress'

import Hero from './sections/Hero'
import About from './sections/About'
import FrmII from './sections/FrmII'
import Team from './sections/Team'
import Stack from './sections/Stack'
import Pipeline from './sections/Pipeline'
import Cta from './sections/Cta'
import Footer from './sections/Footer'

export default function App() {
  const setScroll = useStore((s) => s.setScroll)
  const setMouse = useStore((s) => s.setMouse)
  const lenisRef = useRef(null)

  // ── Smooth scroll (Lenis) is the single scroll source ──────────────────
  useEffect(() => {
    const lenis = new Lenis({
      duration: 1.1,
      smoothWheel: true,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    })
    lenisRef.current = lenis

    lenis.on('scroll', ({ scroll, limit }) => {
      // Normalize 0..1 over the full scrollable height and push to the store.
      setScroll(limit > 0 ? scroll / limit : 0)
    })

    let raf
    const loop = (time) => {
      lenis.raf(time)
      raf = requestAnimationFrame(loop)
    }
    raf = requestAnimationFrame(loop)

    return () => {
      cancelAnimationFrame(raf)
      lenis.destroy()
    }
  }, [setScroll])

  // ── Mouse parallax target ──────────────────────────────────────────────
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
      {/* Fixed full-screen WebGL canvas — never scrolls */}
      <Scene />

      {/* Overlays (all pointer-events: none) */}
      <Loader />
      <Grain />
      <Vignette />
      <ScrollProgress />

      {/* Scrolling content above the canvas */}
      <main>
        <Hero />
        <About />
        <FrmII />
        <Team />
        <Stack />
        <Pipeline />
        <Cta />
        <Footer />
      </main>
    </>
  )
}
