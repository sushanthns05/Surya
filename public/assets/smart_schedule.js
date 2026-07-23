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
    btn.textContent = "Error loading schedule";
    btn.disabled = true;
  }
});

function setNotAnnounced(btn, countdownEl) {
  btn.textContent = "Coming Soon";
  btn.disabled = true;
  countdownEl.textContent = "Important Dates have not been announced.";
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
    countdownEl.innerHTML = `Registration Open. Closing In: <span style="color:red">${formatTimeLeft(closeTime - now)}</span>`;
  } else if (now >= closeTime) {
    btn.textContent = "Registration Closed";
    btn.disabled = true;
    countdownEl.textContent = "Applications are no longer being accepted.";
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
