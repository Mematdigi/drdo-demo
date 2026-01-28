const express = require('express');
const router = express.Router();
const multer = require('multer');
const XLSX = require('xlsx');
const path = require('path');
const fs = require('fs');

const upload = multer({ dest: 'uploads/' });

// Data validation templates
const templates = {
  incident: {
    required: ['incident_number', 'timestamp', 'state', 'district', 'city', 'incident_type', 'severity', 'response_time_minutes'],
    optional: ['location', 'latitude', 'longitude', 'casualties', 'injuries', 'property_damage_inr', 'station_id', 'vehicles_deployed', 'personnel_count', 'cause', 'remarks'],
    validations: {
      severity: ['Low', 'Medium', 'High', 'Critical'],
      incident_type: ['Building Fire', 'Vehicle Fire', 'Forest Fire', 'Industrial Fire', 'Electrical Fire', 'Kitchen Fire', 'Chemical Fire', 'Gas Leak']
    }
  },
  vendor: {
    required: ['vendor_name', 'vendor_type', 'contact_person', 'phone', 'email'],
    optional: ['registration_no', 'address', 'contract_id', 'contract_start_date', 'contract_end_date', 'contract_value_inr', 'performance_score']
  },
  station: {
    required: ['station_id', 'station_name', 'state', 'city'],
    optional: ['address', 'latitude', 'longitude', 'personnel_count', 'vehicles', 'established_year', 'coverage_area_sqkm']
  }
};

// Validate record
function validateRecord(record, template, rowNum) {
  const errors = [];
  
  for (const field of template.required) {
    if (!record[field] || record[field] === '') {
      errors.push({ row: rowNum, field: field, message: 'Required field missing' });
    }
  }
  
  if (template.validations) {
    for (const [field, allowedValues] of Object.entries(template.validations)) {
      if (record[field] && !allowedValues.includes(record[field])) {
        errors.push({ row: rowNum, field: field, message: `Must be one of: ${allowedValues.join(', ')}` });
      }
    }
  }
  
  return errors;
}

router.post('/ingest', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ success: false, error: 'No file uploaded' });
    }
    
    const templateType = req.body.template || 'incident';
    const template = templates[templateType];
    
    const workbook = XLSX.readFile(req.file.path);
    const sheetName = workbook.SheetNames[0];
    const data = XLSX.utils.sheet_to_json(workbook.Sheets[sheetName]);
    
    const validationErrors = [];
    const validRecords = [];
    
    data.forEach((record, index) => {
      const errors = validateRecord(record, template, index + 2);
      if (errors.length > 0) {
        validationErrors.push(...errors);
      } else {
        validRecords.push(record);
      }
    });
    
    fs.unlinkSync(req.file.path);
    
    res.json({
      success: true,
      recordsProcessed: data.length,
      validRecords: validRecords.length,
      invalidRecords: data.length - validRecords.length,
      validationErrors: validationErrors.slice(0, 50),
      preview: validRecords.slice(0, 5)
    });
    
  } catch (error) {
    console.error('Ingestion error:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

module.exports = router;