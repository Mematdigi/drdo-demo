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
    const pythonCommand = process.platform === 'win32' ? 'py' : 'python3';
    
    console.log('🐍 Python:', pythonCommand, scriptName, 'Args:', args.length);
    
    const python = spawn(pythonCommand, [pythonPath, ...args], {
      cwd: workingDir,
      shell: true
    });
    
    let dataString = '';
    let errorString = '';
    
    python.stdout.on('data', (data) => {
      const output = data.toString();
      dataString += output;
      console.log('📤 Python output:', output.substring(0, 200));
    });
    
    python.stderr.on('data', (data) => {
      const error = data.toString();
      errorString += error;
      console.error('❌ Python error:', error);
    });
    
    python.on('close', (code) => {
      console.log('🏁 Python finished with code:', code);
      
      if (code !== 0) {
        console.error('💥 Python failed:', errorString || dataString);
        reject(new Error(errorString || dataString || `Exit code ${code}`));
      } else {
        try {
          const result = JSON.parse(dataString);
          console.log('✅ Parsed result:', result.success ? 'SUCCESS' : 'FAILED');
          resolve(result);
        } catch (e) {
          console.error('⚠️ JSON parse error. Raw output:', dataString.substring(0, 500));
          reject(new Error('Invalid JSON from Python'));
        }
      }
    });
  });
}

// AI Analyze with AUTO-LOAD of visualizations
router.post('/analyze', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ success: false, error: 'No file uploaded' });
    }
    
    console.log('🤖 AI Analyzing:', req.file.originalname);
    console.log('📂 File path:', req.file.path);
    
    fileStorage[req.file.originalname] = req.file.path;
    
    // Run AI analysis
    const result = await runPython('improved_autonomous_ai.py', [req.file.path, 'analyze']);
    
    if (!result.success) {
      console.error('❌ AI analysis failed:', result.error);
      return res.status(500).json(result);
    }
    
    console.log('✅ AI created', result.visualizations?.length || 0, 'visualizations');
    
    // AUTO-PREPARE DATA for all visualizations
    if (result.visualizations && result.visualizations.length > 0) {
      console.log('🔄 Auto-preparing data for all visualizations...');
      
      for (let i = 0; i < Math.min(result.visualizations.length, 10); i++) {
        const viz = result.visualizations[i];
        
        try {
          // Write config to temp file
          const tempConfig = path.join(__dirname, '../../uploads', `config_${Date.now()}_${i}.json`);
          fs.writeFileSync(tempConfig, JSON.stringify(viz), 'utf8');
          
          // Prepare data
          const vizResult = await runPython('FIX_CHART_DATA.py', [
            req.file.path,
            'prepare_viz',
            tempConfig
          ]);
          
          // Add data to visualization
          if (vizResult.success && vizResult.data) {
            result.visualizations[i].data = vizResult.data;
            console.log(`✅ Loaded data for viz ${i}: ${vizResult.data.length} points`);
          }
          
          // Cleanup
          try { fs.unlinkSync(tempConfig); } catch (e) {}
          
        } catch (error) {
          console.error(`❌ Error preparing viz ${i}:`, error.message);
        }
      }
    }
    
    res.json(result);
    
  } catch (error) {
    console.error('❌ Analyze error:', error.message);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Manual viz preparation (backup)
router.post('/prepare-viz', async (req, res) => {
  try {
    const { filename, viz_config } = req.body;
    
    console.log('📊 Manual viz prep:', viz_config?.title);
    
    let filepath = fileStorage[filename];
    if (!filepath || !fs.existsSync(filepath)) {
      filepath = path.join(__dirname, '../../uploads', filename);
    }
    
    if (!fs.existsSync(filepath)) {
      console.error('❌ File not found:', filename);
      return res.status(404).json({ success: false, error: 'File not found' });
    }
    
    // Write config
    const tempConfig = path.join(__dirname, '../../uploads', `config_manual_${Date.now()}.json`);
    fs.writeFileSync(tempConfig, JSON.stringify(viz_config), 'utf8');
    
    const result = await runPython('FIX_CHART_DATA.py', [
      filepath,
      'prepare_viz',
      tempConfig
    ]);
    
    // Cleanup
    try { fs.unlinkSync(tempConfig); } catch (e) {}
    
    console.log('✅ Manual viz loaded:', result.data?.length || 0, 'points');
    res.json(result);
    
  } catch (error) {
    console.error('❌ Prepare viz error:', error.message);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Generate Report
router.post('/generate-report', async (req, res) => {
  try {
    const { filename } = req.body;
    
    console.log('📄 Generating report for:', filename);
    
    let filepath = fileStorage[filename];
    if (!filepath || !fs.existsSync(filepath)) {
      filepath = path.join(__dirname, '../../uploads', filename);
    }
    
    if (!fs.existsSync(filepath)) {
      return res.status(404).json({ success: false, error: 'File not found' });
    }
    
    const result = await runPython('ULTIMATE_AI_REPORT.py', [filepath]);
    
    if (result.success) {
      const pdfPath = result.path;
      
      if (fs.existsSync(pdfPath)) {
        console.log('✅ Report generated:', result.filename);
        res.download(pdfPath, result.filename);
      } else {
        res.status(404).json({ success: false, error: 'PDF not found' });
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