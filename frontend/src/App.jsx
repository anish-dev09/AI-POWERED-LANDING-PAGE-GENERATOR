import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Businesses from './pages/Businesses';
import GeneratePage from './pages/GeneratePage';
import LandingPages from './pages/LandingPages';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="businesses" element={<Businesses />} />
          <Route path="generate" element={<GeneratePage />} />
          <Route path="landing-pages" element={<LandingPages />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;

