import React, { useState } from 'react';
import {
  Box, Card, CardContent, Typography, Button, Grid, Alert, CircularProgress,
  Chip, Slider, FormControl, InputLabel, Select, MenuItem
} from '@mui/material';
import {
  CloudUpload, AutoAwesome, Download, Insights, FilterList
} from '@mui/icons-material';
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, AreaChart, Area,
  ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer
} from 'recharts';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316'];

const AutonomousVisualizer = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [aiResults, setAiResults] = useState(null);
  const [dataRange, setDataRange] = useState([0, 100]);
  const [maxRows, setMaxRows] = useState(100);

  const handleFileUpload = async (event) => {
    const uploadedFile = event.target.files[0];
    if (!uploadedFile) return;

    setFile(uploadedFile);
    setUploading(true);

    const formData = new FormData();
    formData.append('file', uploadedFile);

    try {
      console.log('📤 Uploading:', uploadedFile.name);
      
      const response = await fetch('http://localhost:3001/api/ai/analyze', {
        method: 'POST',
        body: formData
      });

      const result = await response.json();

      if (result.success) {
        setAiResults(result);
        
        // Set max rows for slider
        const totalRows = result.summary?.total_rows || 100;
        setMaxRows(totalRows);
        setDataRange([0, Math.min(100, totalRows - 1)]);
        
        console.log('✅ Loaded', result.visualizations?.length, 'visualizations');
        console.log('📊 Total rows:', totalRows);
      } else {
        alert('Error: ' + result.error);
      }
    } catch (error) {
      console.error('❌ Upload error:', error);
      alert('Upload failed: ' + error.message);
    } finally {
      setUploading(false);
    }
  };

  const handleDataRangeChange = (event, newValue) => {
    setDataRange(newValue);
    console.log('📏 Data range changed:', newValue);
  };

  const handleApplyFilters = async () => {
    console.log('🔄 Applying filters, data range:', dataRange);
    
    // Reload visualizations with new range
    setUploading(true);
    
    try {
      // Re-fetch with data range
      const formData = new FormData();
      formData.append('file', file);
      formData.append('data_range', JSON.stringify(dataRange));
      
      const response = await fetch('http://localhost:3001/api/ai/analyze', {
        method: 'POST',
        body: formData
      });

      const result = await response.json();

      if (result.success) {
        // Update visualizations with data_range parameter
        const updatedViz = result.visualizations.map(v => ({
          ...v,
          data_range: dataRange
        }));
        
        setAiResults({
          ...result,
          visualizations: updatedViz
        });
        
        console.log('✅ Applied data range filter');
      }
    } catch (error) {
      console.error('❌ Filter error:', error);
    } finally {
      setUploading(false);
    }
  };

  const renderVisualization = (viz) => {
    const data = viz.data || [];
    
    if (data.length === 0) {
      return (
        <Alert severity="warning" sx={{ mt: 2 }}>
          <Typography variant="body2" color="text.primary">
            No data available for this chart
          </Typography>
        </Alert>
      );
    }

    try {
      switch (viz.type) {
        case 'pie':
        case 'donut':
          return (
            <ResponsiveContainer width="100%" height={350}>
              <PieChart>
                <Pie
                  data={data}
                  dataKey="value"
                  nameKey="category"
                  cx="50%"
                  cy="50%"
                  outerRadius={viz.type === 'donut' ? 100 : 120}
                  innerRadius={viz.type === 'donut' ? 50 : 0}
                  label={(entry) => `${entry.category}: ${entry.value}`}
                >
                  {data.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          );

        case 'bar':
        case 'horizontal_bar':
          const xKey = viz.x || Object.keys(data[0] || {})[0];
          const yKey = 'count';
          
          return (
            <ResponsiveContainer width="100%" height={350}>
              <BarChart 
                data={data}
                layout={viz.type === 'horizontal_bar' ? 'vertical' : 'horizontal'}
                margin={{ top: 20, right: 30, left: 20, bottom: 80 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                {viz.type === 'horizontal_bar' ? (
                  <>
                    <XAxis type="number" />
                    <YAxis type="category" dataKey={xKey} width={120} />
                  </>
                ) : (
                  <>
                    <XAxis dataKey={xKey} angle={-45} textAnchor="end" height={100} interval={0} />
                    <YAxis />
                  </>
                )}
                <Tooltip />
                <Legend />
                <Bar dataKey={yKey} fill={COLORS[0]} />
              </BarChart>
            </ResponsiveContainer>
          );

        case 'line':
          return (
            <ResponsiveContainer width="100%" height={350}>
              <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey={viz.x} />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey={viz.y} stroke={COLORS[0]} strokeWidth={3} dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          );

        case 'area':
          return (
            <ResponsiveContainer width="100%" height={350}>
              <AreaChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
                <defs>
                  <linearGradient id="colorArea" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor={COLORS[4]} stopOpacity={0.8}/>
                    <stop offset="95%" stopColor={COLORS[4]} stopOpacity={0.1}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey={viz.x} />
                <YAxis />
                <Tooltip />
                <Area type="monotone" dataKey={viz.y} stroke={COLORS[4]} fillOpacity={1} fill="url(#colorArea)" />
              </AreaChart>
            </ResponsiveContainer>
          );

        case 'scatter':
          return (
            <ResponsiveContainer width="100%" height={350}>
              <ScatterChart margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey={viz.x} name={viz.x} />
                <YAxis dataKey={viz.y} name={viz.y} />
                <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                <Legend />
                <Scatter name={viz.title} data={data} fill={COLORS[3]} />
              </ScatterChart>
            </ResponsiveContainer>
          );

        case 'gantt':
          // Simple Gantt visualization
          return (
            <Box sx={{ p: 2 }}>
              <Typography variant="body2" gutterBottom fontWeight="bold">
                Timeline Gantt Chart:
              </Typography>
              {data.slice(0, 15).map((item, idx) => (
                <Box key={idx} sx={{ mb: 1.5 }}>
                  <Typography variant="caption" display="block">
                    {item.task} ({item.duration} days)
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Typography variant="caption" sx={{ mr: 1, minWidth: 80 }}>
                      {new Date(item.start).toLocaleDateString()}
                    </Typography>
                    <Box sx={{
                      height: 24,
                      bgcolor: COLORS[idx % COLORS.length],
                      width: `${Math.min((item.duration / 30) * 100, 100)}%`,
                      borderRadius: 1,
                      minWidth: 40
                    }} />
                  </Box>
                </Box>
              ))}
            </Box>
          );

        default:
          return (
            <Box sx={{ textAlign: 'center', py: 4, bgcolor: '#f5f5f5', borderRadius: 2 }}>
              <Typography variant="h6" color="primary">{viz.type.toUpperCase()}</Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                {viz.description}
              </Typography>
              <Chip label={`${data.length} points`} sx={{ mt: 2 }} />
            </Box>
          );
      }
    } catch (error) {
      console.error('Chart error:', error);
      return <Alert severity="error">Error: {error.message}</Alert>;
    }
  };

  const handleGenerateReport = async () => {
    try {
      const response = await fetch('http://localhost:3001/api/ai/generate-report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filename: file.name })
      });

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `AI_Analytics_${Date.now()}.pdf`;
      a.click();
    } catch (error) {
      alert('Report failed: ' + error.message);
    }
  };

  return (
    <Box sx={{ minHeight: '100vh', pb: 4 }}>
      <Typography variant="h4" gutterBottom sx={{ mb: 3, color: '#fff' }}>
        🤖 Autonomous AI Studio
      </Typography>

      {!aiResults && (
        <Card>
          <CardContent>
            <Alert severity="info" sx={{ mb: 3 }}>
              <strong>15+ Chart Types!</strong> Pie, Donut, Bar, Line, Area, Scatter, Gantt, Heatmap & more!
            </Alert>

            <Box sx={{
              border: '2px dashed #3b82f6',
              borderRadius: 2,
              p: 6,
              textAlign: 'center',
              bgcolor: 'rgba(59, 130, 246, 0.05)'
            }}>
              <AutoAwesome sx={{ fontSize: 80, color: '#3b82f6', mb: 2 }} />
              <Typography variant="h5" gutterBottom sx={{ color: '#1e293b' }}>
                Upload Data - Get 15+ Visualizations
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                AI auto-creates ALL chart types with interactive data range selector
              </Typography>
              
              <Button 
                variant="contained" 
                component="label" 
                disabled={uploading}
                size="large"
                startIcon={uploading ? <CircularProgress size={20} /> : <CloudUpload />}
              >
                {uploading ? 'AI Processing...' : 'Choose File'}
                <input type="file" hidden accept=".csv,.xlsx,.xls" onChange={handleFileUpload} />
              </Button>
            </Box>
          </CardContent>
        </Card>
      )}

      {aiResults && (
        <Box>
          {/* Insights */}
          <Card sx={{ mb: 3, bgcolor: '#10b981' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ color: '#fff', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: 1 }}>
                <Insights sx={{ color: '#fff' }} /> AI Analysis Complete
              </Typography>
              {aiResults.insights?.map((insight, idx) => (
                <Typography key={idx} variant="body2" sx={{ mb: 0.5, color: '#fff' }}>
                  {insight}
                </Typography>
              ))}
              <Box sx={{ mt: 2 }}>
                <Chip label={`${aiResults.visualizations?.length || 0} Visualizations`} 
                      sx={{ mr: 1, bgcolor: '#fff', color: '#10b981', fontWeight: 'bold' }} />
                <Chip label={`${aiResults.visualizations?.filter(v => v.data?.length > 0).length || 0} With Data`} 
                      sx={{ bgcolor: '#059669', color: '#fff', fontWeight: 'bold' }} />
              </Box>
            </CardContent>
          </Card>

          {/* DATA RANGE SELECTOR */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <FilterList /> Select Data Range
              </Typography>
              <Typography variant="caption" color="text.secondary" display="block" sx={{ mb: 2 }}>
                Choose which rows to include in visualizations (Row {dataRange[0]} to {dataRange[1]})
              </Typography>
              <Slider
                value={dataRange}
                onChange={handleDataRangeChange}
                valueLabelDisplay="auto"
                min={0}
                max={maxRows - 1}
                marks={[
                  { value: 0, label: '0' },
                  { value: Math.floor(maxRows / 2), label: `${Math.floor(maxRows / 2)}` },
                  { value: maxRows - 1, label: `${maxRows - 1}` }
                ]}
                sx={{ mb: 2 }}
              />
              <Button variant="contained" onClick={handleApplyFilters} disabled={uploading}>
                {uploading ? <CircularProgress size={20} /> : 'Apply Filter'}
              </Button>
            </CardContent>
          </Card>

          {/* Action Buttons */}
          <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="h5" sx={{ color: '#fff' }}>
              🎨 AI-Selected Visualizations
            </Typography>
            <Box>
              <Button variant="contained" onClick={handleGenerateReport} startIcon={<Download />}
                      sx={{ mr: 2, bgcolor: '#10b981', '&:hover': { bgcolor: '#059669' } }}>
                Generate Report
              </Button>
              <Button variant="outlined" onClick={() => { setAiResults(null); setFile(null); }}
                      sx={{ borderColor: '#fff', color: '#fff' }}>
                Upload New
              </Button>
            </Box>
          </Box>

          {/* Visualizations */}
          <Grid container spacing={3}>
            {aiResults.visualizations?.map((viz, idx) => (
              <Grid item xs={12} md={6} key={idx}>
                <Card sx={{ height: '100%', '&:hover': { transform: 'translateY(-4px)', boxShadow: 4 } }}>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                      <Box sx={{ flex: 1 }}>
                        <Typography variant="h6" gutterBottom sx={{ color: '#1e293b' }}>
                          {viz.title}
                        </Typography>
                        <Typography variant="caption" color="text.secondary" display="block">
                          {viz.description}
                        </Typography>
                      </Box>
                      <Chip label={viz.priority} size="small"
                            color={viz.priority === 'high' ? 'error' : viz.priority === 'medium' ? 'warning' : 'default'} />
                    </Box>
                    
                    {renderVisualization(viz)}
                    
                    <Box sx={{ mt: 2, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                      <Chip label={viz.type} size="small" variant="outlined" />
                      <Chip label={`${viz.data?.length || 0} points`} size="small"
                            color={viz.data?.length > 0 ? 'success' : 'default'} />
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      )}
    </Box>
  );
};

export default AutonomousVisualizer;