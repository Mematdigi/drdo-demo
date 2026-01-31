import React, { useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import {
  Box, AppBar, Toolbar, Typography, Tabs, Tab, Container, CssBaseline,
  IconButton, Drawer, List, ListItem, ListItemIcon, ListItemText, useMediaQuery
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Analytics as AnalyticsIcon,
  Business as VendorsIcon,
  Map as GeoIcon,
  CloudUpload as UploadIcon,
  DataObject as DataIcon,
  AutoAwesome as AIIcon,
  Menu as MenuIcon,
  Settings as SettingsIcon
} from '@mui/icons-material';

// Import all page components
import DashboardPage from './pages/Dashboard';
import AnalyticsPage from './pages/Analytics';
import VendorsPage from './pages/Vendors';
import GeographicPage from './pages/Geographic';
import UploadPage from './pages/Upload';
import DataIngestionPage from './pages/DataIngestion';
import SmartStudioPage from './pages/Smartdatastudio';
import AutonomousVisualizer from './pages/Autonomousvisualizer';
//import AIStudioPage from './pages/AIStudio';


// Professional Light Theme
const lightTheme = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#2563eb', light: '#60a5fa', dark: '#1e40af' },
    secondary: { main: '#7c3aed', light: '#a78bfa', dark: '#5b21b6' },
    success: { main: '#10b981', light: '#34d399', dark: '#059669' },
    warning: { main: '#f59e0b', light: '#fbbf24', dark: '#d97706' },
    error: { main: '#ef4444', light: '#f87171', dark: '#dc2626' },
    background: { default: '#f8fafc', paper: '#ffffff', secondary: '#f1f5f9' },
    text: { primary: '#0f172a', secondary: '#475569', disabled: '#94a3b8' },
    divider: '#e2e8f0',
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    button: { textTransform: 'none', fontWeight: 500 },
  },
  shape: { borderRadius: 12 },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 1px 3px 0 rgb(0 0 0 / 0.1)',
          borderRadius: 16,
          border: '1px solid #e2e8f0',
          transition: 'all 0.3s ease',
          '&:hover': {
            boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)',
            transform: 'translateY(-2px)',
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 10,
          padding: '10px 20px',
          boxShadow: 'none',
          '&:hover': { boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' },
        },
      },
    },
  },
});

function TabPanel({ children, value, index }) {
  return (
    <div hidden={value !== index} style={{ height: '100%' }}>
      {value === index && <Box sx={{ height: '100%' }}>{children}</Box>}
    </div>
  );
}

function ProfessionalApp() {
  const [currentTab, setCurrentTab] = useState(0);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const isMobile = useMediaQuery(lightTheme.breakpoints.down('md'));

  const tabs = [
    { label: 'Dashboard', icon: <DashboardIcon />, component: DashboardPage },
    { label: 'Analytics', icon: <AnalyticsIcon />, component: AnalyticsPage },
    { label: 'Vendors', icon: <VendorsIcon />, component: VendorsPage },
    { label: 'Geographic', icon: <GeoIcon />, component: GeographicPage },
    { label: 'Upload', icon: <UploadIcon />, component: UploadPage },
    { label: 'Data Ingestion', icon: <DataIcon />, component: DataIngestionPage },
    { label: 'Smart Studio', icon: <SettingsIcon />, component: SmartStudioPage },
    { label: 'AI Studio', icon: <SettingsIcon />, component: AutonomousVisualizer },

    //{ label: 'AI Studio', icon: <AIIcon />, component: AIStudioPage },
    
  ];

  const handleTabChange = (event, newValue) => {
    setCurrentTab(newValue);
    if (isMobile) setDrawerOpen(false);
  };

  return (
    <ThemeProvider theme={lightTheme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', flexDirection: 'column', height: '100vh', bgcolor: 'background.default' }}>
        
        {/* Top AppBar */}
        <AppBar position="static" elevation={0} sx={{ bgcolor: 'background.paper', borderBottom: '1px solid', borderColor: 'divider' }}>
          <Toolbar>
            {isMobile && (
              <IconButton edge="start" onClick={() => setDrawerOpen(!drawerOpen)} sx={{ mr: 2, color: 'primary.main' }}>
                <MenuIcon />
              </IconButton>
            )}
            
            <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
              <Box sx={{ 
                bgcolor: 'primary.main', 
                width: 40, 
                height: 40, 
                borderRadius: 2, 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center',
                mr: 2
              }}>
                <DashboardIcon sx={{ color: 'white' }} />
              </Box>
              <Box>
                <Typography variant="h6" sx={{ fontWeight: 700, color: 'text.primary', lineHeight: 1.2 }}>
                  Fire Department Analytics
                </Typography>
                <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                  Data-Driven Insights & Reporting Platform
                </Typography>
              </Box>
            </Box>

            {!isMobile && (
              <Tabs 
                value={currentTab} 
                onChange={handleTabChange}
                sx={{ 
                  '& .MuiTab-root': { 
                    minHeight: 64,
                    color: 'text.secondary',
                    '&.Mui-selected': { color: 'primary.main' }
                  }
                }}
                TabIndicatorProps={{ sx: { height: 3, borderRadius: '3px 3px 0 0' } }}
              >
                {tabs.map((tab, index) => (
                  <Tab 
                    key={index} 
                    label={tab.label} 
                    icon={tab.icon}
                    iconPosition="start"
                    sx={{ fontWeight: 500 }}
                  />
                ))}
              </Tabs>
            )}
          </Toolbar>
        </AppBar>

        {/* Mobile Drawer */}
        {isMobile && (
          <Drawer anchor="left" open={drawerOpen} onClose={() => setDrawerOpen(false)}>
            <Box sx={{ width: 280, pt: 2 }}>
              <Typography variant="h6" sx={{ px: 2, mb: 2, fontWeight: 700 }}>
                Navigation
              </Typography>
              <List>
                {tabs.map((tab, index) => (
                  <ListItem
                    button
                    key={index}
                    selected={currentTab === index}
                    onClick={() => handleTabChange(null, index)}
                    sx={{
                      mb: 0.5,
                      mx: 1,
                      borderRadius: 2,
                      '&.Mui-selected': {
                        bgcolor: 'primary.main',
                        color: 'white',
                        '& .MuiListItemIcon-root': { color: 'white' },
                        '&:hover': { bgcolor: 'primary.dark' }
                      }
                    }}
                  >
                    <ListItemIcon sx={{ color: currentTab === index ? 'white' : 'text.secondary' }}>
                      {tab.icon}
                    </ListItemIcon>
                    <ListItemText primary={tab.label} />
                  </ListItem>
                ))}
              </List>
            </Box>
          </Drawer>
        )}

        {/* Main Content Area */}
        <Box sx={{ flexGrow: 1, overflow: 'auto', bgcolor: 'background.default' }}>
          <Container maxWidth="xl" sx={{ py: 4, height: '100%' }}>
            {tabs.map((tab, index) => (
              <TabPanel key={index} value={currentTab} index={index}>
                <tab.component />
              </TabPanel>
            ))}
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default ProfessionalApp;
