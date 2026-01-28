const express = require('express');
const router = express.Router();
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

// Store file paths
const fileStorage = {};

// Configure multer
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

// Helper to run Python
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
      console.error('❌ Python error:', data.toString());
    });
    
    python.on('close', (code) => {
      if (code !== 0) {
        console.error('💥 Python failed:', errorString || dataString);
        reject(new Error(errorString || dataString || `Python exited with code ${code}`));
      } else {
        try {
          resolve(JSON.parse(dataString));
        } catch (e) {
          console.error('⚠️ JSON parse error');
          reject(new Error('Invalid JSON response from Python'));
        }
      }
    });
  });
}

// Analyze endpoint
router.post('/analyze', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ success: false, error: 'No file uploaded' });
    }
    
    console.log('📥 Analyzing:', req.file.originalname);
    
    // Store file path
    fileStorage[req.file.originalname] = req.file.path;
    
    const result = await runPython('smart_processor.py', ['analyze', req.file.path]);
    
    console.log('✅ Analysis complete!');
    res.json(result);
    
  } catch (error) {
    console.error('❌ Analysis error:', error.message);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Prepare visualization endpoint
router.post('/prepare-viz', async (req, res) => {
  try {
    const { filename, viz_config } = req.body;
    
    console.log('📊 Preparing viz:', viz_config?.type);
    
    if (!filename || !viz_config) {
      return res.status(400).json({ success: false, error: 'Missing parameters' });
    }
    
    // Get file path
    let filepath = fileStorage[filename];
    if (!filepath || !fs.existsSync(filepath)) {
      filepath = path.join(__dirname, '../../uploads', filename);
    }
    
    if (!fs.existsSync(filepath)) {
      return res.status(404).json({ success: false, error: 'File not found' });
    }
    
    // Write viz_config to temp file
    const tempConfigFile = path.join(__dirname, '../../uploads', `viz_config_${Date.now()}.json`);
    fs.writeFileSync(tempConfigFile, JSON.stringify(viz_config), 'utf8');
    
    const result = await runPython('smart_processor.py', [
      'prepare_viz',
      filepath,
      tempConfigFile
    ]);
    
    // Clean up
    try { fs.unlinkSync(tempConfigFile); } catch (e) {}
    
    console.log('✅ Visualization prepared!');
    res.json(result);
    
  } catch (error) {
    console.error('❌ Viz error:', error.message);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Generate SMART report with AI analytics
router.post('/generate-report', async (req, res) => {
  try {
    const { filename } = req.body;
    
    console.log('🤖 Generating SMART analytics report for:', filename);
    
    // Get file path
    let filepath = fileStorage[filename];
    if (!filepath || !fs.existsSync(filepath)) {
      filepath = path.join(__dirname, '../../uploads', filename);
    }
    
    if (!fs.existsSync(filepath)) {
      return res.status(404).json({ success: false, error: 'File not found. Please upload again.' });
    }
    
    console.log('📊 Running AI analysis...');
    
    // Generate smart analytics report
    const result = await runPython('smart_analytics_report.py', [filepath]);
    
    if (result.success) {
      console.log('✅ Report generated:', result.filename);
      console.log(`   - ${result.insights_count} insights`);
      console.log(`   - ${result.predictions_count} predictions`);
      console.log(`   - ${result.recommendations_count} recommendations`);
      
      const pdfPath = result.path;
      
      if (fs.existsSync(pdfPath)) {
        res.download(pdfPath, result.filename, (err) => {
          if (err) {
            console.error('Error sending file:', err);
          }
        });
      } else {
        res.status(404).json({ success: false, error: 'PDF file not found' });
      }
    } else {
      res.status(500).json({ success: false, error: result.error });
    }
    
  } catch (error) {
    console.error('❌ Report error:', error.message);
    res.status(500).json({ success: false, error: error.message });
  }
});

module.exports = router;