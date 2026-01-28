const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const multer = require('multer');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const XLSX = require('xlsx');

const app = express();
const PORT = 3001;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Configure multer for file uploads
const upload = multer({ dest: '../data/uploads/' });

const smartRoutes = require('./routes/smart');
app.use('/api/smart', smartRoutes);

const aiRoutes = require('./routes/ai');
app.use('/api/ai', aiRoutes);

// Helper function to run Python scripts
function runPythonScript(scriptName, args = []) {
  return new Promise((resolve, reject) => {
    const pythonPath = path.join(__dirname, '../python-engine', scriptName);
    const workingDir = path.join(__dirname, '../python-engine');
    const python = spawn('py', [pythonPath, ...args], {
      cwd: workingDir  // Set working directory for Python script
    });
    
    let dataString = '';
    let errorString = '';
    
    python.stdout.on('data', (data) => {
      dataString += data.toString();
    });
    
    python.stderr.on('data', (data) => {
      errorString += data.toString();
    });
    
    python.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(errorString || `Python script exited with code ${code}`));
      } else {
        try {
          // Try to parse as JSON, otherwise return raw output
          const result = JSON.parse(dataString);
          resolve(result);
        } catch (e) {
          resolve(dataString);
        }
      }
    });
  });
}

// ===== API ENDPOINTS =====

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', message: 'Fire Department Analytics API is running' });
});

// Get dashboard KPIs
app.get('/api/dashboard/kpis', async (req, res) => {
  try {
    const data = await runPythonScript('api_bridge.py', ['get_kpis']);
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get incidents by type
app.get('/api/analytics/incidents-by-type', async (req, res) => {
  try {
    const data = await runPythonScript('api_bridge.py', ['get_incidents_by_type']);
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get incidents by severity
app.get('/api/analytics/incidents-by-severity', async (req, res) => {
  try {
    const data = await runPythonScript('api_bridge.py', ['get_incidents_by_severity']);
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get state-wise analysis
app.get('/api/analytics/by-state', async (req, res) => {
  try {
    const data = await runPythonScript('api_bridge.py', ['get_state_analysis']);
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get monthly trends
app.get('/api/analytics/monthly-trends', async (req, res) => {
  try {
    const data = await runPythonScript('api_bridge.py', ['get_monthly_trends']);
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get response time analysis
app.get('/api/analytics/response-time', async (req, res) => {
  try {
    const data = await runPythonScript('api_bridge.py', ['get_response_time']);
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get vendor performance
app.get('/api/vendors/performance', async (req, res) => {
  try {
    const data = await runPythonScript('api_bridge.py', ['get_vendor_performance']);
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get geographic data
app.get('/api/analytics/geographic', async (req, res) => {
  try {
    const data = await runPythonScript('api_bridge.py', ['get_geographic_data']);
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get top causes
app.get('/api/analytics/top-causes', async (req, res) => {
  try {
    const data = await runPythonScript('api_bridge.py', ['get_top_causes']);
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});


// Search incidents
app.post('/api/incidents/search', async (req, res) => {
  try {
    const filters = req.body;
    const data = await runPythonScript('api_bridge.py', ['search_incidents', JSON.stringify(filters)]);
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Generate PDF report
app.post('/api/reports/generate-pdf', async (req, res) => {
  try {
    const result = await runPythonScript('api_bridge.py', ['generate_pdf_report']);
    
    // Read the generated file
    const filePath = result.file_path;
    const fileName = path.basename(filePath);
    
    res.download(filePath, fileName, (err) => {
      if (err) {
        res.status(500).json({ error: 'Error downloading file' });
      }
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Generate Excel report
app.post('/api/reports/generate-excel', async (req, res) => {
  try {
    const result = await runPythonScript('api_bridge.py', ['generate_excel_report']);
    
    // Read the generated file
    const filePath = result.file_path;
    const fileName = path.basename(filePath);
    
    res.download(filePath, fileName, (err) => {
      if (err) {
        res.status(500).json({ error: 'Error downloading file' });
      }
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Upload data file
app.post('/api/data/upload', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }
    
    const filePath = req.file.path;
    const fileType = req.file.mimetype;
    
    // Process based on file type
    let data = [];
    if (fileType.includes('excel') || fileType.includes('spreadsheet')) {
      const workbook = XLSX.readFile(filePath);
      const sheetName = workbook.SheetNames[0];
      data = XLSX.utils.sheet_to_json(workbook.Sheets[sheetName]);
    } else if (fileType.includes('csv')) {
      const workbook = XLSX.readFile(filePath);
      const sheetName = workbook.SheetNames[0];
      data = XLSX.utils.sheet_to_json(workbook.Sheets[sheetName]);
    }
    
    // Clean up uploaded file
    fs.unlinkSync(filePath);
    
    res.json({
      success: true,
      message: 'File uploaded and processed successfully',
      recordsCount: data.length,
      sample: data.slice(0, 5)
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Serve static files from reports directory
app.use('/reports', express.static(path.join(__dirname, '../reports')));

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Fire Department Analytics API running on http://localhost:${PORT}`);
  console.log(`📊 Endpoints available:`);
  console.log(`   - GET  /api/health`);
  console.log(`   - GET  /api/dashboard/kpis`);
  console.log(`   - GET  /api/analytics/*`);
  console.log(`   - GET  /api/vendors/performance`);
  console.log(`   - POST /api/reports/generate-pdf`);
  console.log(`   - POST /api/reports/generate-excel`);
  console.log(`   - POST /api/data/upload`);
});

module.exports = app;
