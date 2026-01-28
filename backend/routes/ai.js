const express = require('express');
const router = express.Router();
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

const fileStorage = {};

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    const uploadsDir = path.join(__dirname, '../../uploads');
    if (!fs.existsSync(uploadsDir)) {
      fs.mkdirSync(uploadsDir, { recursive: true });
    }
    cb(null, uploadsDir);
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname);
  }
});

const upload = multer({ storage: storage });

function runPython(scriptName, args = []) {
  return new Promise((resolve, reject) => {
    const pythonPath = path.join(__dirname, '../../python-engine', scriptName);
    const workingDir = path.join(__dirname, '../../python-engine');
    const pythonCommand = process.platform === 'win32' ? 'py' : 'python';
    
    console.log('🐍 Running:', pythonCommand, scriptName);
    
    const python = spawn(pythonCommand, [pythonPath, ...args], {
      cwd: workingDir,
      shell: true
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
        console.error('Python failed:', errorString);
        reject(new Error(errorString || `Python exited with code ${code}`));
      } else {
        try {
          resolve(JSON.parse(dataString));
        } catch (e) {
          reject(new Error('Invalid JSON'));
        }
      }
    });
  });
}

// AI Analyze
router.post('/analyze', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ success: false, error: 'No file uploaded' });
    }
    
    console.log('🤖 AI Analyzing:', req.file.originalname);
    
    fileStorage[req.file.originalname] = req.file.path;
    
    const result = await runPython('improved_autonomous_ai.py', [req.file.path, 'analyze']);
    
    console.log('✅ AI created', result.visualizations?.length || 0, 'visualizations');
    res.json(result);
    
  } catch (error) {
    console.error('❌', error.message);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Prepare visualization - FIXED!
router.post('/prepare-viz', async (req, res) => {
  try {
    const { filename, viz_config } = req.body;
    
    console.log('📊 Loading:', viz_config?.title);
    
    let filepath = fileStorage[filename];
    if (!filepath || !fs.existsSync(filepath)) {
      filepath = path.join(__dirname, '../../uploads', filename);
    }
    
    if (!fs.existsSync(filepath)) {
      return res.status(404).json({ success: false, error: 'File not found' });
    }
    
    // Write config to temp file
    const tempConfig = path.join(__dirname, '../../uploads', `config_${Date.now()}.json`);
    fs.writeFileSync(tempConfig, JSON.stringify(viz_config), 'utf8');
    
    // Use fixed chart data script
    const result = await runPython('FIX_CHART_DATA.py', [
      filepath,
      'prepare_viz',
      tempConfig
    ]);
    
    // Cleanup
    try { fs.unlinkSync(tempConfig); } catch (e) {}
    
    console.log('✅ Loaded:', result.data?.length || 0, 'data points');
    res.json(result);
    
  } catch (error) {
    console.error('❌', error.message);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Generate ULTIMATE PREDICTIVE Report
router.post('/generate-report', async (req, res) => {
  try {
    const { filename } = req.body;
    
    console.log('📄 Generating ULTIMATE AI REPORT...');
    
    let filepath = fileStorage[filename];
    if (!filepath || !fs.existsSync(filepath)) {
      filepath = path.join(__dirname, '../../uploads', filename);
    }
    
    if (!fs.existsSync(filepath)) {
      return res.status(404).json({ success: false, error: 'File not found' });
    }
    
    // Use ULTIMATE AI REPORT
    const result = await runPython('ULTIMATE_AI_REPORT.py', [filepath]);
    
    if (result.success) {
      const pdfPath = result.path;
      
      if (fs.existsSync(pdfPath)) {
        console.log('✅ ULTIMATE REPORT generated!');
        res.download(pdfPath, result.filename);
      } else {
        res.status(404).json({ success: false, error: 'PDF not found' });
      }
    } else {
      res.status(500).json({ success: false, error: result.error });
    }
    
  } catch (error) {
    console.error('❌', error.message);
    res.status(500).json({ success: false, error: error.message });
  }
});

module.exports = router;