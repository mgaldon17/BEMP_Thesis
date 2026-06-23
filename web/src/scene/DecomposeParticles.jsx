import { useMemo, useRef, useState, useEffect } from 'react'
import { useFrame, extend } from '@react-three/fiber'
import { shaderMaterial } from '@react-three/drei'
import * as THREE from 'three'
import { useStore } from '../store'

import curlNoiseGLSL from './shaders/curlNoise.glsl?raw'
import vertexGLSL from './shaders/vertex.glsl?raw'
import fragmentGLSL from './shaders/fragment.glsl?raw'

// ── Tunable constants ────────────────────────────────────────────────────────
export const PARTICLE_STEP = 2        // sample 1 particle every N px (lower = denser)
export const AMPLITUDE = 7.0          // how far particles fly when fully scattered
export const FREQ = 0.22              // spatial frequency of the curl-noise flow
export const BLOOM_INTENSITY = 0.85   // Cherenkov glow strength (see Scene.jsx)
export const SUBJECT = 'image'        // 'image' (atom.jpg) | 'text'

const BASE_SIZE = 0.19                // base point size (world units, see vertex)
const PLANE_HEIGHT = 9.0              // assembled subject height in world units
const MAX_DIM = 800                   // cap the source raster (~26k particles w/ atom.jpg @ STEP 2)
const LUMA_THRESHOLD = 0.06           // skip near-black / transparent pixels
const TEXT_SUBJECT = '☢'              // used when SUBJECT === 'text'

const IMAGE_SRC = `${import.meta.env.BASE_URL}atom.jpg`

// ── Custom shader material (drei) ────────────────────────────────────────────
// curlNoise is prepended so its snoise()/curlNoise() functions are declared
// before main() in the vertex stage.
const DecomposeMaterial = shaderMaterial(
  {
    uProgress: 0,
    uTime: 0,
    uFreq: FREQ,
    uAmplitude: AMPLITUDE,
    uSize: BASE_SIZE,
    uOpacity: 0,
  },
  `${curlNoiseGLSL}\n${vertexGLSL}`,
  fragmentGLSL
)
extend({ DecomposeMaterial })

// ── Source raster -> typed arrays of particle attributes ─────────────────────
function buildAttributes(imageData, srcW, srcH) {
  const { data } = imageData
  const positions = []
  const colors = []
  const randoms = []
  const seeds = []

  const aspect = srcW / srcH
  const worldH = PLANE_HEIGHT
  const worldW = PLANE_HEIGHT * aspect

  for (let y = 0; y < srcH; y += PARTICLE_STEP) {
    for (let x = 0; x < srcW; x += PARTICLE_STEP) {
      const i = (y * srcW + x) * 4
      const r = data[i] / 255
      const g = data[i + 1] / 255
      const b = data[i + 2] / 255
      const a = data[i + 3] / 255

      const luma = 0.299 * r + 0.587 * g + 0.114 * b
      if (a < 0.1 || luma < LUMA_THRESHOLD) continue

      // UV (0..1) -> centred world plane (y flipped: image row 0 is top).
      const nx = (x / srcW - 0.5) * worldW
      const ny = (0.5 - y / srcH) * worldH
      positions.push(nx, ny, (Math.random() - 0.5) * 0.4)

      colors.push(r, g, b)
      randoms.push(Math.random())

      // Random unit-ish direction, decorrelates the curl flow per particle.
      seeds.push(
        Math.random() * 2 - 1,
        Math.random() * 2 - 1,
        Math.random() * 2 - 1
      )
    }
  }

  return {
    position: new Float32Array(positions),
    aColor: new Float32Array(colors),
    aRandom: new Float32Array(randoms),
    aSeed: new Float32Array(seeds),
    count: randoms.length,
  }
}

// Draw the configured subject onto an offscreen 2D canvas and read it back.
// Falls back to a procedurally-drawn atom if atom.jpg is missing, so the
// effect always works out of the box (drop a real HD render at public/atom.jpg
// to override it).
function rasterToImageData(canvas) {
  return canvas
    .getContext('2d')
    .getImageData(0, 0, canvas.width, canvas.height)
}

function drawSyntheticAtom(size = 320) {
  const c = document.createElement('canvas')
  c.width = c.height = size
  const ctx = c.getContext('2d')
  const cx = size / 2
  const cy = size / 2

  ctx.clearRect(0, 0, size, size)

  // Nucleus: hot white-blue core fading out (Cherenkov tint).
  const core = ctx.createRadialGradient(cx, cy, 0, cx, cy, size * 0.22)
  core.addColorStop(0, '#ffffff')
  core.addColorStop(0.35, '#cdeeff')
  core.addColorStop(0.7, '#2bd6ff')
  core.addColorStop(1, 'rgba(43,214,255,0)')
  ctx.fillStyle = core
  ctx.beginPath()
  ctx.arc(cx, cy, size * 0.22, 0, Math.PI * 2)
  ctx.fill()

  // Nucleons (protons/neutrons) clustered in the core.
  for (let i = 0; i < 26; i++) {
    const a = Math.random() * Math.PI * 2
    const r = Math.random() * size * 0.1
    ctx.fillStyle = i % 2 ? '#9ef01a' : '#e8f6ff'
    ctx.beginPath()
    ctx.arc(cx + Math.cos(a) * r, cy + Math.sin(a) * r, size * 0.012, 0, Math.PI * 2)
    ctx.fill()
  }

  // Three elliptical orbital shells at different tilts.
  const shells = [0, Math.PI / 3, -Math.PI / 3]
  ctx.lineWidth = size * 0.006
  shells.forEach((rot, idx) => {
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(rot)
    ctx.strokeStyle = 'rgba(205,238,255,0.55)'
    ctx.beginPath()
    ctx.ellipse(0, 0, size * 0.42, size * 0.16, 0, 0, Math.PI * 2)
    ctx.stroke()

    // Electron on each shell.
    const ea = (idx / shells.length) * Math.PI * 2
    ctx.fillStyle = '#2bd6ff'
    ctx.beginPath()
    ctx.arc(
      Math.cos(ea) * size * 0.42,
      Math.sin(ea) * size * 0.16,
      size * 0.02,
      0,
      Math.PI * 2
    )
    ctx.fill()
    ctx.restore()
  })

  return c
}

