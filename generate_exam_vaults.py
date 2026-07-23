import os
import re
import csv
import json
from datetime import datetime

VAULTS_DIR = r"e:\Sushanth Projects\SURYA\Vaults"
TEMPLATE_FILE = r"e:\Sushanth Projects\SURYA\templates\SET_Session01_Exam_Portal.html"

EXAMS = [
    {"name": "Vault_SET_Session01.html", "title": "Surya Entrance Test [SET] Session 01 Vault", "code": "SET 01", "header": "Surya Entrance Test (SET) 2027-27", "duration_seconds": 10800},
    {"name": "Vault_SET_Session02.html", "title": "Surya Entrance Test [SET] Session 02 Vault", "code": "SET 02", "header": "Surya Entrance Test (SET) 2027-27", "duration_seconds": 7200},
    {"name": "Vault_SST.html", "title": "Surya Scholarship Test [SST] Vault", "code": "SST", "header": "Surya Scholarship Test (SST) 2027-27", "duration_seconds": 10800},
    {"name": "Vault_SAT.html", "title": "Surya Admission Test [SAT] Vault", "code": "SAT", "header": "Surya Admission Test (SAT) 2027-27", "duration_seconds": 10800},
    {"name": "Vault_SME.html", "title": "Surya Medical Examination [SME] Vault", "code": "SME", "header": "Surya Medical Examination (SME) 2027-27", "duration_seconds": 10800},
    {"name": "Vault_SA.html", "title": "Surya Accountancy [SA] Vault", "code": "SA", "header": "Surya Accountancy (SA) 2027-27", "duration_seconds": 10800},
]

