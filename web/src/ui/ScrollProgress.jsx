import { useEffect, useRef } from 'react'
import { useStore } from '../store'

// Vertical progress bar pinned to the right edge: fills in --cherenkov and
// shows the percentage in mono. Subscribes to the store transiently to avoid
// re-rendering React on every scroll frame.
export default function ScrollProgress() {
  const fillRef = useRef(null)
  const pctRef = useRef(null)

  useEffect(() => {
    // Transient subscription -> direct DOM writes, no React re-render.
    const unsub = useStore.subscribe((state) => {
      const v = Math.round(state.scroll * 100)
      if (fillRef.current) fillRef.current.style.height = `${v}%`
      if (pctRef.current) pctRef.current.textContent = String(v).padStart(3, '0')
    })
    return unsub
  }, [])

  return (
    <div className="scroll-progress" aria-hidden="true">
      <span ref={pctRef} className="mono scroll-progress__pct">000</span>
      <div className="scroll-progress__track">
        <div ref={fillRef} className="scroll-progress__fill" />
      </div>
      <span className="mono scroll-progress__unit">%</span>
    </div>
  )
}
