import React, { useState } from 'react';
import {
  Box, Card, CardContent, Typography, Grid, Button, Tabs, Tab,
  TextField, Select, MenuItem, FormControl, InputLabel, Alert,
  LinearProgress, Chip, IconButton, List, ListItem, ListItemText,
  Dialog, DialogTitle, DialogContent, DialogActions, Stepper, Step, StepLabel
} from '@mui/material';
import {
  CloudUpload, Storage, Api, Cloud, Refresh, CheckCircle, Error as ErrorIcon,
  Delete, Settings, Add
} from '@mui/icons-material';

function MultiSourceDataIngestion() {
  const [activeSource, setActiveSource] = useState(0);
  const [loading, setLoading] = useState(false);
  const [connections, setConnections] = useState([]);
  const [dialogOpen, setDialogOpen] = useState(false);

  // Data source configurations
  const dataSources = [
    {
      id: 'file',
      name: 'Files',
      icon: <CloudUpload />,
      color: '#3b82f6',
      description: 'Upload Excel, CSV, JSON, or connect to Google Sheets',
      supported: ['Excel (.xlsx, .xls)', 'CSV (.csv)', 'JSON (.json)', 'TSV (.tsv)', 'Google Sheets']
    },
    {
      id: 'database',
      name: 'Databases',
      icon: <Storage />,
      color: '#10b981',
      description: 'Connect to SQL & NoSQL databases',
      supported: ['MySQL', 'PostgreSQL', 'MongoDB', 'SQL Server', 'Oracle', 'SQLite']
    },
    {
      id: 'api',
      name: 'APIs',
      icon: <Api />,
      color: '#f59e0b',
      description: 'Fetch data from REST & GraphQL APIs',
      supported: ['REST API', 'GraphQL', 'SOAP', 'Webhook', 'Custom endpoints']
    },
    {
      id: 'cloud',
      name: 'Cloud Storage',
      icon: <Cloud />,
      color: '#7c3aed',
      description: 'Import from cloud storage platforms',
      supported: ['AWS S3', 'Google Cloud Storage', 'Azure Blob', 'Dropbox', 'OneDrive']
    },
    {
      id: 'streaming',
      name: 'Real-Time',
      icon: <Refresh />,
      color: '#ef4444',
      description: 'Stream data from real-time sources',
      supported: ['Kafka', 'RabbitMQ', 'MQTT', 'WebSocket', 'Server logs', 'IoT devices']
    }
  ];

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:3001/api/data/ingest/file', {
        method: 'POST',
        body: formData
      });

      const result = await response.json();
      
      if (result.success) {
        setConnections([...connections, {
          id: Date.now(),
          type: 'file',
          name: file.name,
          status: 'connected',
          rows: result.rows,
          columns: result.columns,
          timestamp: new Date().toLocaleString()
        }]);
      }
    } catch (error) {
      console.error('Upload error:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderFileUpload = () => (
    <Box>
      <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
        Upload Files
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Supports Excel, CSV, JSON, TSV files. Auto-detects schema and data types.
      </Typography>

      <Card sx={{ mb: 3, bgcolor: 'background.secondary' }}>
        <CardContent>
          <Box sx={{
            border: '2px dashed #cbd5e1',
            borderRadius: 3,
            p: 4,
            textAlign: 'center',
            cursor: 'pointer',
            transition: 'all 0.3s',
            '&:hover': {
              borderColor: 'primary.main',
              bgcolor: 'rgba(37, 99, 235, 0.02)'
            }
          }}
          component="label">
            <input type="file" hidden accept=".csv,.xlsx,.xls,.json,.tsv" onChange={handleFileUpload} />
            <CloudUpload sx={{ fontSize: 64, color: 'primary.main', mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              Drop files here or click to browse
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Excel, CSV, JSON, TSV supported • Max 100MB
            </Typography>
          </Box>
        </CardContent>
      </Card>

      <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 600, mt: 3 }}>
        Google Sheets Integration
      </Typography>
      <Card>
        <CardContent>
          <TextField
            fullWidth
            label="Google Sheets URL"
            placeholder="https://docs.google.com/spreadsheets/d/..."
            variant="outlined"
            sx={{ mb: 2 }}
          />
          <Button variant="contained" startIcon={<Add />}>
            Connect Google Sheet
          </Button>
        </CardContent>
      </Card>
    </Box>
  );

  const renderDatabaseConnection = () => (
    <Box>
      <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
        Database Connections
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Connect to SQL and NoSQL databases with secure credentials.
      </Typography>

      <Card>
        <CardContent>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Database Type</InputLabel>
                <Select defaultValue="" label="Database Type">
                  <MenuItem value="mysql">MySQL</MenuItem>
                  <MenuItem value="postgresql">PostgreSQL</MenuItem>
                  <MenuItem value="mongodb">MongoDB</MenuItem>
                  <MenuItem value="sqlserver">SQL Server</MenuItem>
                  <MenuItem value="oracle">Oracle</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <TextField fullWidth label="Host" placeholder="localhost or IP address" />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField fullWidth label="Port" placeholder="3306" />
            </Grid>
            
            <Grid item xs={12}>
              <TextField fullWidth label="Database Name" />
            </Grid>
            
            <Grid item xs={12} md={6}>
              <TextField fullWidth label="Username" />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField fullWidth label="Password" type="password" />
            </Grid>
            
            <Grid item xs={12}>
              <Button variant="contained" fullWidth size="large" startIcon={<Storage />}>
                Test & Connect
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    </Box>
  );

  const renderAPIConnection = () => (
    <Box>
      <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
        API Connections
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Fetch data from REST or GraphQL APIs with authentication.
      </Typography>

      <Card>
        <CardContent>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>API Type</InputLabel>
                <Select defaultValue="rest" label="API Type">
                  <MenuItem value="rest">REST API</MenuItem>
                  <MenuItem value="graphql">GraphQL</MenuItem>
                  <MenuItem value="soap">SOAP</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Endpoint URL"
                placeholder="https://api.example.com/data"
              />
            </Grid>
            
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Method</InputLabel>
                <Select defaultValue="GET" label="Method">
                  <MenuItem value="GET">GET</MenuItem>
                  <MenuItem value="POST">POST</MenuItem>
                  <MenuItem value="PUT">PUT</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Authentication</InputLabel>
                <Select defaultValue="none" label="Authentication">
                  <MenuItem value="none">None</MenuItem>
                  <MenuItem value="basic">Basic Auth</MenuItem>
                  <MenuItem value="bearer">Bearer Token</MenuItem>
                  <MenuItem value="apikey">API Key</MenuItem>
                  <MenuItem value="oauth">OAuth 2.0</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Headers (JSON)"
                multiline
                rows={3}
                placeholder='{"Authorization": "Bearer token"}'
              />
            </Grid>
            
            <Grid item xs={12}>
              <Button variant="contained" fullWidth size="large" startIcon={<Api />}>
                Test & Connect
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    </Box>
  );

  const renderCloudStorage = () => (
    <Box>
      <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
        Cloud Storage
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Connect to AWS S3, Google Cloud, Azure, or other cloud storage.
      </Typography>

      <Grid container spacing={2}>
        {['AWS S3', 'Google Cloud Storage', 'Azure Blob', 'Dropbox'].map((provider) => (
          <Grid item xs={12} sm={6} key={provider}>
            <Card sx={{ cursor: 'pointer', '&:hover': { borderColor: 'primary.main' } }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Cloud sx={{ fontSize: 40, color: 'primary.main', mr: 2 }} />
                  <Typography variant="h6">{provider}</Typography>
                </Box>
                <Button variant="outlined" fullWidth>
                  Connect {provider}
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );

  const renderStreaming = () => (
    <Box>
      <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
        Real-Time Data Streams
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Connect to Kafka, logs, IoT devices, and other streaming sources.
      </Typography>

      <Alert severity="info" sx={{ mb: 3 }}>
        Real-time streaming requires advanced configuration. Contact support for setup assistance.
      </Alert>

      <Card>
        <CardContent>
          <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 600 }}>
            Available Connectors
          </Typography>
          <List>
            {['Apache Kafka', 'RabbitMQ', 'MQTT', 'WebSocket', 'Server Logs', 'IoT Devices'].map((source) => (
              <ListItem key={source}>
                <ListItemText primary={source} secondary="Configuration required" />
                <Button size="small">Configure</Button>
              </ListItem>
            ))}
          </List>
        </CardContent>
      </Card>
    </Box>
  );

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ fontWeight: 700, mb: 1 }}>
        Multi-Source Data Ingestion
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        Connect to any data source with auto-schema detection and type inference
      </Typography>

      {/* Source Selection Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {dataSources.map((source, index) => (
          <Grid item xs={12} sm={6} md={2.4} key={source.id}>
            <Card
              sx={{
                cursor: 'pointer',
                border: 2,
                borderColor: activeSource === index ? source.color : 'transparent',
                transition: 'all 0.3s',
                '&:hover': { borderColor: source.color, transform: 'translateY(-4px)' }
              }}
              onClick={() => setActiveSource(index)}
            >
              <CardContent sx={{ textAlign: 'center', py: 3 }}>
                <Box sx={{
                  bgcolor: `${source.color}15`,
                  width: 60,
                  height: 60,
                  borderRadius: 3,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  mx: 'auto',
                  mb: 2
                }}>
                  {React.cloneElement(source.icon, { sx: { fontSize: 32, color: source.color } })}
                </Box>
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
                  {source.name}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {source.supported.length} sources
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Active Connections */}
      {connections.length > 0 && (
        <Card sx={{ mb: 4, bgcolor: 'success.light', color: 'success.contrastText' }}>
          <CardContent>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <CheckCircle /> Active Connections ({connections.length})
            </Typography>
            <Grid container spacing={2}>
              {connections.map((conn) => (
                <Grid item xs={12} sm={6} md={4} key={conn.id}>
                  <Card>
                    <CardContent>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                        <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                          {conn.name}
                        </Typography>
                        <IconButton size="small" onClick={() => setConnections(connections.filter(c => c.id !== conn.id))}>
                          <Delete fontSize="small" />
                        </IconButton>
                      </Box>
                      <Typography variant="caption" display="block">
                        {conn.rows} rows × {conn.columns} columns
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {conn.timestamp}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </CardContent>
        </Card>
      )}

      {/* Configuration Panel */}
      <Card>
        <CardContent sx={{ p: 4 }}>
          {activeSource === 0 && renderFileUpload()}
          {activeSource === 1 && renderDatabaseConnection()}
          {activeSource === 2 && renderAPIConnection()}
          {activeSource === 3 && renderCloudStorage()}
          {activeSource === 4 && renderStreaming()}
        </CardContent>
      </Card>

      {loading && <LinearProgress sx={{ mt: 2 }} />}
    </Box>
  );
}

export default MultiSourceDataIngestion;