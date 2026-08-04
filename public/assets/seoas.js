// seoas.js
const SEOAS_API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ? '' : 'https://surya-s2f5.onrender.com';


let currentStep = 1;
const totalSteps = 10;
const form = document.getElementById('seoas-form');

// Start Registration (Hide home, show wizard)
function startRegistration() {
  document.getElementById('seoas-home').style.display = 'none';
  document.getElementById('registration-wizard').style.display = 'block';
  document.getElementById('btn-next').style.display = 'inline-block';
  updateUI();
  loadAutoSave();
}

// Navigation
function nextStep() {
  if (!validateStep(currentStep)) return;
  if (currentStep === 1) {
    const mobileVerified = document.getElementById('reg-mobile').dataset.verified === 'true';
    const emailVerified = document.getElementById('reg-email').dataset.verified === 'true';
    if (!mobileVerified || !emailVerified) {
      alert("Please verify both Mobile Number and Email ID before proceeding.");
      return;
    }
  }

  // Add validation logic here later if needed
  if (currentStep < totalSteps) {
    currentStep++;
    updateUI();
    autoSave();
  }
}

function validateStep(stepNumber) {
  const step = document.querySelector(`.wizard-step[data-step="${stepNumber}"]`);
  if (!step) return true;
  const password = document.getElementById('reg-pass');
  const confirmation = document.getElementById('reg-pass2');
  if (password && confirmation) {
    const strong = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d]).{8,}$/;
    password.setCustomValidity(strong.test(password.value) ? '' : 'Use at least 8 characters with uppercase, lowercase, number, and special character.');
    confirmation.setCustomValidity(password.value === confirmation.value ? '' : 'Passwords do not match.');
  }
  const required = [...step.querySelectorAll('input, select, textarea')].filter(input => input.required);
  const invalid = required.find(input => !input.checkValidity());
  if (invalid) {
    invalid.reportValidity();
    invalid.focus();
    return false;
  }
  if (stepNumber === 3 && !document.getElementById('id-file')?.files.length) {
    alert('Please upload your government ID.');
    return false;
  }
  if (stepNumber === 7 && !document.getElementById('declare-check')?.checked) {
    alert('Please confirm that all information is correct.');
    return false;
  }
  return true;
}

function prevStep() {
  if (currentStep > 1) {
    currentStep--;
    updateUI();
  }
}

// Update UI
function updateUI() {
  // Hide all steps, show current
  document.querySelectorAll('.wizard-step').forEach(step => {
    step.classList.remove('active');
    if (parseInt(step.dataset.step) === currentStep) {
      step.classList.add('active');
    }
  });

  // Progress Bar
  const progressPercent = ((currentStep - 1) / (totalSteps - 1)) * 100;
  document.getElementById('progress-fill').style.width = `${progressPercent}%`;

  // Buttons
  const btnPrev = document.getElementById('btn-prev');
  const btnNext = document.getElementById('btn-next');
  
  if (currentStep === 1) {
    btnPrev.style.display = 'none';
  } else if (currentStep > 1 && currentStep < 9) {
    btnPrev.style.display = 'inline-block';
    btnNext.style.display = 'inline-block';
    btnNext.textContent = 'Save & Next';
  } else if (currentStep === 9) {
    btnPrev.style.display = 'inline-block';
    btnNext.style.display = 'none'; // Hidden because Submit is on the page
  } else if (currentStep === 10) {
    btnPrev.style.display = 'none';
    btnNext.style.display = 'none';
  }

  if (currentStep === 7) {
    generateReviewSummary();
  }
}

// Dummy OTP Verification
async function requestOtp(type) {
  const inputEl = document.getElementById(`reg-${type.toLowerCase()}`);
  const statusEl = document.getElementById(`${type.toLowerCase()}-status`);
  const contact = inputEl.value.trim();
  
  if (!contact) {
    alert(`Please enter a valid ${type}`);
    return;
  }

  if (type === 'Email') {
    statusEl.innerHTML = '<span style="color:var(--seoas-gold)">Sending OTP...</span>';
    const button = document.getElementById('btn-email');
    button.disabled = true;
    try {
      const formData = new FormData();
      formData.append('contact', contact);
      formData.append('type', 'Email');
      const response = await fetch(`${SEOAS_API_BASE}/api/send-otp`, { method: 'POST', body: formData });
      const result = await response.json();
      if (!response.ok || result.status !== 'ok') throw new Error(result.message || 'Unable to send OTP');
      statusEl.innerHTML = '<span style="color:var(--seoas-gold)">OTP sent to your email</span>';
      document.getElementById('email-otp-group').style.display = 'flex';
    } catch (error) {
      button.disabled = false;
      statusEl.innerHTML = `<span style="color:red">${error.message}</span>`;
    }
    return;
  }
  
  statusEl.innerHTML = '<span style="color:var(--seoas-emerald)">✅ Verified</span>';
  document.getElementById(`btn-${type.toLowerCase()}`).style.display = 'none';
  inputEl.readOnly = true;
  inputEl.dataset.verified = 'true';
}

