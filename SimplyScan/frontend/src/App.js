import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import ProfilePage from './pages/ProfilePage';
import HistoryPage from './pages/HistoryPage';
import GantryPage from './pages/GantryPage'; 
import SignUpPage from './pages/SignUpPage';
import TopUpPage from './pages/TopUpPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/history" element={<HistoryPage />} />
        <Route path="/gantry" element={<GantryPage />} />  {/* New Gantry Page Route */}
        <Route path="/signup" element={<SignUpPage />} />
        <Route path="/topup" element={<TopUpPage />} />
      </Routes>
    </Router>
  );
}

export default App;

