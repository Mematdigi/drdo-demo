import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Analytics from './pages/Analytics';
import Vendors from './pages/Vendors';
import Geographic from './pages/Geographic';
import Upload from './pages/Upload';
import DataIngestion from './pages/DataIngestion';
import SmartDataStudio from './pages/Smartdatastudio';
import AutonomousVisualizer from './pages/Autonomousvisualizer';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#3b82f6',
    },
    secondary: {
      main: '#10b981',
    },
    background: {
      default: '#0f172a',
      paper: '#1e293b',
    },
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
    ].join(','),
  },
});

function App() {
  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/vendors" element={<Vendors />} />
            <Route path="/geographic" element={<Geographic />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/ingestion" element={<DataIngestion />} />
            <Route path ="/smart-studio" element={<SmartDataStudio />} />
            <Route path = "/ai-studio" element={ <AutonomousVisualizer />}/>
          </Routes>
        </Layout>
      </Router>
    </ThemeProvider>
  );
}

export default App;