async function confirmOtp(type) {
  const contact = document.getElementById(`reg-${type.toLowerCase()}`).value.trim();
  const otp = document.getElementById(`reg-${type.toLowerCase()}-otp`).value.trim();
  const statusEl = document.getElementById(`${type.toLowerCase()}-status`);
  
  if (!otp) {
    alert('Please enter the OTP');
    return;
  }
  
  statusEl.innerHTML = '<span style="color:var(--seoas-gold)">Verifying...</span>';
  
  try {
    const formData = new FormData();
    formData.append('contact', contact);
    formData.append('otp', otp);
    
    const response = await fetch(`${SEOAS_API_BASE}/api/verify-otp`, {
      method: 'POST',
      body: formData
    });
    
    const result = await response.json();
    if (result.status === 'ok') {
      statusEl.innerHTML = '<span style="color:var(--seoas-emerald)">✅ Verified</span>';
      document.getElementById(`${type.toLowerCase()}-otp-group`).style.display = 'none';
      document.getElementById(`btn-${type.toLowerCase()}`).style.display = 'none';
      document.getElementById(`reg-${type.toLowerCase()}`).readOnly = true;
      // Mark as verified
      document.getElementById(`reg-${type.toLowerCase()}`).dataset.verified = 'true';
    } else {
      statusEl.innerHTML = `<span style="color:red">Error: ${result.message}</span>`;
    }
  } catch (error) {
    statusEl.innerHTML = `<span style="color:red">Error verifying OTP</span>`;
  }
}

// Mock Payment
function mockPayment(method) {
  const statusEl = document.getElementById('payment-status');
  statusEl.innerHTML = `<span style="color:var(--seoas-gold)">Processing ${method} Payment...</span>`;
  setTimeout(() => {
    statusEl.innerHTML = '<span style="color:var(--seoas-emerald)">✅ Payment Successful!</span>';
    setTimeout(() => {
      nextStep(); // Auto advance to Step 9
    }, 1000);
  }, 2000);
}

// Final Submit (Firebase Firestore + Storage)
async function finalSubmit() {
  for (let step = 1; step <= 7; step++) {
    if (!validateStep(step)) {
      currentStep = step;
      updateUI();
      return;
    }
  }
  const submitBtn = document.querySelector('.wizard-step[data-step="9"] button');
  submitBtn.textContent = 'Submitting registration...';
  submitBtn.disabled = true;

  try {
    const data = collectFormData();

    const payload = new FormData();
    payload.append('data', JSON.stringify(data));
    form.querySelectorAll('input[type="file"]').forEach(input => {
      if (input.files[0]) payload.append(input.id || 'document', input.files[0]);
    });
    const response = await fetch(`${SEOAS_API_BASE}/api/seoas-register`, { method: 'POST', body: payload });
    const result = await response.json();
    if (!response.ok || result.status !== 'ok' || !result.application_number) {
      throw new Error(result.message || 'The server did not return an application number');
    }

    // Success Update
    const name = document.getElementById('reg-name').value || 'Candidate';
    document.getElementById('conf-name').textContent = name;
    document.getElementById('conf-app-no').textContent = result.application_number;
    renderConfirmation(data, result);
    currentStep = 10;
    updateUI();
    localStorage.removeItem('seoas-draft'); // Clear auto-save

  } catch (err) {
    console.error("Firebase Submit Error: ", err);
    alert("Submission failed: " + err.message);
    submitBtn.textContent = 'Submit Application Now';
    submitBtn.disabled = false;
  }
}

// Auto Save
function autoSave() {
  if (currentStep >= 10 || !form) return;
  const data = collectFormData();
  delete data['reg-pass'];
  delete data['reg-pass2'];
  localStorage.setItem('seoas-draft', JSON.stringify(data));
  console.log('Auto-saved at', new Date().toLocaleTimeString());
}

function collectFormData() {
  const labelKeys = {
    "Father's Name": 'pd-father', "Mother's Name": 'pd-mother',
    'Annual Income': 'pd-income', 'Permanent Address': 'pd-address',
    'State': 'pd-state', 'District': 'pd-district', 'PIN Code': 'pd-pin',
    'Class X Board': 'academic-board', 'Class X Passing Year': 'academic-year',
    'Class X Marks (%)': 'academic-marks', 'Medium of Examination': 'exam-medium',
    'Preference 1': 'preference-1', 'Preference 2': 'preference-2',
    'Nationality': 'nationality'
  };
  const data = {};
  form.querySelectorAll('input:not([type="file"]), select, textarea').forEach(input => {
    const label = input.closest('.form-group')?.querySelector('label')?.textContent.trim();
    const key = input.id || labelKeys[label] || label?.toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_|_$/g, '');
    if (key) data[key] = input.value;
  });
  return data;
}

