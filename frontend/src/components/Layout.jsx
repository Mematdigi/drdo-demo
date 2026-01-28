import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  AppBar,
  Box,
  Toolbar,
  Typography,
  Button,
  Container,
  Tabs,
  Tab,
  IconButton,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Analytics as AnalyticsIcon,
  Business as BusinessIcon,
  Map as MapIcon,
  CloudUpload as UploadIcon,
  PictureAsPdf as PdfIcon,
  TableChart as ExcelIcon,
} from '@mui/icons-material';
import { generatePDFReport, generateExcelReport } from '../services/api';
import { AutoAwesome } from '@mui/icons-material';

const Layout = ({ children }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleDownloadReport = async (type) => {
    try {
      const response = type === 'pdf' 
        ? await generatePDFReport()
        : await generateExcelReport();
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `Fire_Dept_Report_${Date.now()}.${type}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Error generating report:', error);
      alert('Failed to generate report. Make sure backend is running.');
    }
  };

  const tabs = [
    { label: 'Dashboard', value: '/dashboard', icon: <DashboardIcon /> },
    { label: 'Analytics', value: '/analytics', icon: <AnalyticsIcon /> },
    { label: 'Vendors', value: '/vendors', icon: <BusinessIcon /> },
    { label: 'Geographic', value: '/geographic', icon: <MapIcon /> },
    { label: 'Upload', value: '/upload', icon: <UploadIcon /> },
    {label : 'Data Ingestion', value:'/ingestion'},
    { label: 'Smart Studio', value: '/smart-studio', icon: <AutoAwesome /> },
    { label: 'AI Studio', value: '/ai-studio', icon: <AutoAwesome /> },
  ];

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar position="sticky" sx={{ background: 'linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%)' }}>
        <Toolbar>
          <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
            <Box
              sx={{
                width: 48,
                height: 48,
                borderRadius: 2,
                background: 'linear-gradient(135deg, #f59e0b 0%, #ef4444 100%)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '1.5rem',
                mr: 2,
              }}
            >
              🚒
            </Box>
            <Box>
              <Typography variant="h6" component="div" sx={{ fontWeight: 700 }}>
                Fire Department Analytics
              </Typography>
              <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.7)' }}>
                Data-Driven Insights & Reporting Platform
              </Typography>
            </Box>
          </Box>
          
          <Button
            variant="contained"
            color="success"
            startIcon={<PdfIcon />}
            onClick={() => handleDownloadReport('pdf')}
            sx={{ mr: 1 }}
          >
            PDF
          </Button>
          <Button
            variant="contained"
            color="success"
            startIcon={<ExcelIcon />}
            onClick={() => handleDownloadReport('xlsx')}
          >
            Excel
          </Button>
        </Toolbar>
        
        <Tabs
          value={location.pathname}
          onChange={(e, value) => navigate(value)}
          sx={{
            bgcolor: 'rgba(0,0,0,0.1)',
            '& .MuiTab-root': { color: 'rgba(255,255,255,0.7)' },
            '& .Mui-selected': { color: '#fff' },
          }}
        >
          {tabs.map((tab) => (
            <Tab
              key={tab.value}
              label={tab.label}
              value={tab.value}
              icon={tab.icon}
              iconPosition="start"
            />
          ))}
        </Tabs>
      </AppBar>

      <Container maxWidth="xl" sx={{ mt: 4, mb: 4, flexGrow: 1 }}>
        {children}
      </Container>

      <Box
        component="footer"
        sx={{
          py: 3,
          px: 2,
          mt: 'auto',
          borderTop: 1,
          borderColor: 'divider',
          textAlign: 'center',
        }}
      >
        <Typography variant="body2" color="text.secondary">
          Fire Department Analytics Platform © 2026 | Powered by Python + Node.js + React
        </Typography>
      </Box>
    </Box>
  );
};

export default Layout;
