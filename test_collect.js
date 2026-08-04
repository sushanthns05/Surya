const fs = require('fs');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;
const html = fs.readFileSync('public/Register_SST.html', 'utf8');
const dom = new JSDOM(html);
const document = dom.window.document;

const labelKeys = {
  "Father's Name": 'pd-father', "Mother's Name": 'pd-mother',
  'Annual Income': 'pd-income', 'Permanent Address': 'pd-address',
  'State': 'pd-state', 'District': 'pd-district', 'PIN Code': 'pd-pin',
  'Class X Board': 'academic-board', 'Class X Passing Year': 'academic-year',
  'Class X Marks (%)': 'academic-marks', 'Medium of Examination': 'exam-medium',
  'Class XII Board': 'academic-board', 'Class XII Stream': 'academic-stream',
  'Class XII Marks (%)': 'academic-marks', 'Current Class/Degree': 'academic-current-class',
  'Previous Class Marks': 'academic-marks', 'Previous Year Marks (%)': 'academic-marks',
  'Preference 1': 'preference-1', 'Preference 2': 'preference-2',
  'Nationality': 'nationality'
};

const data = {};
const form = document.getElementById('seoas-form');
form.querySelectorAll('input:not([type="file"]), select, textarea').forEach(input => {
  const label = input.closest('.form-group')?.querySelector('label')?.textContent
    .trim().replace(/\s*\*\s*$/, '');
  const isAcademicField = Boolean(input.closest('#dynamic-academic-fields'));
  const normalizedLabel = label?.toLowerCase()
    .replace(/[^a-z0-9]+/g, '_').replace(/^_|_$/g, '');
  let key = input.id || labelKeys[label] || normalizedLabel;

  if (isAcademicField && !String(key).startsWith('academic-')) {
    key = `academic-${normalizedLabel || 'detail'}`;
  }
  
  // mock user input
  let val = 'test';
  if (input.tagName === 'SELECT') val = input.querySelector('option').textContent;
  
  if (key) data[key] = val;
});

console.log("Collected Data:", data);
