import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

// We will mount this onto the specific div in admin.html
const rootElement = document.getElementById('analytics-root')

// Only mount if the element exists on the page (meaning we are on the Analytics tab)
if (rootElement) {
  createRoot(rootElement).render(
    <StrictMode>
      <App />
    </StrictMode>,
  )
}
