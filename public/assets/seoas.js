// seoas.js
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ? '' : 'https://surya-s2f5.onrender.com';


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
  // Add validation logic here later if needed
  if (currentStep < totalSteps) {
    currentStep++;
    updateUI();
    autoSave();
  }
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

// Mock OTP Verification
function mockVerify(type) {
  const statusEl = document.getElementById(`${type.toLowerCase()}-status`);
  statusEl.innerHTML = '<span style="color:var(--seoas-gold)">Sending OTP...</span>';
  setTimeout(() => {
    statusEl.innerHTML = '<span style="color:var(--seoas-emerald)">✅ Verified</span>';
  }, 1500);
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

// Final Submit
function finalSubmit() {
  const submitBtn = document.querySelector('.wizard-step[data-step="9"] button');
  submitBtn.textContent = 'Submitting...';
  submitBtn.disabled = true;

  const data = {};
  const inputs = form.querySelectorAll('input:not([type="file"]), select, textarea');
  inputs.forEach(input => {
    if (input.id) data[input.id] = input.value;
  });

  const formData = new FormData();
  formData.append('data', JSON.stringify(data));

  // Add files
  const fileInputs = form.querySelectorAll('input[type="file"]');
  fileInputs.forEach((input, index) => {
    if (input.files.length > 0) {
      formData.append(`file_${index}`, input.files[0]);
    }
  });

  fetch(API_BASE_URL + '/api/seoas-register', {
    method: 'POST',
    body: formData
  })
  .then(res => res.json())
  .then(resData => {
    if (resData.status === 'ok') {
      const name = document.getElementById('reg-name').value || 'Candidate';
      document.getElementById('conf-name').textContent = name;
      document.getElementById('conf-app-no').textContent = resData.application_number;
      nextStep(); // Go to step 10
      localStorage.removeItem('seoas-draft'); // Clear auto-save
    } else {
      alert("Submission failed: " + resData.message);
      submitBtn.textContent = 'Submit Application Now';
      submitBtn.disabled = false;
    }
  })
  .catch(err => {
    alert("Network error: " + err.message);
    submitBtn.textContent = 'Submit Application Now';
    submitBtn.disabled = false;
  });
}

// Auto Save
function autoSave() {
  if (currentStep >= 10) return;
  const data = {};
  const inputs = form.querySelectorAll('input:not([type="file"]), select, textarea');
  inputs.forEach(input => {
    if (input.id) data[input.id] = input.value;
  });
  localStorage.setItem('seoas-draft', JSON.stringify(data));
  console.log('Auto-saved at', new Date().toLocaleTimeString());
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
