import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  CircularProgress,
  Alert,
} from '@mui/material';
import { getStateAnalysis, getResponseTimeAnalysis } from '../services/api';

const Analytics = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [stateData, setStateData] = useState([]);
  const [responseTimeData, setResponseTimeData] = useState([]);

  useEffect(() => {
    loadAnalyticsData();
  }, []);

  const loadAnalyticsData = async () => {
    try {
      const [stateRes, responseRes] = await Promise.all([
        getStateAnalysis(),
        getResponseTimeAnalysis(),
      ]);
      setStateData(stateRes.data.slice(0, 10));
      setResponseTimeData(responseRes.data);
    } catch (err) {
      setError('Failed to load analytics data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity) => {
    const colors = {
      Critical: 'error',
      High: 'warning',
      Medium: 'info',
      Low: 'success',
    };
    return colors[severity] || 'default';
  };

  if (loading) return <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}><CircularProgress /></Box>;
  if (error) return <Alert severity="error">{error}</Alert>;

  return (
    <Box>
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h5" gutterBottom>State-wise Analysis</Typography>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell><strong>State</strong></TableCell>
                  <TableCell align="right"><strong>Incidents</strong></TableCell>
                  <TableCell align="right"><strong>Casualties</strong></TableCell>
                  <TableCell align="right"><strong>Avg Response Time</strong></TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {stateData.map((state, idx) => (
                  <TableRow key={idx} hover>
                    <TableCell>{state.state}</TableCell>
                    <TableCell align="right">{state.incidents}</TableCell>
                    <TableCell align="right">{state.casualties}</TableCell>
                    <TableCell align="right">{state.avg_response_time} min</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <Typography variant="h5" gutterBottom>Response Time by Severity</Typography>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell><strong>Severity</strong></TableCell>
                  <TableCell align="right"><strong>Avg Time</strong></TableCell>
                  <TableCell align="right"><strong>Min Time</strong></TableCell>
                  <TableCell align="right"><strong>Max Time</strong></TableCell>
                  <TableCell align="right"><strong>Count</strong></TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {responseTimeData.map((item, idx) => (
                  <TableRow key={idx} hover>
                    <TableCell>
                      <Chip 
                        label={item.severity} 
                        color={getSeverityColor(item.severity)} 
                        size="small" 
                      />
                    </TableCell>
                    <TableCell align="right">{item.avg_time} min</TableCell>
                    <TableCell align="right">{item.min_time} min</TableCell>
                    <TableCell align="right">{item.max_time} min</TableCell>
                    <TableCell align="right">{item.count}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Analytics;
