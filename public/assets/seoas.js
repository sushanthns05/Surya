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
  if (currentStep < 9) { // Prevent nextStep from bypassing step 9
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
      const verifiedInput = document.getElementById(`reg-${type.toLowerCase()}`);
      verifiedInput.readOnly = true;
      // Mark as verified
      verifiedInput.dataset.verified = 'true';
      if (type === 'Email' && result.verification_token) {
        verifiedInput.dataset.verificationToken = result.verification_token;
      }
    } else {
      statusEl.innerHTML = `<span style="color:red">Error: ${result.message}</span>`;
    }
  } catch (error) {
    statusEl.innerHTML = `<span style="color:red">Error verifying OTP</span>`;
  }
}

// Mock Payment
function mockPayment(method) {
  document.querySelectorAll('.payment-options button').forEach(btn => btn.disabled = true);
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
    const emailInput = document.getElementById('reg-email');
    if (emailInput?.dataset.verificationToken) {
      payload.append('email_verification_token', emailInput.dataset.verificationToken);
    }
    form.querySelectorAll('input[type="file"]').forEach(input => {
      if (input.files[0]) payload.append(input.id || 'document', input.files[0]);
    });
    const response = await fetch(`${SEOAS_API_BASE}/api/seoas-register`, { method: 'POST', body: payload });
    const result = await response.json();
    if (!response.ok || result.status !== 'ok' || !result.application_number) {
      throw new Error(result.message || 'The server did not return an application number');
    }

    // Success Update. Use the submitted payload as a fallback so the
    // confirmation cannot appear with a blank candidate name.
    const name = data['reg-name'] || document.getElementById('reg-name')?.value || result.details?.name || 'Candidate';
    const applicationNumber = String(result.application_number).trim();
    if (/^SEOAS-X+$/i.test(applicationNumber)) {
      throw new Error('The server returned an invalid application number. Please try again.');
    }
    document.getElementById('conf-name').textContent = name;
    document.getElementById('conf-app-no').textContent = applicationNumber;
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
    'Class XII Board': 'academic-board', 'Class XII Stream': 'academic-stream',
    'Class XII Marks (%)': 'academic-marks', 'Current Class/Degree': 'academic-current-class',
    'Previous Class Marks': 'academic-marks', 'Previous Year Marks (%)': 'academic-marks',
    'Preference 1': 'preference-1', 'Preference 2': 'preference-2',
    'Nationality': 'nationality'
  };
  const data = {};
  form.querySelectorAll('input:not([type="file"]), select, textarea').forEach(input => {
    // Some of the exam-specific academic fields do not have ids.  Keep their
    // labels as a fallback, but normalize the required-field marker first so
    // the label map works consistently ("Father's Name*" vs "Father's Name").
    const label = input.closest('.form-group')?.querySelector('label')?.textContent
      .trim().replace(/\s*\*\s*$/, '');
    const isAcademicField = Boolean(input.closest('#dynamic-academic-fields'));
    const normalizedLabel = label?.toLowerCase()
      .replace(/[^a-z0-9]+/g, '_').replace(/^_|_$/g, '');
    let key = input.id || labelKeys[label] || normalizedLabel;

    // The API uses the academic-* prefix to detect that at least one
    // qualification was provided.  Academic controls in the exam variants
    // are intentionally generated without ids, so classify all controls in
    // under that namespace. The academic section is Step 4 in the current
    // wizard, but targeting the section keeps this correct for every exam
    // variant regardless of step ordering.
    if (isAcademicField && !String(key).startsWith('academic-')) {
      key = `academic-${normalizedLabel || 'detail'}`;
    }
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

  const emailNotice = document.getElementById('conf-email-status') || document.createElement('p');
  emailNotice.id = 'conf-email-status';
  emailNotice.style.marginTop = '12px';
  emailNotice.style.color = result.email_sent ? 'var(--seoas-emerald)' : '#fbbf24';
  emailNotice.textContent = result.email_sent
    ? 'Confirmation email sent to your verified email address.'
    : 'Registration saved, but the confirmation email could not be sent. Please download the PDF and contact support.';
  if (!emailNotice.parentElement) details.parentElement.appendChild(emailNotice);
}

function generateReviewSummary() {
  const review = document.getElementById('review-content');
  if (!review) return;
  review.replaceChildren();

  const fragment = document.createDocumentFragment();
  const ignored = new Set(['reg-pass', 'reg-pass2', 'reg-mobile-otp', 'reg-email-otp']);
  const controls = form.querySelectorAll('input, select, textarea');
  let lastStep = null;

  controls.forEach(input => {
    if (input.type === 'file' || ignored.has(input.id) || input.type === 'button' || input.type === 'submit') return;
    const step = input.closest('.wizard-step')?.dataset.step;
    if (!step || step === '7' || step === '8' || step === '9' || step === '10') return;

    if (step !== lastStep) {
      const heading = document.createElement('h3');
      heading.textContent = `Step ${step} details`;
      heading.style.cssText = 'grid-column: 1 / -1; margin: 1rem 0 .25rem; color: var(--seoas-gold);';
      fragment.appendChild(heading);
      lastStep = step;
    }

    const label = input.closest('.form-group')?.querySelector('label')?.textContent
      .trim().replace(/\s*\*\s*$/, '') || input.id || 'Detail';
    const value = input.type === 'checkbox'
      ? (input.checked ? 'Confirmed' : 'Not confirmed')
      : (input.value.trim() || 'Not provided');
    const item = document.createElement('div');
    item.style.cssText = 'padding: .7rem; border: 1px solid rgba(255,255,255,.12); border-radius: 8px;';
    const name = document.createElement('strong');
    name.textContent = `${label}: `;
    const detail = document.createElement('span');
    detail.textContent = value;
    item.append(name, detail);
    fragment.appendChild(item);
  });

  const files = form.querySelectorAll('input[type="file"]');
  if (files.length) {
    const heading = document.createElement('h3');
    heading.textContent = 'Uploaded documents';
    heading.style.cssText = 'grid-column: 1 / -1; margin: 1rem 0 .25rem; color: var(--seoas-gold);';
    fragment.appendChild(heading);
    files.forEach(input => {
      const item = document.createElement('div');
      item.style.cssText = 'padding: .7rem; border: 1px solid rgba(255,255,255,.12); border-radius: 8px;';
      const label = input.closest('.upload-zone')?.querySelector('h4')?.textContent.trim() || input.id || 'Document';
      item.textContent = `${label}: ${input.files[0]?.name || 'Not uploaded'}`;
      fragment.appendChild(item);
    });
  }

  const edit = document.createElement('button');
  edit.type = 'button';
  edit.className = 'seoas-btn btn-outline';
  edit.textContent = 'Edit Details';
  edit.style.gridColumn = '1 / -1';
  edit.addEventListener('click', () => { currentStep = 1; updateUI(); });
  fragment.appendChild(edit);
  review.appendChild(fragment);
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
