import React, { useState, useEffect } from 'react';
import {
  Box, Card, CardContent, Typography, Button, Grid, Alert, CircularProgress,
  Chip, FormControl, InputLabel, Select, MenuItem, Slider, TextField,
  FormGroup, FormControlLabel, Checkbox, Paper
} from '@mui/material';
import {
  CloudUpload, AutoAwesome, Download, FilterList, Insights
} from '@mui/icons-material';
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, AreaChart, Area,
  ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar,
  Treemap, ComposedChart
} from 'recharts';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316'];

const AutonomousVisualizer = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [aiResults, setAiResults] = useState(null);
  const [visualizations, setVisualizations] = useState([]);
  const [vizData, setVizData] = useState({});
  const [filters, setFilters] = useState({});
  const [loading, setLoading] = useState({});

  // Handle file upload
  const handleFileUpload = async (event) => {
    const uploadedFile = event.target.files[0];
    if (!uploadedFile) return;

    setFile(uploadedFile);
    setUploading(true);

    const formData = new FormData();
    formData.append('file', uploadedFile);

    try {
      const response = await fetch('http://localhost:3001/api/ai/analyze', {
        method: 'POST',
        body: formData
      });

      const result = await response.json();

      if (result.success) {
        setAiResults(result);
        setVisualizations(result.visualizations || []);
        
        // Auto-load all high priority visualizations
        loadHighPriorityViz(result.visualizations || [], uploadedFile.name);
      } else {
        alert('Error: ' + result.error);
      }
    } catch (error) {
      alert('Upload failed: ' + error.message);
    } finally {
      setUploading(false);
    }
  };

  // Load high priority visualizations automatically
  const loadHighPriorityViz = async (vizList, filename) => {
    const highPriority = vizList.filter(v => v.priority === 'high').slice(0, 6);
    
    for (const viz of highPriority) {
      await loadVisualization(viz, filename);
    }
  };

  // Load individual visualization
  const loadVisualization = async (viz, filename) => {
    const vizId = `${viz.type}_${viz.title.replace(/\s/g, '_')}`;
    
    setLoading(prev => ({ ...prev, [vizId]: true }));

    try {
      const response = await fetch('http://localhost:3001/api/smart/prepare-viz', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          filename: filename || file.name,
          viz_config: viz
        })
      });

      const result = await response.json();

      if (result.success && result.data) {
        setVizData(prev => ({ ...prev, [vizId]: result.data }));
      }
    } catch (error) {
      console.error('Error loading viz:', error);
    } finally {
      setLoading(prev => ({ ...prev, [vizId]: false }));
    }
  };

  // Render different chart types
  const renderVisualization = (viz) => {
    const vizId = `${viz.type}_${viz.title.replace(/\s/g, '_')}`;
    const data = vizData[vizId];
    const isLoading = loading[vizId];

    if (isLoading) {
      return (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 300 }}>
          <CircularProgress />
        </Box>
      );
    }

    if (!data || (Array.isArray(data) && data.length === 0)) {
      return (
        <Alert severity="info">
          No data available. Click to load this visualization.
        </Alert>
      );
    }

    switch (viz.type) {
      case 'pie':
        return renderPieChart(data, viz);
      
      case 'donut':
        return renderDonutChart(data, viz);
      
      case 'bar':
        return renderBarChart(data, viz);
      
      case 'horizontal_bar':
        return renderHorizontalBarChart(data, viz);
      
      case 'line':
        return renderLineChart(data, viz);
      
      case 'area':
        return renderAreaChart(data, viz);
      
      case 'scatter':
        return renderScatterChart(data, viz);
      
      case 'bubble':
        return renderBubbleChart(data, viz);
      
      case 'stacked_bar':
        return renderStackedBarChart(data, viz);
      
      case 'heatmap':
        return renderHeatmap(data, viz);
      
      case 'radar':
        return renderRadarChart(data, viz);
      
      case 'gantt':
        return renderGanttChart(data, viz);
      
      default:
        return <Typography>Chart type {viz.type} coming soon!</Typography>;
    }
  };

  const renderPieChart = (data, viz) => (
    <ResponsiveContainer width="100%" height={350}>
      <PieChart>
        <Pie
          data={data}
          dataKey="value"
          nameKey="category"
          cx="50%"
          cy="50%"
          outerRadius={120}
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

  const renderDonutChart = (data, viz) => (
    <ResponsiveContainer width="100%" height={350}>
      <PieChart>
        <Pie
          data={data}
          dataKey="value"
          nameKey="category"
          cx="50%"
          cy="50%"
          innerRadius={60}
          outerRadius={120}
          label
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

  const renderBarChart = (data, viz) => (
    <ResponsiveContainer width="100%" height={350}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey={viz.x} angle={-45} textAnchor="end" height={100} />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="count" fill="#3b82f6" />
      </BarChart>
    </ResponsiveContainer>
  );

  const renderHorizontalBarChart = (data, viz) => (
    <ResponsiveContainer width="100%" height={350}>
      <BarChart data={data} layout="horizontal">
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis type="number" />
        <YAxis dataKey={viz.x} type="category" width={150} />
        <Tooltip />
        <Legend />
        <Bar dataKey="count" fill="#10b981" />
      </BarChart>
    </ResponsiveContainer>
  );

  const renderLineChart = (data, viz) => (
    <ResponsiveContainer width="100%" height={350}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey={viz.x} />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey={viz.y} stroke="#3b82f6" strokeWidth={2} />
      </LineChart>
    </ResponsiveContainer>
  );

  const renderAreaChart = (data, viz) => (
    <ResponsiveContainer width="100%" height={350}>
      <AreaChart data={data}>
        <defs>
          <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.8}/>
            <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey={viz.x} />
        <YAxis />
        <Tooltip />
        <Area type="monotone" dataKey={viz.y} stroke="#8b5cf6" fillOpacity={1} fill="url(#colorValue)" />
      </AreaChart>
    </ResponsiveContainer>
  );

  const renderScatterChart = (data, viz) => (
    <ResponsiveContainer width="100%" height={350}>
      <ScatterChart>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey={viz.x} name={viz.x} />
        <YAxis dataKey={viz.y} name={viz.y} />
        <Tooltip cursor={{ strokeDasharray: '3 3' }} />
        <Scatter data={data} fill="#ef4444" />
      </ScatterChart>
    </ResponsiveContainer>
  );

  const renderBubbleChart = (data, viz) => (
    <ResponsiveContainer width="100%" height={350}>
      <ScatterChart>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey={viz.x} name={viz.x} />
        <YAxis dataKey={viz.y} name={viz.y} />
        <Tooltip cursor={{ strokeDasharray: '3 3' }} />
        <Scatter data={data} fill="#ec4899">
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Scatter>
      </ScatterChart>
    </ResponsiveContainer>
  );

  const renderStackedBarChart = (data, viz) => (
    <ResponsiveContainer width="100%" height={350}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey={viz.x} />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="value1" stackId="a" fill="#3b82f6" />
        <Bar dataKey="value2" stackId="a" fill="#10b981" />
        <Bar dataKey="value3" stackId="a" fill="#f59e0b" />
      </BarChart>
    </ResponsiveContainer>
  );

  const renderRadarChart = (data, viz) => (
    <ResponsiveContainer width="100%" height={350}>
      <RadarChart data={data}>
        <PolarGrid />
        <PolarAngleAxis dataKey="subject" />
        <PolarRadiusAxis />
        <Radar name="Value" dataKey="value" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.6} />
        <Legend />
      </RadarChart>
    </ResponsiveContainer>
  );

  const renderHeatmap = (data, viz) => (
    <Box sx={{ p: 2, bgcolor: '#f5f5f5', borderRadius: 1 }}>
      <Typography variant="body2" align="center">
        Heatmap visualization - Correlation matrix
      </Typography>
      <Typography variant="caption" color="text.secondary" align="center">
        (Interactive heatmap requires additional library)
      </Typography>
    </Box>
  );

  const renderGanttChart = (data, viz) => (
    <Box sx={{ p: 2 }}>
      <Typography variant="body2" gutterBottom>Timeline View:</Typography>
      {data && data.length > 0 ? (
        data.slice(0, 10).map((item, idx) => (
          <Box key={idx} sx={{ mb: 1 }}>
            <Typography variant="caption">{item.task || item.name || `Item ${idx + 1}`}</Typography>
            <Box sx={{ 
              height: 20, 
              bgcolor: COLORS[idx % COLORS.length], 
              width: `${Math.random() * 100}%`,
              borderRadius: 1
            }} />
          </Box>
        ))
      ) : (
        <Typography variant="caption">No timeline data</Typography>
      )}
    </Box>
  );

  // Generate report
  const handleGenerateReport = async () => {
    try {
      const response = await fetch('http://localhost:3001/api/ai/generate-report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          filename: file.name,
          aiResults: aiResults
        })
      });

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `AI_Analytics_${Date.now()}.pdf`;
      a.click();
    } catch (error) {
      console.error('Report generation error:', error);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ mb: 3 }}>
        🤖 Autonomous AI Studio
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        Upload your data - AI will automatically analyze, visualize, and generate insights!
      </Typography>

      {/* Upload Section */}
      {!aiResults && (
        <Card>
          <CardContent>
            <Box sx={{
              border: '2px dashed #3b82f6',
              borderRadius: 2,
              p: 6,
              textAlign: 'center',
              bgcolor: 'rgba(59, 130, 246, 0.05)'
            }}>
              <AutoAwesome sx={{ fontSize: 80, color: '#3b82f6', mb: 2 }} />
              <Typography variant="h5" gutterBottom>
                Upload Data - AI Does The Rest!
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                No configuration needed. AI automatically selects best visualizations.
              </Typography>
              
              <Button variant="contained" component="label" disabled={uploading} size="large">
                {uploading ? <CircularProgress size={24} /> : 'Choose File'}
                <input type="file" hidden accept=".csv,.xlsx,.xls" onChange={handleFileUpload} />
              </Button>
            </Box>
          </CardContent>
        </Card>
      )}

      {/* AI Results */}
      {aiResults && (
        <>
          {/* Insights */}
          <Card sx={{ mb: 3, bgcolor: '#f0fdf4' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Insights /> AI Insights
              </Typography>
              {aiResults.insights?.map((insight, idx) => (
                <Typography key={idx} variant="body2" sx={{ mb: 0.5 }}>
                  {insight}
                </Typography>
              ))}
            </CardContent>
          </Card>

          {/* Toggles/Filters */}
          {aiResults.toggles && aiResults.toggles.length > 0 && (
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <FilterList /> Smart Filters
                </Typography>
                <Grid container spacing={2}>
                  {aiResults.toggles.map((toggle, idx) => (
                    <Grid item xs={12} md={6} lg={3} key={idx}>
                      <Typography variant="caption">{toggle.label}</Typography>
                      {toggle.type === 'multi_select' && (
                        <FormControl fullWidth size="small">
                          <Select defaultValue="all">
                            <MenuItem value="all">All</MenuItem>
                            {toggle.options?.slice(0, 10).map(opt => (
                              <MenuItem key={opt} value={opt}>{opt}</MenuItem>
                            ))}
                          </Select>
                        </FormControl>
                      )}
                      {toggle.type === 'range_slider' && (
                        <Slider
                          defaultValue={[toggle.min, toggle.max]}
                          min={toggle.min}
                          max={toggle.max}
                          valueLabelDisplay="auto"
                        />
                      )}
                    </Grid>
                  ))}
                </Grid>
              </CardContent>
            </Card>
          )}

          {/* Visualizations */}
          <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="h5">
              🎨 AI-Selected Visualizations ({visualizations.length})
            </Typography>
            <Button variant="contained" onClick={handleGenerateReport} startIcon={<Download />}>
              Generate Report
            </Button>
          </Box>

          <Grid container spacing={3}>
            {visualizations.map((viz, idx) => (
              <Grid item xs={12} md={6} key={idx}>
                <Card>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2 }}>
                      <Box>
                        <Typography variant="h6">{viz.title}</Typography>
                        <Typography variant="caption" color="text.secondary">
                          {viz.description}
                        </Typography>
                      </Box>
                      <Chip 
                        label={viz.priority} 
                        size="small" 
                        color={viz.priority === 'high' ? 'error' : viz.priority === 'medium' ? 'warning' : 'default'}
                      />
                    </Box>
                    
                    {renderVisualization(viz)}
                    
                    {!vizData[`${viz.type}_${viz.title.replace(/\s/g, '_')}`] && !loading[`${viz.type}_${viz.title.replace(/\s/g, '_')}`] && (
                      <Button 
                        fullWidth 
                        variant="outlined" 
                        sx={{ mt: 2 }}
                        onClick={() => loadVisualization(viz, file.name)}
                      >
                        Load Visualization
                      </Button>
                    )}
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>

          <Button
            variant="outlined"
            onClick={() => {
              setAiResults(null);
              setFile(null);
              setVisualizationData({});
            }}
            sx={{ mt: 3 }}
          >
            Upload New File
          </Button>
        </>
      )}
    </Box>
  );
};

export default AutonomousVisualizer;