setInterval(autoSave, 20000); // Save every 20s

function loadAutoSave() {
  const draft = localStorage.getItem('seoas-draft');
  if (draft) {
    const data = JSON.parse(draft);
    for (const key in data) {
      const input = document.getElementById(key);
      if (input) input.value = data[key];
    }
  }
}



// File Preview
function previewImage(input, previewId) {
  const file = input.files[0];
  const preview = document.getElementById(previewId);
  if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      preview.src = e.target.result;
      preview.style.display = 'block';
    }
    reader.readAsDataURL(file);
  }
}

function handleFileUpload(input, previewContainerId) {
  const file = input.files[0];
  const container = document.getElementById(previewContainerId);
  if (file) {
    container.innerHTML = `<span style="color:var(--seoas-emerald)">✅ ${file.name} uploaded successfully.</span>`;
    document.getElementById('id-ai-status').style.display = 'block';
    setTimeout(() => {
      document.getElementById('id-ai-status').innerHTML = '<span style="color:var(--seoas-emerald)">✅ AI Verification Passed</span>';
    }, 2000);
  }
}

// Review Summary
const EXAM_CENTERS = {
  Karnataka: ['Bengaluru', 'Mysuru', 'Mangaluru', 'Hubballi-Dharwad', 'Kalaburagi'],
  'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Tiruchirappalli', 'Salem'],
  Maharashtra: ['Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Aurangabad (Chhatrapati Sambhajinagar)'],
  Telangana: ['Hyderabad', 'Warangal', 'Karimnagar', 'Nizamabad', 'Khammam'],
  'Andhra Pradesh': ['Visakhapatnam', 'Vijayawada', 'Tirupati', 'Guntur', 'Kurnool'],
  Kerala: ['Thiruvananthapuram', 'Kochi', 'Kozhikode', 'Thrissur', 'Kannur']
};

function populateExamCenters() {
  document.querySelectorAll('.form-group').forEach(group => {
    const label = group.querySelector('label');
    const input = group.querySelector('input[type="text"]');
    if (!label || !input || !/^Preference [12]$/.test(label.textContent.trim())) return;
    const select = document.createElement('select');
    select.id = `preference-${label.textContent.trim().slice(-1)}`;
    select.required = true;
    select.innerHTML = '<option value="">Select a city</option>';
    Object.entries(EXAM_CENTERS).forEach(([state, cities]) => {
      const optgroup = document.createElement('optgroup');
      optgroup.label = state;
      cities.forEach(city => optgroup.appendChild(new Option(city, city)));
      select.appendChild(optgroup);
    });
    select.value = input.value;
    input.replaceWith(select);
  });
}

function renderConfirmation(data, result) {
  const details = document.querySelector('.wizard-step[data-step="10"] .confirmation-details');
  if (!details) return;
  details.replaceChildren();
  const allDetails = { application_number: result.application_number, ...data, password: result.password || '' };
  Object.entries(allDetails).forEach(([key, value]) => {
    if (key.startsWith('file_') || key === 'password_hash' || value === '') return;
    const item = document.createElement('div');
    const label = document.createElement('strong');
    label.textContent = `${key.replace(/[-_]/g, ' ')}: `;
    const text = document.createElement('span');
    text.textContent = String(value);
    if (key === 'application_number') text.className = 'text-emerald';
    item.append(label, text);
    details.appendChild(item);
  });
  let download = document.getElementById('conf-pdf');
  if (!download) {
    download = document.createElement('a');
    download.id = 'conf-pdf';
    download.className = 'seoas-btn btn-primary';
    download.textContent = 'Download Application PDF';
    download.target = '_blank';
    download.rel = 'noopener';
    details.parentElement.appendChild(download);
  }
  download.href = new URL(result.pdf_url, SEOAS_API_BASE || window.location.origin).href;
}

function generateReviewSummary() {
  const name = document.getElementById('reg-name').value || 'Not provided';
  const exam = document.getElementById('exam-select').value || 'Not selected';
  
  document.getElementById('review-content').innerHTML = `
    <div style="margin-bottom: 1rem;">
      <strong>Name:</strong> ${name} <br>
      <strong>Exam:</strong> ${exam} <br>
    </div>
    <button type="button" class="seoas-btn btn-outline" onclick="currentStep=2; updateUI();">Edit Details</button>
  `;
}


document.addEventListener('DOMContentLoaded', () => {
  populateExamCenters();
  setTimeout(() => {
    const pass = document.getElementById('reg-pass');
    if(pass) {
      pass.style.pointerEvents = 'auto';
      pass.style.zIndex = '99999';
      pass.style.position = 'relative';
    }
  }, 1000);
});
