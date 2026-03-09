import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './stores/authStore'
import Layout from './components/Layout'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import SketchBuilder from './pages/SketchBuilder'
import SuspectDatabase from './pages/SuspectDatabase'
import CaseManagement from './pages/CaseManagement'
import Recognition from './pages/Recognition'
import Settings from './pages/Settings'

function App() {
  const { isAuthenticated } = useAuthStore()

  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      
      {isAuthenticated ? (
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="sketch-builder" element={<SketchBuilder />} />
          <Route path="suspects" element={<SuspectDatabase />} />
          <Route path="cases" element={<CaseManagement />} />
          <Route path="recognition" element={<Recognition />} />
          <Route path="settings" element={<Settings />} />
        </Route>
      ) : (
        <Route path="*" element={<Navigate to="/login" replace />} />
      )}
    </Routes>
  )
}

export default App
