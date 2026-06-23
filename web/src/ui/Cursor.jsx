import { useEffect, useRef } from 'react'

// Custom cursor: a --steel ring using mix-blend-mode: difference that grows
// when hovering interactive elements. Hidden on touch / small screens via CSS.
export default function Cursor() {
  const ref = useRef(null)

  useEffect(() => {
    const el = ref.current
    if (!el) return

    let x = window.innerWidth / 2
    let y = window.innerHeight / 2
    let tx = x
    let ty = y
    let raf

    const onMove = (e) => {
      tx = e.clientX
      ty = e.clientY
    }

    // Grow over links/buttons/anything tagged data-hover.
    const onOver = (e) => {
      if (e.target.closest('a, button, [data-hover]')) {
        el.classList.add('cursor--hover')
      }
    }
    const onOut = (e) => {
      if (e.target.closest('a, button, [data-hover]')) {
        el.classList.remove('cursor--hover')
      }
    }

    const loop = () => {
      x += (tx - x) * 0.2
      y += (ty - y) * 0.2
      el.style.transform = `translate(${x}px, ${y}px) translate(-50%, -50%)`
      raf = requestAnimationFrame(loop)
    }
    loop()

    window.addEventListener('pointermove', onMove)
    document.addEventListener('pointerover', onOver)
    document.addEventListener('pointerout', onOut)
    return () => {
      cancelAnimationFrame(raf)
      window.removeEventListener('pointermove', onMove)
      document.removeEventListener('pointerover', onOver)
      document.removeEventListener('pointerout', onOut)
    }
  }, [])

  return <div ref={ref} className="cursor" aria-hidden="true" />
}
