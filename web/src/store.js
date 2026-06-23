import { create } from 'zustand'

// Single source of scroll truth. Lenis writes `scroll` (0..1, normalized over
// the whole page) on every frame; the particle system reads it in useFrame and
// damps toward it. The mouse parallax target lives here too.
export const useStore = create((set) => ({
  scroll: 0,            // normalized 0..1 scroll progress
  mouse: [0, 0],        // -1..1 normalized pointer, for camera parallax
  loaded: false,        // texture / scene ready -> hide loader

  setScroll: (scroll) => set({ scroll }),
  setMouse: (mouse) => set({ mouse }),
  setLoaded: (loaded) => set({ loaded }),
}))
