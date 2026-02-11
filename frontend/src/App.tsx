import { Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import SurveyPage from './pages/SurveyPage';
import GeneratePage from './pages/GeneratePage';
import CompletePage from './pages/CompletePage';

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<SurveyPage />} />
        <Route path="/generate/:projectId" element={<GeneratePage />} />
        <Route path="/complete/:projectId" element={<CompletePage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  );
}
