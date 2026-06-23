import { Canvas } from '@react-three/fiber'
import { EffectComposer, Bloom } from '@react-three/postprocessing'
import { Suspense } from 'react'
import DecomposeParticles, { BLOOM_INTENSITY } from './DecomposeParticles'

// Fixed, full-screen canvas living behind the scrolling content.
// Pointer events are disabled so the page scrolls/clicks through to <main>.
export default function Scene() {
  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        zIndex: 1,
        pointerEvents: 'none',
      }}
    >
      <Canvas
        dpr={[1, 2]}
        camera={{ position: [0, 0, 14], fov: 45, near: 0.1, far: 100 }}
        gl={{ antialias: true, alpha: true, powerPreference: 'high-performance' }}
      >
        <color attach="background" args={['#06080a']} />
        <Suspense fallback={null}>
          <DecomposeParticles />
        </Suspense>

        {/* Subtle Cherenkov-blue bloom — the atom "emits radiation". */}
        <EffectComposer disableNormalPass>
          <Bloom
            intensity={BLOOM_INTENSITY}
            luminanceThreshold={0.15}
            luminanceSmoothing={0.9}
            mipmapBlur
            radius={0.7}
          />
        </EffectComposer>
      </Canvas>
    </div>
  )
}
