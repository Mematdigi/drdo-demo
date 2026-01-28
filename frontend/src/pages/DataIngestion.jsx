import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Tabs,
  Tab,
  TextField,
  Grid,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  IconButton,
  Stepper,
  Step,
  StepLabel,
} from '@mui/material';
import {
  CloudUpload,
  Api,
  Edit,
  Download,
  Check,
  Error as ErrorIcon,
  Info,
  Visibility,
  TableChart,
} from '@mui/icons-material';

const DataIngestion = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [uploadResult, setUploadResult] = useState(null);
  const [validationErrors, setValidationErrors] = useState([]);
  const [previewData, setPreviewData] = useState([]);
  const [showPreview, setShowPreview] = useState(false);
  const [activeStep, setActiveStep] = useState(0);

  // Data templates
  const dataTemplates = {
    incident: {
      name: 'Fire Incident Data',
      requiredFields: [
        'incident_number', 'timestamp', 'state', 'district', 'city',
        'incident_type', 'severity', 'response_time_minutes'
      ],
      optionalFields: [
        'location', 'latitude', 'longitude', 'casualties', 'injuries',
        'property_damage_inr', 'station_id', 'vehicles_deployed',
        'personnel_count', 'cause', 'remarks'
      ],
      sampleData: {
        incident_number: 'INC-2024-001',
        timestamp: '2024-01-15T14:30:00',
        state: 'Maharashtra',
        district: 'Mumbai',
        city: 'Mumbai',
        incident_type: 'Building Fire',
        severity: 'High',
        response_time_minutes: 12,
        casualties: 0,
        injuries: 2,
        property_damage_inr: 500000
      }
    },
    vendor: {
      name: 'Vendor Data',
      requiredFields: [
        'vendor_name', 'vendor_type', 'contact_person', 'phone', 'email'
      ],
      optionalFields: [
        'registration_no', 'address', 'contract_id', 'contract_start_date',
        'contract_end_date', 'contract_value_inr', 'performance_score'
      ],
      sampleData: {
        vendor_name: 'Fire Equipment Co.',
        vendor_type: 'Equipment Supplier',
        contact_person: 'John Doe',
        phone: '+91-9876543210',
        email: 'john@fireequip.com',
        performance_score: 4.5
      }
    },
    station: {
      name: 'Fire Station Data',
      requiredFields: [
        'station_id', 'station_name', 'state', 'city'
      ],
      optionalFields: [
        'address', 'latitude', 'longitude', 'personnel_count',
        'vehicles', 'established_year', 'coverage_area_sqkm'
      ],
      sampleData: {
        station_id: 'FS-001',
        station_name: 'Central Fire Station',
        state: 'Delhi',
        city: 'New Delhi',
        personnel_count: 50,
        vehicles: 10
      }
    }
  };

  const [selectedTemplate, setSelectedTemplate] = useState('incident');

  // File upload handler
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setActiveStep(1);
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('template', selectedTemplate);

    try {
      const response = await fetch('http://localhost:3001/api/data/ingest', {
        method: 'POST',
        body: formData,
      });
      
      const result = await response.json();
      
      if (result.success) {
        setUploadResult(result);
        setPreviewData(result.preview || []);
        setValidationErrors(result.validationErrors || []);
        setActiveStep(2);
        
        if (result.validationErrors && result.validationErrors.length > 0) {
          setShowPreview(true);
        }
      } else {
        setUploadResult({ success: false, error: result.error });
        setActiveStep(0);
      }
    } catch (error) {
      setUploadResult({ success: false, error: error.message });
      setActiveStep(0);
    }
  };

  // Download template
  const downloadTemplate = (templateType) => {
    const template = dataTemplates[templateType];
    const headers = [...template.requiredFields, ...template.optionalFields];
    const sampleRow = template.sampleData;
    
    let csv = headers.join(',') + '\n';
    csv += headers.map(h => sampleRow[h] || '').join(',');
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${templateType}_template.csv`;
    a.click();
  };

  const steps = ['Select Template', 'Upload Data', 'Review & Validate'];

  return (
    <Box>
      {/* Header */}
      <Typography variant="h4" gutterBottom sx={{ mb: 3 }}>
        📥 Data Ingestion Portal
      </Typography>

      {/* Stepper */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Stepper activeStep={activeStep}>
            {steps.map((label) => (
              <Step key={label}>
                <StepLabel>{label}</StepLabel>
              </Step>
            ))}
          </Stepper>
        </CardContent>
      </Card>

      {/* Template Selection */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Step 1: Select Data Template
              </Typography>
              <FormControl fullWidth sx={{ mt: 2 }}>
                <InputLabel>Data Type</InputLabel>
                <Select
                  value={selectedTemplate}
                  onChange={(e) => setSelectedTemplate(e.target.value)}
                  label="Data Type"
                >
                  {Object.keys(dataTemplates).map((key) => (
                    <MenuItem key={key} value={key}>
                      {dataTemplates[key].name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              <Box sx={{ mt: 3 }}>
                <Typography variant="subtitle2" gutterBottom>
                  <strong>Required Fields:</strong>
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                  {dataTemplates[selectedTemplate].requiredFields.map((field) => (
                    <Chip key={field} label={field} color="error" size="small" />
                  ))}
                </Box>

                <Typography variant="subtitle2" gutterBottom>
                  <strong>Optional Fields:</strong>
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {dataTemplates[selectedTemplate].optionalFields.map((field) => (
                    <Chip key={field} label={field} size="small" />
                  ))}
                </Box>
              </Box>

              <Button
                variant="outlined"
                startIcon={<Download />}
                onClick={() => downloadTemplate(selectedTemplate)}
                sx={{ mt: 2 }}
              >
                Download Template (CSV)
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Main Tabs */}
      <Card>
        <Tabs value={activeTab} onChange={(e, v) => setActiveTab(v)}>
          <Tab icon={<CloudUpload />} label="File Upload" />
          <Tab icon={<Api />} label="API Integration" />
          <Tab icon={<Edit />} label="Manual Entry" />
          <Tab icon={<TableChart />} label="Bulk Import" />
        </Tabs>

        <CardContent>
          {/* Tab 0: File Upload */}
          {activeTab === 0 && (
            <Box>
              <Alert severity="info" sx={{ mb: 3 }}>
                Upload CSV or Excel files. Data will be validated against the selected template.
              </Alert>

              <Box
                sx={{
                  border: '2px dashed #3b82f6',
                  borderRadius: 2,
                  p: 4,
                  textAlign: 'center',
                  bgcolor: 'rgba(59, 130, 246, 0.05)',
                }}
              >
                <CloudUpload sx={{ fontSize: 60, color: '#3b82f6', mb: 2 }} />
                <Typography variant="h6" gutterBottom>
                  Upload {dataTemplates[selectedTemplate].name}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  Supported: CSV, Excel (.xlsx, .xls)
                </Typography>
                <Button variant="contained" component="label">
                  Choose File
                  <input
                    type="file"
                    hidden
                    accept=".csv,.xlsx,.xls"
                    onChange={handleFileUpload}
                  />
                </Button>
              </Box>

              {/* Upload Result */}
              {uploadResult && (
                <Alert
                  severity={uploadResult.success ? 'success' : 'error'}
                  sx={{ mt: 3 }}
                  action={
                    uploadResult.success && previewData.length > 0 && (
                      <Button
                        color="inherit"
                        size="small"
                        onClick={() => setShowPreview(true)}
                        startIcon={<Visibility />}
                      >
                        Preview
                      </Button>
                    )
                  }
                >
                  {uploadResult.success ? (
                    <Box>
                      <Typography variant="body1" gutterBottom>
                        <strong>✅ Upload Successful!</strong>
                      </Typography>
                      <Typography variant="body2">
                        • Records processed: {uploadResult.recordsProcessed}
                      </Typography>
                      <Typography variant="body2">
                        • Valid records: {uploadResult.validRecords}
                      </Typography>
                      <Typography variant="body2">
                        • Invalid records: {uploadResult.invalidRecords}
                      </Typography>
                    </Box>
                  ) : (
                    <Box>
                      <Typography variant="body1" gutterBottom>
                        <strong>❌ Upload Failed</strong>
                      </Typography>
                      <Typography variant="body2">{uploadResult.error}</Typography>
                    </Box>
                  )}
                </Alert>
              )}

              {/* Validation Errors */}
              {validationErrors.length > 0 && (
                <Card sx={{ mt: 3, bgcolor: '#fff3cd' }}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom color="warning.dark">
                      ⚠️ Validation Issues ({validationErrors.length})
                    </Typography>
                    <TableContainer component={Paper} sx={{ maxHeight: 300 }}>
                      <Table size="small">
                        <TableHead>
                          <TableRow>
                            <TableCell>Row</TableCell>
                            <TableCell>Field</TableCell>
                            <TableCell>Error</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {validationErrors.slice(0, 10).map((error, idx) => (
                            <TableRow key={idx}>
                              <TableCell>{error.row}</TableCell>
                              <TableCell>{error.field}</TableCell>
                              <TableCell>{error.message}</TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </TableContainer>
                    {validationErrors.length > 10 && (
                      <Typography variant="caption" sx={{ mt: 1 }}>
                        Showing first 10 of {validationErrors.length} errors
                      </Typography>
                    )}
                  </CardContent>
                </Card>
              )}
            </Box>
          )}

          {/* Tab 1: API Integration */}
          {activeTab === 1 && (
            <Box>
              <Alert severity="info" sx={{ mb: 3 }}>
                Integrate with external systems via REST API
              </Alert>

              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="API Endpoint URL"
                    placeholder="https://api.example.com/data"
                    helperText="Enter the API endpoint to fetch data"
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <FormControl fullWidth>
                    <InputLabel>Method</InputLabel>
                    <Select defaultValue="GET" label="Method">
                      <MenuItem value="GET">GET</MenuItem>
                      <MenuItem value="POST">POST</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={12} md={6}>
                  <FormControl fullWidth>
                    <InputLabel>Authentication</InputLabel>
                    <Select defaultValue="none" label="Authentication">
                      <MenuItem value="none">None</MenuItem>
                      <MenuItem value="bearer">Bearer Token</MenuItem>
                      <MenuItem value="basic">Basic Auth</MenuItem>
                      <MenuItem value="api_key">API Key</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Headers (JSON)"
                    multiline
                    rows={4}
                    placeholder='{"Authorization": "Bearer token"}'
                  />
                </Grid>
                <Grid item xs={12}>
                  <Button variant="contained" startIcon={<Api />}>
                    Test Connection
                  </Button>
                  <Button variant="outlined" sx={{ ml: 2 }}>
                    Import Data
                  </Button>
                </Grid>
              </Grid>
            </Box>
          )}

          {/* Tab 2: Manual Entry */}
          {activeTab === 2 && (
            <Box>
              <Alert severity="info" sx={{ mb: 3 }}>
                Manually enter single records
              </Alert>
              <Grid container spacing={2}>
                {dataTemplates[selectedTemplate].requiredFields.map((field) => (
                  <Grid item xs={12} md={6} key={field}>
                    <TextField
                      fullWidth
                      required
                      label={field.replace(/_/g, ' ').toUpperCase()}
                      placeholder={`Enter ${field}`}
                    />
                  </Grid>
                ))}
                {dataTemplates[selectedTemplate].optionalFields.slice(0, 4).map((field) => (
                  <Grid item xs={12} md={6} key={field}>
                    <TextField
                      fullWidth
                      label={field.replace(/_/g, ' ').toUpperCase()}
                      placeholder={`Enter ${field} (optional)`}
                    />
                  </Grid>
                ))}
              </Grid>
              <Button variant="contained" sx={{ mt: 3 }} startIcon={<Check />}>
                Submit Record
              </Button>
            </Box>
          )}

          {/* Tab 3: Bulk Import */}
          {activeTab === 3 && (
            <Box>
              <Alert severity="info" sx={{ mb: 3 }}>
                Import large datasets with advanced options
              </Alert>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <FormControl fullWidth>
                    <InputLabel>Import Mode</InputLabel>
                    <Select defaultValue="append" label="Import Mode">
                      <MenuItem value="append">Append (Add new records)</MenuItem>
                      <MenuItem value="replace">Replace (Delete existing)</MenuItem>
                      <MenuItem value="update">Update (Merge with existing)</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField fullWidth type="number" label="Batch Size" defaultValue={1000} />
                </Grid>
                <Grid item xs={12} md={6}>
                  <FormControl fullWidth>
                    <InputLabel>Error Handling</InputLabel>
                    <Select defaultValue="skip" label="Error Handling">
                      <MenuItem value="skip">Skip invalid records</MenuItem>
                      <MenuItem value="stop">Stop on first error</MenuItem>
                      <MenuItem value="warn">Continue with warnings</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
              </Grid>
              <Button variant="contained" component="label" sx={{ mt: 3 }}>
                Select File for Bulk Import
                <input type="file" hidden accept=".csv,.xlsx" />
              </Button>
            </Box>
          )}
        </CardContent>
      </Card>

      {/* Preview Dialog */}
      <Dialog open={showPreview} onClose={() => setShowPreview(false)} maxWidth="lg" fullWidth>
        <DialogTitle>Data Preview</DialogTitle>
        <DialogContent>
          <TableContainer>
            <Table size="small">
              <TableHead>
                <TableRow>
                  {previewData[0] && Object.keys(previewData[0]).map((key) => (
                    <TableCell key={key}><strong>{key}</strong></TableCell>
                  ))}
                </TableRow>
              </TableHead>
              <TableBody>
                {previewData.map((row, idx) => (
                  <TableRow key={idx}>
                    {Object.values(row).map((val, i) => (
                      <TableCell key={i}>{String(val)}</TableCell>
                    ))}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowPreview(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default DataIngestion;