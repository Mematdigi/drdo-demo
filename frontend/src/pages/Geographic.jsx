import React, { useState, useEffect } from 'react';
import { Box, Card, CardContent, Typography, Alert, CircularProgress } from '@mui/material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { getStateAnalysis } from '../services/api';

const Geographic = () => {
  const [loading, setLoading] = useState(true);
  const [stateData, setStateData] = useState([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const response = await getStateAnalysis();
      setStateData(response.data.slice(0, 10));
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}><CircularProgress /></Box>;

  return (
    <Box>
      <Alert severity="info" sx={{ mb: 3 }}>
        <strong>Geographic Visualization</strong> - Interactive map with incident heat maps ready for integration.
      </Alert>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ 
            height: 400, 
            bgcolor: '#334155', 
            borderRadius: 2, 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            flexDirection: 'column',
            gap: 2
          }}>
            <Typography variant="h1">🗺️</Typography>
            <Typography variant="h5">India Fire Incident Heat Map</Typography>
            <Typography variant="body2" color="text.secondary">
              138 Fire Stations • {stateData.reduce((sum, s) => sum + s.incidents, 0)} Incidents
            </Typography>
          </Box>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <Typography variant="h5" gutterBottom>Top 10 States by Incidents</Typography>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={stateData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="state" stroke="#94a3b8" angle={-45} textAnchor="end" height={120} />
              <YAxis stroke="#94a3b8" />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155' }} />
              <Bar dataKey="incidents" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Geographic;
