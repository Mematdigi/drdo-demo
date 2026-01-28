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
  CircularProgress,
  Alert,
  Chip,
} from '@mui/material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { getVendorPerformance } from '../services/api';

const Vendors = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [vendors, setVendors] = useState([]);

  useEffect(() => {
    loadVendorData();
  }, []);

  const loadVendorData = async () => {
    try {
      const response = await getVendorPerformance();
      setVendors(response.data.slice(0, 10));
    } catch (err) {
      setError('Failed to load vendor data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getPerformanceColor = (percentage) => {
    if (percentage >= 90) return 'success';
    if (percentage >= 70) return 'warning';
    return 'error';
  };

  if (loading) return <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}><CircularProgress /></Box>;
  if (error) return <Alert severity="error">{error}</Alert>;

  return (
    <Box>
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h5" gutterBottom>Vendor Performance Leaderboard</Typography>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell><strong>Rank</strong></TableCell>
                  <TableCell><strong>Vendor Name</strong></TableCell>
                  <TableCell><strong>Type</strong></TableCell>
                  <TableCell align="right"><strong>Deliveries</strong></TableCell>
                  <TableCell align="right"><strong>On-Time %</strong></TableCell>
                  <TableCell align="right"><strong>Quality Score</strong></TableCell>
                  <TableCell align="right"><strong>Defects</strong></TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {vendors.map((vendor, idx) => (
                  <TableRow key={idx} hover>
                    <TableCell><Chip label={`#${idx + 1}`} size="small" /></TableCell>
                    <TableCell>{vendor.vendor_name}</TableCell>
                    <TableCell>{vendor.vendor_type}</TableCell>
                    <TableCell align="right">{vendor.total_deliveries}</TableCell>
                    <TableCell align="right">
                      <Chip
                        label={`${vendor.on_time_percentage.toFixed(1)}%`}
                        color={getPerformanceColor(vendor.on_time_percentage)}
                        size="small"
                      />
                    </TableCell>
                    <TableCell align="right">{vendor.avg_quality_score.toFixed(2)}</TableCell>
                    <TableCell align="right">{vendor.total_defects}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <Typography variant="h5" gutterBottom>On-Time Performance Comparison</Typography>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={vendors.slice(0, 8)}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="vendor_name" stroke="#94a3b8" angle={-45} textAnchor="end" height={150} />
              <YAxis stroke="#94a3b8" />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155' }} />
              <Bar dataKey="on_time_percentage" fill="#10b981" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Vendors;
