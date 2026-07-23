// smart_schedule.js
// Enterprise Smart Schedule Engine

document.addEventListener('DOMContentLoaded', async () => {
  const btn = document.getElementById('btn-new-registration');
  const countdownEl = document.getElementById('seoas-countdown');
  const examInput = document.getElementById('exam-select');

  if (!btn || !countdownEl || !examInput) return;

  const currentExam = examInput.value;

  try {
    const doc = await firebase.firestore().collection('examSchedules').doc(currentExam).get();
    
    if (!doc.exists) {
      setNotAnnounced(btn, countdownEl);
      return;
    }

    const schedule = doc.data();

    if (schedule.status !== 'Published') {
      setNotAnnounced(btn, countdownEl);
      return;
    }

    // Start live engine
    setInterval(() => updateScheduleEngine(schedule, btn, countdownEl), 1000);
    updateScheduleEngine(schedule, btn, countdownEl);

  } catch (err) {
    console.error("Schedule Engine Error:", err);
    // Handle the case where the user hasn't created a Firestore database yet
    btn.textContent = "Schedule Not Found";
    btn.disabled = true;
    btn.style.background = "#4b5563";
    countdownEl.innerHTML = `<span style="color:var(--seoas-gold); font-size: 0.9em;">(System: Firestore Database is not initialized or access is denied. Please configure it in the Firebase Console and deploy rules.)</span>`;
  }
});

function setNotAnnounced(btn, countdownEl) {
  btn.textContent = "Coming Soon";
  btn.disabled = true;
  countdownEl.textContent = "Important Dates have not been announced.";
}

function setClosed(btn, countdownEl) {
  btn.textContent = "Registration Closed";
  btn.disabled = true;
  btn.style.background = "#4b5563"; // Greyed out
  btn.style.borderColor = "#374151";
  btn.style.cursor = "not-allowed";
  countdownEl.innerHTML = `<span style="color:#ef4444; font-size: 1.2rem; font-weight: bold; background: rgba(239,68,68,0.1); padding: 8px 16px; border-radius: 8px; border: 1px solid rgba(239,68,68,0.3);">Applications are no longer being accepted.</span>`;
}

function updateScheduleEngine(schedule, btn, countdownEl) {
  const now = new Date().getTime();
  const openTime = schedule.registrationOpen ? new Date(schedule.registrationOpen).getTime() : 0;
  const closeTime = schedule.registrationClose ? new Date(schedule.registrationClose).getTime() : 0;

  if (now < openTime) {
    btn.textContent = "Coming Soon";
    btn.disabled = true;
    countdownEl.innerHTML = `Registration Opens In: <span style="color:var(--seoas-emerald)">${formatTimeLeft(openTime - now)}</span>`;
  } else if (now >= openTime && now < closeTime) {
    btn.textContent = "Apply Now";
    btn.disabled = false;
    btn.style.background = "var(--seoas-primary)";
    btn.style.cursor = "pointer";
    countdownEl.innerHTML = `Registration Open. Closing In: <span style="color:red">${formatTimeLeft(closeTime - now)}</span>`;
  } else if (now >= closeTime) {
    setClosed(btn, countdownEl);
  } else {
    setNotAnnounced(btn, countdownEl);
  }
}

function formatTimeLeft(ms) {
  if (ms < 0) return "00:00:00";
  const days = Math.floor(ms / (1000 * 60 * 60 * 24));
  const hours = Math.floor((ms % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const mins = Math.floor((ms % (1000 * 60 * 60)) / (1000 * 60));
  const secs = Math.floor((ms % (1000 * 60)) / 1000);
  
  if (days > 0) return `${days} Days ${hours} Hrs ${mins} Mins`;
  return `${hours} Hrs ${mins} Mins ${secs} Secs`;
}