CMS_HTML = """
<!-- MATHJAX & OCR LIBRARIES -->
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<script src="https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js"></script>

<style>
  #vault-cms {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: #0f172a; color: #fff; z-index: 999999;
    font-family: Arial, sans-serif; overflow-y: auto; display: flex;
  }
  .cms-sidebar {
    width: 300px; background: #1e293b; padding: 20px; border-right: 1px solid #334155;
    display: flex; flex-direction: column;
  }
  .cms-main {
    flex: 1; padding: 30px; background: #0f172a; overflow-y: auto;
  }
  .cms-header { border-bottom: 1px solid #334155; padding-bottom: 10px; margin-bottom: 20px; }
  .cms-header h1 { color: #38bdf8; font-size: 24px; margin-bottom: 5px; }
  .cms-header p { color: #94a3b8; font-size: 13px; }
  
  .cms-btn {
    background: #3b82f6; color: white; border: none; padding: 10px 15px; border-radius: 6px;
    cursor: pointer; font-weight: bold; margin-bottom: 10px; text-align: center; width: 100%;
  }
  .cms-btn.success { background: #10b981; }
  .cms-btn.danger { background: #ef4444; }
  .cms-btn.warning { background: #f59e0b; }
  .cms-btn:hover { filter: brightness(1.1); }
  
  .section-list { list-style: none; padding: 0; margin-bottom: 20px; flex: 1; overflow-y: auto; }
  .section-item { 
    background: #334155; padding: 10px; margin-bottom: 5px; border-radius: 4px; 
    cursor: pointer; display: flex; justify-content: space-between;
  }
  .section-item.active { background: #38bdf8; color: #000; font-weight: bold; }
  
  .form-group { margin-bottom: 15px; }
  .form-group label { display: block; margin-bottom: 5px; color: #cbd5e1; font-weight: bold; }
  .form-group input, .form-group textarea, .form-group select {
    width: 100%; padding: 10px; background: #1e293b; border: 1px solid #334155;
    color: white; border-radius: 4px; font-family: monospace;
  }
  
  .q-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(40px, 1fr)); gap: 5px; margin-bottom: 20px; }
  .q-badge {
    background: #334155; padding: 10px; text-align: center; border-radius: 4px; cursor: pointer;
  }
  .q-badge.active { background: #10b981; font-weight: bold; }
  
  .preview-box {
    background: #fff; color: #000; padding: 20px; border-radius: 6px; margin-top: 20px;
    border: 2px dashed #38bdf8; font-family: Arial, sans-serif;
  }
</style>

<div id="vault-cms">
  <div class="cms-sidebar">
    <div class="cms-header">
      <h1>EXAM VAULT</h1>
      <p>Confidential Authoring Studio</p>
    </div>
    
    <button class="cms-btn success" onclick="document.getElementById('import-file').click()">Load Exam (.json)</button>
    <input type="file" id="import-file" style="display:none" accept=".json" onchange="importExam(event)">
    
    <button class="cms-btn" onclick="exportExam()">Save Exam (.json)</button>
    
    <hr style="border-color:#334155; margin: 20px 0;">
    
    <h3 style="color:#94a3b8; margin-bottom: 10px;">Sections</h3>
    <ul class="section-list" id="cms-sections"></ul>
    <button class="cms-btn" style="background: #475569;" onclick="addSection()">+ Add Section</button>
    
    <hr style="border-color:#334155; margin: 20px 0;">
    <button class="cms-btn danger" onclick="launchExam()" style="padding: 15px; font-size: 16px;">LAUNCH EXAM</button>
  </div>
  
  <div class="cms-main" id="cms-main-area" style="display:none;">
    <div style="display:flex; justify-content: space-between; align-items:center;">
      <h2 id="current-section-title" style="color:#38bdf8;">Section Editor</h2>
      <button class="cms-btn danger" style="width:auto;" onclick="deleteSection()">Delete Section</button>
    </div>
    
    <div class="form-group" style="margin-top:20px;">
      <label>Section Name (e.g., Physics)</label>
      <input type="text" id="sec-name" oninput="updateSectionConfig()">
    </div>
    
    <div style="display:flex; gap:10px; margin-bottom:20px;">
      <div class="form-group" style="flex:2; margin:0;">
        <label>Section Type</label>
        <select id="sec-type" onchange="updateSectionConfig()">
          <option value="mcq">MCQ (Single Correct)</option>
          <option value="mc">Multiple Correct (Checkbox)</option>
          <option value="int">Numerical (Integer)</option>
        </select>
      </div>
      <div class="form-group" style="flex:1; margin:0;">
        <label>Correct Marks (+)</label>
        <input type="number" id="sec-pos" oninput="updateSectionConfig()">
      </div>
      <div class="form-group" style="flex:1; margin:0;">
        <label>Negative Marks (-)</label>
        <input type="number" id="sec-neg" oninput="updateSectionConfig()">
      </div>
    </div>
    
    <h3 style="color:#94a3b8; margin: 20px 0 10px;">Questions in this Section</h3>
    <div class="q-list" id="cms-q-list"></div>
    <button class="cms-btn" style="background: #475569; width:auto;" onclick="addQuestion()">+ Add Question</button>
    
    <div id="q-editor" style="display:none; margin-top:30px; background:#1e293b; padding:20px; border-radius:8px;">
      <div style="display:flex; justify-content: space-between;">
        <h3 style="color:#10b981; margin-bottom: 15px;">Edit Question <span id="q-number-disp"></span></h3>
        <button class="cms-btn danger" style="width:auto; padding:5px 10px;" onclick="deleteQuestion()">Delete Q</button>
      </div>
      
      <p style="font-size:12px; color:#94a3b8; margin-bottom:10px;">Use MathJax for math: <code>\\( x^2 \\)</code>. Type <code>[IMAGE]</code> in the text to place the attached image inline.</p>
      
      <div class="form-group">
        <div style="display:flex; justify-content: space-between; align-items:center; margin-bottom: 5px;">
           <label style="margin:0;">Question Text</label>
           <button class="cms-btn warning" style="width:auto; padding:5px; margin:0;" onclick="document.getElementById('q-ocr-input').click()">Upload Image to Extract Text</button>
           <input type="file" id="q-ocr-input" accept="image/*" style="display:none" onchange="handleOCRUpload(event)">
        </div>
        <textarea id="q-text" rows="4" oninput="updatePreview()"></textarea>
      </div>
      
      <div class="form-group">
        <label>Attach Image (Optional)</label>
        <input type="file" id="q-img" accept="image/*" onchange="handleImageUpload(event)">
        <img id="q-img-preview" style="max-height: 100px; margin-top:10px; display:none;">
        <button class="cms-btn danger" id="q-img-remove" style="width:auto; padding:5px; margin-top:10px; display:none;" onclick="removeImage()">Remove Image</button>
      </div>
      
      <div id="q-options-container">
        <div style="display:flex; gap:20px;">
          <div class="form-group" style="flex:1"><label>Option A</label><input type="text" id="q-opt-a" oninput="updatePreview()"></div>
          <div class="form-group" style="flex:1"><label>Option B</label><input type="text" id="q-opt-b" oninput="updatePreview()"></div>
        </div>
        <div style="display:flex; gap:20px;">
          <div class="form-group" style="flex:1"><label>Option C</label><input type="text" id="q-opt-c" oninput="updatePreview()"></div>
          <div class="form-group" style="flex:1"><label>Option D</label><input type="text" id="q-opt-d" oninput="updatePreview()"></div>
        </div>
      </div>
      
      <div class="form-group" id="q-ans-mcq-container">
        <label>Correct Answer (Single)</label>
        <select id="q-ans-mcq">
          <option value="0">Option A</option>
          <option value="1">Option B</option>
          <option value="2">Option C</option>
          <option value="3">Option D</option>
        </select>
      </div>
      
      <div class="form-group" id="q-ans-mc-container" style="display:none;">
        <label>Correct Answers (Multiple)</label>
        <div>
          <label style="display:inline; margin-right:10px;"><input type="checkbox" id="q-ans-mc-0"> A</label>
          <label style="display:inline; margin-right:10px;"><input type="checkbox" id="q-ans-mc-1"> B</label>
          <label style="display:inline; margin-right:10px;"><input type="checkbox" id="q-ans-mc-2"> C</label>
          <label style="display:inline; margin-right:10px;"><input type="checkbox" id="q-ans-mc-3"> D</label>
        </div>
      </div>
      
      <div class="form-group" id="q-ans-int-container" style="display:none;">
        <label>Correct Integer Answer</label>
        <input type="number" id="q-ans-int" placeholder="e.g. 45 or -12">
      </div>
      
      <button class="cms-btn success" onclick="saveQuestion()">Save Question</button>
      
      <h4 style="color:#94a3b8; margin-top:20px;">Live Preview</h4>
      <div class="preview-box" id="q-preview"></div>
    </div>
  </div>
</div>

<script>
  let examData = { sections: [] };
  let curSecIdx = -1;
  let curQIdx = -1;
  
  function renderSections() {
    const list = document.getElementById('cms-sections');
    list.innerHTML = '';
    examData.sections.forEach((sec, idx) => {
      const li = document.createElement('li');
      li.className = `section-item ${idx === curSecIdx ? 'active' : ''}`;
      li.style.display = 'flex';
      li.style.justifyContent = 'space-between';
      
      const nameSpan = document.createElement('span');
      nameSpan.innerText = sec.name;
      li.appendChild(nameSpan);
      
      const controls = document.createElement('div');
      
      if (idx > 0) {
          const upBtn = document.createElement('button');
          upBtn.innerHTML = '&#9650;';
          upBtn.style.background = 'transparent';
          upBtn.style.border = 'none';
          upBtn.style.color = '#94a3b8';
          upBtn.style.cursor = 'pointer';
          upBtn.style.marginRight = '5px';
          upBtn.onclick = (e) => {
              e.stopPropagation();
              moveSection(idx, -1);
          };
          controls.appendChild(upBtn);
      }
      if (idx < examData.sections.length - 1) {
          const downBtn = document.createElement('button');
          downBtn.innerHTML = '&#9660;';
          downBtn.style.background = 'transparent';
          downBtn.style.border = 'none';
          downBtn.style.color = '#94a3b8';
          downBtn.style.cursor = 'pointer';
          downBtn.onclick = (e) => {
              e.stopPropagation();
              moveSection(idx, 1);
          };
          controls.appendChild(downBtn);
      }
      
      li.appendChild(controls);
      li.onclick = () => selectSection(idx);
      list.appendChild(li);
    });
    if (examData.sections.length === 0) {
      document.getElementById('cms-main-area').style.display = 'none';
    }
  }
  
  function moveSection(idx, direction) {
      const temp = examData.sections[idx];
      examData.sections[idx] = examData.sections[idx + direction];
      examData.sections[idx + direction] = temp;
      if (curSecIdx === idx) {
          curSecIdx = idx + direction;
      } else if (curSecIdx === idx + direction) {
          curSecIdx = idx;
      }
      renderSections();
  }
  
  function addSection() {
    examData.sections.push({ 
        name: `Section ${examData.sections.length + 1}`,
        type: 'mcq',
        marks: { pos: 4, neg: 1 },
        questions: [] 
    });
    selectSection(examData.sections.length - 1);
  }
  
  function selectSection(idx) {
    curSecIdx = idx;
    curQIdx = -1;
    document.getElementById('cms-main-area').style.display = 'block';
    
    const sec = examData.sections[idx];
    document.getElementById('sec-name').value = sec.name;
    document.getElementById('sec-type').value = sec.type || 'mcq';
    document.getElementById('sec-pos').value = sec.marks ? sec.marks.pos : 4;
    document.getElementById('sec-neg').value = sec.marks ? sec.marks.neg : 1;
    
    document.getElementById('current-section-title').innerText = `Editing: ${sec.name}`;
    document.getElementById('q-editor').style.display = 'none';
    renderSections();
    renderQuestions();
  }
  
  function updateSectionConfig() {
    const sec = examData.sections[curSecIdx];
    sec.name = document.getElementById('sec-name').value;
    sec.type = document.getElementById('sec-type').value;
    if (!sec.marks) sec.marks = { pos: 4, neg: 1 };
    sec.marks.pos = parseInt(document.getElementById('sec-pos').value) || 0;
    sec.marks.neg = parseInt(document.getElementById('sec-neg').value) || 0;
    renderSections();
  }
  
  function deleteSection() {
    if (confirm("Delete this entire section?")) {
      examData.sections.splice(curSecIdx, 1);
      curSecIdx = -1;
      renderSections();
      document.getElementById('cms-main-area').style.display = 'none';
    }
  }
  
  function renderQuestions() {
    const list = document.getElementById('cms-q-list');
    list.innerHTML = '';
    const qs = examData.sections[curSecIdx].questions;
    qs.forEach((q, idx) => {
      const d = document.createElement('div');
      d.className = `q-badge ${idx === curQIdx ? 'active' : ''}`;
      d.innerText = `Q${idx + 1}`;
      d.onclick = () => selectQuestion(idx);
      list.appendChild(d);
    });
  }
  
  function addQuestion() {
    const sec = examData.sections[curSecIdx];
    let defaultAns = "0";
    if (sec.type === 'mc') defaultAns = [];
    if (sec.type === 'int') defaultAns = 0;
    
    sec.questions.push({
      text: "New Question", image: null, opts: ["A", "B", "C", "D"], ans: defaultAns
    });
    selectQuestion(sec.questions.length - 1);
  }
  
  function selectQuestion(idx) {
    curQIdx = idx;
    renderQuestions();
    const sec = examData.sections[curSecIdx];
    const q = sec.questions[idx];
    document.getElementById('q-editor').style.display = 'block';
    document.getElementById('q-number-disp').innerText = idx + 1;
    
    document.getElementById('q-text').value = q.text || '';
    document.getElementById('q-opt-a').value = q.opts[0] || '';
    document.getElementById('q-opt-b').value = q.opts[1] || '';
    document.getElementById('q-opt-c').value = q.opts[2] || '';
    document.getElementById('q-opt-d').value = q.opts[3] || '';
    
    if (sec.type === 'int') {
        document.getElementById('q-options-container').style.display = 'none';
        document.getElementById('q-ans-mcq-container').style.display = 'none';
        document.getElementById('q-ans-mc-container').style.display = 'none';
        document.getElementById('q-ans-int-container').style.display = 'block';
        document.getElementById('q-ans-int').value = q.ans !== undefined ? q.ans : '';
    } else if (sec.type === 'mc') {
        document.getElementById('q-options-container').style.display = 'block';
        document.getElementById('q-ans-mcq-container').style.display = 'none';
        document.getElementById('q-ans-int-container').style.display = 'none';
        document.getElementById('q-ans-mc-container').style.display = 'block';
        const arr = Array.isArray(q.ans) ? q.ans : [];
        for (let i = 0; i < 4; i++) {
            document.getElementById('q-ans-mc-' + i).checked = arr.includes(String(i)) || arr.includes(i);
        }
    } else {
        document.getElementById('q-options-container').style.display = 'block';
        document.getElementById('q-ans-mc-container').style.display = 'none';
        document.getElementById('q-ans-int-container').style.display = 'none';
        document.getElementById('q-ans-mcq-container').style.display = 'block';
        document.getElementById('q-ans-mcq').value = q.ans !== undefined ? q.ans : "0";
    }
    
    if (q.image) {
      document.getElementById('q-img-preview').src = q.image;
      document.getElementById('q-img-preview').style.display = 'block';
      document.getElementById('q-img-remove').style.display = 'inline-block';
    } else {
      document.getElementById('q-img-preview').style.display = 'none';
      document.getElementById('q-img-remove').style.display = 'none';
    }
    
    updatePreview();
  }
  
  function handleImageUpload(e) {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function(event) {
      const b64 = event.target.result;
      examData.sections[curSecIdx].questions[curQIdx].image = b64;
      document.getElementById('q-img-preview').src = b64;
      document.getElementById('q-img-preview').style.display = 'block';
      document.getElementById('q-img-remove').style.display = 'inline-block';
      updatePreview();
    };
    reader.readAsDataURL(file);
  }
  
  function removeImage() {
    examData.sections[curSecIdx].questions[curQIdx].image = null;
    document.getElementById('q-img').value = '';
    document.getElementById('q-img-preview').style.display = 'none';
    document.getElementById('q-img-remove').style.display = 'none';
    updatePreview();
  }
  
  function updatePreview() {
    const text = document.getElementById('q-text').value;
    const optA = document.getElementById('q-opt-a').value;
    const optB = document.getElementById('q-opt-b').value;
    const optC = document.getElementById('q-opt-c').value;
    const optD = document.getElementById('q-opt-d').value;
    
    let html = `<div>${text.replace(/\\n/g, '<br>')}</div>`;
    if (examData.sections[curSecIdx].questions[curQIdx].image) {
       const imgTag = `<img src="${examData.sections[curSecIdx].questions[curQIdx].image}" style="max-width:100%; max-height:200px; margin:10px 0; display:block;">`;
       if (html.includes('[IMAGE]')) {
           html = html.replace('[IMAGE]', imgTag);
       } else {
           html += imgTag;
       }
    }
    const sec = examData.sections[curSecIdx];
    if (sec.type !== 'int') {
      html += `
        <ol type="A" style="margin-top:15px; padding-left:20px;">
          <li>${optA}</li><li>${optB}</li><li>${optC}</li><li>${optD}</li>
        </ol>
      `;
    }
    const box = document.getElementById('q-preview');
    box.innerHTML = html;
    if (window.MathJax) { MathJax.typesetPromise([box]); }
  }
  
  async function handleOCRUpload(e) {
    const file = e.target.files[0];
    if (!file) return;
    const btn = document.querySelector('button[onclick="document.getElementById(\\'q-ocr-input\\').click()"]');
    const originalText = btn.innerText;
    btn.disabled = true;
    btn.innerText = "Extracting... Please wait";
    
    const reader = new FileReader();
    reader.onload = async function(event) {
        try {
          const result = await Tesseract.recognize(event.target.result, 'eng');
          if (result && result.data && result.data.text) {
            const textInput = document.getElementById('q-text');
            textInput.value += (textInput.value ? '\\n\\n' : '') + result.data.text.trim();
            const q = examData.sections[curSecIdx].questions[curQIdx];
            q.text = textInput.value;
            updatePreview();
          }
        } catch (err) {
          console.error(err);
          alert("OCR Extraction Failed: " + err.message);
        } finally {
          btn.disabled = false;
          btn.innerText = originalText;
          e.target.value = ''; // Reset input
        }
    };
    reader.readAsDataURL(file);
  }
  
  function saveQuestion() {
    const sec = examData.sections[curSecIdx];
    const q = sec.questions[curQIdx];
    q.text = document.getElementById('q-text').value;
    q.opts = [
      document.getElementById('q-opt-a').value,
      document.getElementById('q-opt-b').value,
      document.getElementById('q-opt-c').value,
      document.getElementById('q-opt-d').value
    ];
    
    if (sec.type === 'int') {
        q.ans = parseInt(document.getElementById('q-ans-int').value) || 0;
    } else if (sec.type === 'mc') {
        const arr = [];
        for (let i = 0; i < 4; i++) {
            if (document.getElementById('q-ans-mc-' + i).checked) arr.push(String(i));
        }
        q.ans = arr;
    } else {
        q.ans = document.getElementById('q-ans-mcq').value;
    }
    alert("Question saved!");
  }
  
  function deleteQuestion() {
    if (confirm("Delete this question?")) {
      examData.sections[curSecIdx].questions.splice(curQIdx, 1);
      document.getElementById('q-editor').style.display = 'none';
      curQIdx = -1;
      renderQuestions();
    }
  }
  
  function exportExam() {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(examData));
    const a = document.createElement('a');
    a.href = dataStr;
    a.download = "Surya_Confidential_Exam.json";
    document.body.appendChild(a);
    a.click();
    a.remove();
  }
  
  function importExam(e) {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function(event) {
      try {
        examData = JSON.parse(event.target.result);
        curSecIdx = -1;
        curQIdx = -1;
        document.getElementById('cms-main-area').style.display = 'none';
        renderSections();
        alert("Exam loaded successfully!");
      } catch (err) {
        alert("Invalid exam file.");
      }
    };
    reader.readAsText(file);
  }
  
  function launchExam() {
    if (examData.sections.length === 0) { alert("Add at least one section before launching."); return; }
    
    // Inject EXAM_SECTIONS and QUESTIONS into the TCS window
    window.EXAM_SECTIONS = [];
    window.QUESTIONS = {};
    
    let totalQuestions = 0;
    let totalMarks = 0;
    let dynamicPatternTable = `
      <tr style="background:#003087;color:white;">
        <th style="padding:7px 10px;text-align:left;">Section</th>
        <th style="padding:7px 10px;text-align:left;">Type</th>
        <th style="padding:7px 10px;text-align:left;">Questions</th>
        <th style="padding:7px 10px;text-align:left;">Correct</th>
        <th style="padding:7px 10px;text-align:left;">Wrong</th>
        <th style="padding:7px 10px;text-align:left;">Unattempted</th>
      </tr>`;
    
    examData.sections.forEach((sec, idx) => {
      const secId = `sec${idx}`;
      const qCount = sec.questions.length;
      totalQuestions += qCount;
      const correctM = sec.marks ? sec.marks.pos : 4;
      const wrongM = sec.marks ? sec.marks.neg : 1;
      totalMarks += (qCount * correctM);
      
      window.EXAM_SECTIONS.push({
        id: secId,
        label: sec.name,
        secName: sec.name,
        subject: sec.name,
        type: sec.type || 'mcq',
        qCount: qCount,
        marks: sec.marks ? { correct: correctM, wrong: wrongM } : { correct: 4, wrong: 1 }
      });
      
      const typeStr = sec.type === 'int' ? 'Numerical (Integer)' : (sec.type === 'mc' ? 'Multiple Correct' : 'Multiple Choice');
      
      dynamicPatternTable += `
        <tr>
          <td style="padding:6px 10px;border:1px solid #ccc;font-weight:700;">${sec.name}</td>
          <td style="padding:6px 10px;border:1px solid #ccc;">${typeStr}</td>
          <td style="padding:6px 10px;border:1px solid #ccc;">${qCount}</td>
          <td style="padding:6px 10px;border:1px solid #ccc;color:#2a8a2a;font-weight:700;">+${correctM}</td>
          <td style="padding:6px 10px;border:1px solid #ccc;color:#c00;font-weight:700;">-${wrongM}</td>
          <td style="padding:6px 10px;border:1px solid #ccc;">0</td>
        </tr>`;
      
      window.QUESTIONS[secId] = sec.questions.map(q => {
        let qHtml = `<div>${q.text.replace(/\\n/g, '<br>')}</div>`;
        if (q.image) {
            const imgTag = `<img src="${q.image}" style="max-width:100%; max-height:200px; margin:10px 0; display:block;">`;
            if (qHtml.includes('[IMAGE]')) {
                qHtml = qHtml.replace('[IMAGE]', imgTag);
            } else {
                qHtml += imgTag;
            }
        }
        return { q: qHtml, opts: q.opts, ans: q.ans };
      });
    });
    
    // Overwrite the instructions tables
    const tables = document.querySelectorAll('#instructionsScreen table');
    if(tables.length >= 2) {
      tables[0].innerHTML = `
        <tr style="background:#f5f5f5;"><td style="padding:6px 10px;border:1px solid #ccc;">Examination</td><td style="padding:6px 10px;border:1px solid #ccc;font-weight:bold;">Surya Examination Vault</td></tr>
        <tr><td style="padding:6px 10px;border:1px solid #ccc;">Duration</td><td style="padding:6px 10px;border:1px solid #ccc;">${window.EXAM_DURATION_SECONDS ? (window.EXAM_DURATION_SECONDS / 60) + ' Minutes' : 'Variable (As instructed)'}</td></tr>
        <tr style="background:#f5f5f5;"><td style="padding:6px 10px;border:1px solid #ccc;">Total Questions</td><td style="padding:6px 10px;border:1px solid #ccc;">${totalQuestions}</td></tr>
        <tr><td style="padding:6px 10px;border:1px solid #ccc;">Total Marks</td><td style="padding:6px 10px;border:1px solid #ccc;">${totalMarks}</td></tr>
      `;
      tables[1].innerHTML = dynamicPatternTable;
    }
    
    document.getElementById('vault-cms').style.display = 'none';
    
    // Attempt to trigger TCS init
    try {
      state.currentSec = 0;
      state.currentQ = 0;
      state.status = {};
      initStatus();
      renderSectionsHeader();
      renderStatusPanel();
      renderQuestion();
      document.getElementById('loginScreen').style.display = 'block';
    } catch(e) {
      console.error(e);
      alert("Failed to hook into execution engine.");
    }
  }
</script>
"""

