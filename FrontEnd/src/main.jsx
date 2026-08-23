import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import LogiMatch from './components/LogiMatch.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <LogiMatch />
  </StrictMode>,
)