function drawTextSubject(text, size = 320) {
  const c = document.createElement('canvas')
  c.width = c.height = size
  const ctx = c.getContext('2d')
  ctx.fillStyle = '#cdd6dc'
  ctx.font = `${size * 0.7}px "Space Grotesk", sans-serif`
  ctx.textAlign = 'center'
  ctx.textBaseline = 'middle'
  ctx.fillText(text, size / 2, size / 2)
  return c
}

// ── Component ────────────────────────────────────────────────────────────────
export default function DecomposeParticles() {
  const pointsRef = useRef()
  const materialRef = useRef()
  const groupRef = useRef()

  const [attrs, setAttrs] = useState(null)
  const setLoaded = useStore((s) => s.setLoaded)

  // Build the geometry once on mount.
  useEffect(() => {
    let cancelled = false

    const finish = (canvas) => {
      if (cancelled) return
      const img = rasterToImageData(canvas)
      setAttrs(buildAttributes(img, canvas.width, canvas.height))
      // Give the loader a beat so its fade reads as intentional.
      setTimeout(() => !cancelled && setLoaded(true), 350)
    }

    if (SUBJECT === 'text') {
      finish(drawTextSubject(TEXT_SUBJECT))
      return () => { cancelled = true }
    }

    const image = new Image()
    image.crossOrigin = 'anonymous'
    image.onload = () => {
      // Downscale to MAX_DIM keeping aspect, then read pixels.
      const scale = Math.min(1, MAX_DIM / Math.max(image.width, image.height))
      const w = Math.max(1, Math.round(image.width * scale))
      const h = Math.max(1, Math.round(image.height * scale))
      const c = document.createElement('canvas')
      c.width = w
      c.height = h
      c.getContext('2d').drawImage(image, 0, 0, w, h)
      finish(c)
    }
    image.onerror = () => finish(drawSyntheticAtom()) // placeholder fallback
    image.src = IMAGE_SRC

    return () => { cancelled = true }
  }, [setLoaded])

  // BufferGeometry built from the attributes.
  const geometry = useMemo(() => {
    if (!attrs) return null
    const g = new THREE.BufferGeometry()
    g.setAttribute('position', new THREE.BufferAttribute(attrs.position, 3))
    g.setAttribute('aColor', new THREE.BufferAttribute(attrs.aColor, 3))
    g.setAttribute('aRandom', new THREE.BufferAttribute(attrs.aRandom, 1))
    g.setAttribute('aSeed', new THREE.BufferAttribute(attrs.aSeed, 3))
    return g
  }, [attrs])

  // Damped scroll progress (avoids 1:1 jitter with the wheel).
  const progress = useRef(0)

  useFrame((state, delta) => {
    if (!materialRef.current) return
    const { scroll, mouse } = useStore.getState()

    // Exponential damp toward the scroll target.
    const k = 1 - Math.pow(0.0015, delta) // frame-rate independent smoothing
    progress.current += (scroll - progress.current) * k

    const m = materialRef.current
    m.uProgress = progress.current
    m.uTime = state.clock.elapsedTime
    m.uOpacity += ((useStore.getState().loaded ? 1 : 0) - m.uOpacity) * (1 - Math.pow(0.01, delta))

    // Gentle whole-object rotation tied to scroll + a slow idle drift.
    if (groupRef.current) {
      groupRef.current.rotation.y = progress.current * 0.5 + state.clock.elapsedTime * 0.02
      groupRef.current.rotation.x = progress.current * 0.12
    }

    // Camera parallax: lerp toward the mouse target.
    const cam = state.camera
    const targetX = mouse[0] * 1.2
    const targetY = -mouse[1] * 0.8
    cam.position.x += (targetX - cam.position.x) * (1 - Math.pow(0.02, delta))
    cam.position.y += (targetY - cam.position.y) * (1 - Math.pow(0.02, delta))
    cam.lookAt(0, 0, 0)
  })

  if (!geometry) return null

  return (
    <group ref={groupRef}>
      <points ref={pointsRef} geometry={geometry} frustumCulled={false}>
        <decomposeMaterial
          ref={materialRef}
          transparent
          depthWrite={false}
          depthTest={false}
          blending={THREE.AdditiveBlending}
        />
      </points>
    </group>
  )
}