def generate():
    if not os.path.exists(VAULTS_DIR):
        os.makedirs(VAULTS_DIR)

    if not os.path.exists(TEMPLATE_FILE):
        print(f"Error: Template {TEMPLATE_FILE} not found.")
        return

    # Parse candidates globally
    all_candidates = []
    csv_path = r"e:\Sushanth Projects\SURYA\registrations.csv"
    if os.path.exists(csv_path):
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                all_candidates.append(row)

    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        tcs_html = f.read()

    tcs_html = re.sub(r'<div class="screen active" id="loginScreen">', r'<div class="screen" id="loginScreen" style="display:none;">', tcs_html)
    tcs_html = re.sub(r'<body[^>]*>', lambda m: m.group(0) + "\n" + CMS_HTML, tcs_html, count=1)
    
    tcs_html = tcs_html.replace("const EXAM_SECTIONS =", "window.EXAM_SECTIONS =")
    tcs_html = tcs_html.replace("const QUESTIONS = buildQuestions();", "window.QUESTIONS = buildQuestions();")
    tcs_html = tcs_html.replace("const state =", "window.state =")

    for exam in EXAMS:
        final_html = tcs_html
        final_html = re.sub(r'<title>.*?</title>', f"<title>{exam['title']}</title>", final_html)
        
        # Replace hardcoded headers in the UI
        final_html = final_html.replace("Surya Entrance Test (SET) 2027-27", exam['header'])
        final_html = final_html.replace("Surya Entrance Test [SET] Session 01", exam['title'].replace(" Vault", ""))
        final_html = final_html.replace("SET Session 01", exam['code'])
        final_html = final_html.replace("SURYA ENTRANCE TEST", exam['header'].upper())
        final_html = final_html.replace(">SET<", f">{exam['code'].split(' ')[0]}<")
        
        # Filter candidates for this specific exam
        vault_candidates = {}
        for row in all_candidates:
            if row.get("exam_category", "").strip().upper() == exam["code"].upper():
                reg_id = row.get("registration_id", "").strip().upper()
                if not reg_id: continue
                
                dob_raw = row.get("dob", "").strip()
                phone = row.get("phone", "").strip()
                passwords = []
                
                try:
                    dt = datetime.strptime(dob_raw, "%Y-%m-%d")
                    passwords.append(dt.strftime("%d%b%Y").lower())
                    passwords.append(dt.strftime("%d-%m-%Y").lower())
                    passwords.append(dt.strftime("%d%m%Y").lower())
                except ValueError:
                    if dob_raw: passwords.append(dob_raw.lower())
                
                if phone: passwords.append(phone.lower())
                
                vault_candidates[reg_id] = {
                    "name": row.get("name", "Candidate"),
                    "passwords": passwords
                }
        
        candidates_json = json.dumps(vault_candidates)
        
        # Inject candidates, duration, and MathJax wrapper
        duration = exam.get('duration_seconds', 10800)
        mj_wrapper = """
        <script>
        window.EXAM_DURATION_SECONDS = %d;
        window.CANDIDATES_DATA = %s;
        const _origRenderQuestion = window.renderQuestion;
        window.renderQuestion = function() {
            _origRenderQuestion();
            if (window.MathJax) {
                MathJax.typesetPromise([document.getElementById('questionText'), document.getElementById('answerArea')]).catch(e=>console.log(e));
            }
        };
        </script>
        """ % (duration, candidates_json)
        
        final_html = final_html.replace("</body>", f"{mj_wrapper}\n</body>")
        
        filepath = os.path.join(VAULTS_DIR, exam["name"])
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(final_html)
        print(f"Created Vault: {filepath}")

if __name__ == "__main__":
    generate()
