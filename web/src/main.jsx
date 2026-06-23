import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import StateScreen from './StateScreen.jsx'
import './styles.css'

// `data-state` on #root selects a frozen "maintenance" / "unpublished" screen
// (set by maintenance.html / unpublish.html). Empty -> the full landing.
const rootEl = document.getElementById('root')
const state = rootEl.dataset.state || ''

ReactDOM.createRoot(rootEl).render(
  <React.StrictMode>
    {state ? <StateScreen variant={state} /> : <App />}
  </React.StrictMode>
)
