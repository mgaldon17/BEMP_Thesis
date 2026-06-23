import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { fileURLToPath } from 'url'

// GitHub Pages PROJECT page: the site is served from
//   https://<user>.github.io/<REPO_NAME>/
// so every asset URL must be prefixed with the repo name.
// ── EDIT HERE if you rename the repository ──────────────────────────
const REPO_NAME = 'Master-s-Thesis-of-Manuel-Galdon'

export default defineConfig({
  // In dev `base` is "/", in build it becomes "/<REPO_NAME>/".
  base: process.env.NODE_ENV === 'production' ? `/${REPO_NAME}/` : '/',
  plugins: [react()],
  // Allow importing .glsl files as raw strings.
  assetsInclude: ['**/*.glsl'],
  build: {
    // Multi-page: the landing plus two "frozen atom" state pages that the
    // GitHub Actions workflows publish as index.html when taking the site
    // into maintenance / unpublishing it. They reuse the same bundle.
    rollupOptions: {
      input: {
        main: fileURLToPath(new URL('./index.html', import.meta.url)),
        maintenance: fileURLToPath(new URL('./maintenance.html', import.meta.url)),
        unpublish: fileURLToPath(new URL('./unpublish.html', import.meta.url)),
      },
    },
  },
})
