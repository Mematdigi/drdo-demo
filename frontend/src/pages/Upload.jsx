import React, { useState } from 'react';
import { Box, Card, CardContent, Typography, Button, Alert } from '@mui/material';
import { CloudUpload } from '@mui/icons-material';
import { uploadDataFile } from '../services/api';

const Upload = () => {
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setUploading(true);
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await uploadDataFile(formData);
      setResult({ success: true, data: response.data });
    } catch (err) {
      setResult({ success: false, error: err.message });
    } finally {
      setUploading(false);
    }
  };

  return (
    <Box>
      <Alert severity="info" sx={{ mb: 3 }}>
        <strong>Data Upload</strong> - Upload CSV or Excel files containing fire incident data.
      </Alert>

      <Card>
        <CardContent>
          <Box sx={{
            border: '2px dashed #334155',
            borderRadius: 2,
            p: 4,
            textAlign: 'center',
            cursor: 'pointer',
            '&:hover': { borderColor: '#3b82f6', bgcolor: 'rgba(59, 130, 246, 0.05)' }
          }}>
            <CloudUpload sx={{ fontSize: 60, color: 'text.secondary', mb: 2 }} />
            <Typography variant="h6" gutterBottom>Upload Data File</Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Supported formats: CSV, Excel (.xlsx, .xls)
            </Typography>
            <Button
              variant="contained"
              component="label"
              disabled={uploading}
            >
              {uploading ? 'Uploading...' : 'Choose File'}
              <input
                type="file"
                hidden
                accept=".csv,.xlsx,.xls"
                onChange={handleFileUpload}
              />
            </Button>
          </Box>

          {result && (
            <Alert severity={result.success ? 'success' : 'error'} sx={{ mt: 3 }}>
              {result.success ? (
                <>
                  <strong>Upload Successful!</strong>
                  <p>Records processed: {result.data.recordsCount}</p>
                </>
              ) : (
                <>
                  <strong>Upload Failed</strong>
                  <p>{result.error}</p>
                </>
              )}
            </Alert>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default Upload;
