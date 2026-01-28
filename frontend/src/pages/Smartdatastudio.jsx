import React, { useState } from 'react';
import {
  Box, Card, CardContent, Typography, Button, Stepper, Step, StepLabel,
  Alert, Grid, CircularProgress, Select, MenuItem, FormControl, InputLabel,
  TextField, Chip, Table, TableBody, TableCell, TableContainer, TableHead,
  TableRow, Paper, Tabs, Tab, Dialog, DialogTitle, DialogContent, DialogActions
} from '@mui/material';
import {
  CloudUpload, AutoAwesome, BarChart as BarChartIcon, PieChart as PieChartIcon,
  Timeline, ScatterPlot, Assessment
} from '@mui/icons-material';
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, ScatterChart, Scatter,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell
} from 'recharts';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

const SmartDataStudio = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [dataSummary, setDataSummary] = useState(null);
  const [vizSuggestions, setVizSuggestions] = useState([]);
  const [selectedVisualizations, setSelectedVisualizations] = useState([]);
  const [visualizationData, setVisualizationData] = useState({});
  const [cleaningReport, setCleaningReport] = useState([]);

  const steps = ['Upload Data', 'Review & Clean', 'Build Visualizations', 'Generate Report'];

  // Step 1: Upload file
  const handleFileUpload = async (event) => {
    const uploadedFile = event.target.files[0];
    if (!uploadedFile) return;

    setFile(uploadedFile);
    setUploading(true);

    const formData = new FormData();
    formData.append('file', uploadedFile);

    try {
      const response = await fetch('http://localhost:3001/api/smart/analyze', {
        method: 'POST',
        body: formData
      });

      const result = await response.json();

      if (result.success) {
        setDataSummary(result.summary);
        setVizSuggestions(result.visualization_suggestions);
        setCleaningReport(result.summary.cleaning_report);
        setActiveStep(1);
      } else {
        alert('Error analyzing data: ' + result.error);
      }
    } catch (error) {
      alert('Upload failed: ' + error.message);
    } finally {
      setUploading(false);
    }
  };

  // Step 2: Add visualization
  const addVisualization = async (vizConfig) => {
    try {
      const response = await fetch('http://localhost:3001/api/smart/prepare-viz', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          filename: file.name,
          viz_config: vizConfig
        })
      });

      const result = await response.json();

      if (result.success) {
        const vizId = `viz_${selectedVisualizations.length}`;
        setSelectedVisualizations([...selectedVisualizations, { ...vizConfig, id: vizId }]);
        setVisualizationData({ ...visualizationData, [vizId]: result.data });
      }
    } catch (error) {
      console.error('Error preparing visualization:', error);
    }
  };

  // Render visualization based on type
  const renderVisualization = (viz) => {
    const data = visualizationData[viz.id];
    if (!data) return <CircularProgress />;

    switch (viz.type) {
      case 'bar':
        return (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={viz.x} angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        );

      case 'line':
        return (
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={viz.x} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey={viz.y} stroke="#3b82f6" />
            </LineChart>
          </ResponsiveContainer>
        );

      case 'pie':
        return (
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={data} dataKey="value" nameKey="category" cx="50%" cy="50%" outerRadius={100} label>
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        );

      case 'scatter':
        return (
          <ResponsiveContainer width="100%" height={300}>
            <ScatterChart>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={viz.x} name={viz.x} />
              <YAxis dataKey={viz.y} name={viz.y} />
              <Tooltip cursor={{ strokeDasharray: '3 3' }} />
              <Scatter data={data} fill="#3b82f6" />
            </ScatterChart>
          </ResponsiveContainer>
        );

      default:
        return <Typography>Unsupported visualization type</Typography>;
    }
  };

  // Generate report
  const generateReport = async () => {
    try {
      const response = await fetch('http://localhost:3001/api/smart/generate-report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          filename: file.name,
          summary: dataSummary,
          visualizations: selectedVisualizations
        }),
        responseType: 'blob'
      });

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Smart_Report_${Date.now()}.pdf`;
      a.click();
    } catch (error) {
      console.error('Error generating report:', error);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ mb: 3 }}>
        🤖 Smart Data Studio
      </Typography>

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

      {/* Step 1: Upload */}
      {activeStep === 0 && (
        <Card>
          <CardContent>
            <Alert severity="info" sx={{ mb: 3 }}>
              <strong>Upload ANY data file</strong> - Our AI will analyze, clean, and suggest visualizations automatically!
            </Alert>

            <Box sx={{
              border: '2px dashed #3b82f6',
              borderRadius: 2,
              p: 6,
              textAlign: 'center',
              bgcolor: 'rgba(59, 130, 246, 0.05)'
            }}>
              <CloudUpload sx={{ fontSize: 80, color: '#3b82f6', mb: 2 }} />
              <Typography variant="h5" gutterBottom>Drop Your Data File Here</Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                CSV or Excel • Any columns • Any format • We'll handle it!
              </Typography>
              
              <Button variant="contained" component="label" disabled={uploading} size="large">
                {uploading ? <CircularProgress size={24} /> : 'Choose File'}
                <input type="file" hidden accept=".csv,.xlsx,.xls" onChange={handleFileUpload} />
              </Button>
            </Box>
          </CardContent>
        </Card>
      )}

      {/* Step 2: Review & Clean */}
      {activeStep === 1 && dataSummary && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>📊 Data Summary</Typography>
                <Table size="small">
                  <TableBody>
                    <TableRow>
                      <TableCell><strong>Total Rows</strong></TableCell>
                      <TableCell>{dataSummary.total_rows.toLocaleString()}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><strong>Total Columns</strong></TableCell>
                      <TableCell>{dataSummary.total_columns}</TableCell>
                    </TableRow>
                  </TableBody>
                </Table>

                <Typography variant="subtitle2" sx={{ mt: 2, mb: 1 }}><strong>Columns Detected:</strong></Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {Object.keys(dataSummary.columns).map(col => (
                    <Chip
                      key={col}
                      label={`${col} (${dataSummary.columns[col].detected_type})`}
                      size="small"
                      color={dataSummary.columns[col].detected_type === 'numeric' ? 'primary' : 'default'}
                    />
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>🧹 Cleaning Report</Typography>
                <Box sx={{ maxHeight: 300, overflow: 'auto' }}>
                  {cleaningReport.map((report, idx) => (
                    <Alert key={idx} severity="info" sx={{ mb: 1 }}>
                      {report}
                    </Alert>
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>👀 Data Preview (First 10 Rows)</Typography>
                <TableContainer sx={{ maxHeight: 400 }}>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        {dataSummary.data_preview[0] && Object.keys(dataSummary.data_preview[0]).map(key => (
                          <TableCell key={key}><strong>{key}</strong></TableCell>
                        ))}
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {dataSummary.data_preview.map((row, idx) => (
                        <TableRow key={idx}>
                          {Object.values(row).map((val, i) => (
                            <TableCell key={i}>{String(val)}</TableCell>
                          ))}
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>

                <Box sx={{ mt: 3, textAlign: 'right' }}>
                  <Button variant="contained" onClick={() => setActiveStep(2)} startIcon={<AutoAwesome />}>
                    Continue to Visualizations
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Step 3: Build Visualizations */}
      {activeStep === 2 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>💡 AI Suggestions</Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  Click to add visualizations to your report
                </Typography>

                {vizSuggestions.map((viz, idx) => (
                  <Card key={idx} sx={{ mb: 2, cursor: 'pointer', '&:hover': { bgcolor: 'action.hover' } }}
                    onClick={() => addVisualization(viz)}>
                    <CardContent>
                      <Typography variant="subtitle2">{viz.title}</Typography>
                      <Typography variant="caption" color="text.secondary">{viz.description}</Typography>
                      <Chip label={viz.type} size="small" sx={{ mt: 1 }} />
                    </CardContent>
                  </Card>
                ))}
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  📊 Selected Visualizations ({selectedVisualizations.length})
                </Typography>

                {selectedVisualizations.length === 0 && (
                  <Alert severity="info">
                    Click on suggestions to add visualizations
                  </Alert>
                )}

                {selectedVisualizations.map((viz) => (
                  <Card key={viz.id} sx={{ mb: 3 }}>
                    <CardContent>
                      <Typography variant="h6">{viz.title}</Typography>
                      {renderVisualization(viz)}
                    </CardContent>
                  </Card>
                ))}

                {selectedVisualizations.length > 0 && (
                  <Button variant="contained" onClick={() => setActiveStep(3)} fullWidth>
                    Continue to Report Generation
                  </Button>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Step 4: Generate Report */}
      {activeStep === 3 && (
        <Card>
          <CardContent sx={{ textAlign: 'center', py: 6 }}>
            <Assessment sx={{ fontSize: 80, color: '#10b981', mb: 2 }} />
            <Typography variant="h5" gutterBottom>Your Custom Report is Ready!</Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
              Report includes your data summary, cleaning report, and {selectedVisualizations.length} custom visualizations
            </Typography>

            <Button variant="contained" size="large" onClick={generateReport} sx={{ mr: 2 }}>
              Download PDF Report
            </Button>
            <Button variant="outlined" size="large" onClick={() => setActiveStep(0)}>
              Start New Analysis
            </Button>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default SmartDataStudio;