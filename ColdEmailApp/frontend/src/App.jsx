import { useState, useEffect } from 'react'
import { HashRouter, Routes, Route } from 'react-router-dom'
import SplashScreen from './components/SplashScreen'
import Layout from './components/Layout'
import DashboardHome from './pages/DashboardHome'

import LeadsPage from './pages/LeadsPage'

// Simple Placeholders for modules to be built next
import CampaignsPage from './pages/CampaignsPage'

import UniboxPage from './pages/UniboxPage'
import SettingsPage from './pages/SettingsPage'

function App() {
  const [loading, setLoading] = useState(true)

  if (loading) {
    return <SplashScreen onFinish={() => setLoading(false)} />
  }

  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<DashboardHome />} />
          <Route path="leads" element={<LeadsPage />} />
          <Route path="campaigns" element={<CampaignsPage />} />
          <Route path="unibox" element={<UniboxPage />} />
          <Route path="settings" element={<SettingsPage />} />
        </Route>
      </Routes>
    </HashRouter>
  )
}

export default App
