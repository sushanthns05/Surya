// TODO: Replace with your actual Render URL once you have it!
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ? '' : 'https://YOUR-RENDER-APP-URL.onrender.com';

document.addEventListener('DOMContentLoaded', function () {
  const navToggle = document.getElementById('nav-toggle');
  const nav = document.getElementById('site-nav');
  const header = document.querySelector('.site-header');

  if (navToggle && nav) {
    navToggle.addEventListener('click', function () {
      nav.classList.toggle('open');
    });
  }

  const onScroll = function () {
    if (window.scrollY > 24) {
      header && header.classList.add('scrolled');
    } else {
      header && header.classList.remove('scrolled');
    }
  };

  onScroll();
  window.addEventListener('scroll', onScroll);

  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'light') {
    document.documentElement.classList.remove('dark-theme');
  } else {
    document.documentElement.classList.add('dark-theme');
  }

  const themeBtn = document.getElementById('btn-theme');
  if (themeBtn) {
    themeBtn.textContent = document.documentElement.classList.contains('dark-theme') ? '☀️' : '🌙';
    themeBtn.addEventListener('click', function () {
      const isDark = document.documentElement.classList.toggle('dark-theme');
      themeBtn.textContent = isDark ? '☀️' : '🌙';
      localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });
  }

  const searchBtn = document.getElementById('btn-search');
  const searchOverlay = document.getElementById('search-overlay');
  const closeSearch = document.getElementById('close-search');
  const navSearchInput = document.getElementById('search-input');

  if (searchBtn && searchOverlay && closeSearch) {
    searchBtn.addEventListener('click', () => {
      searchOverlay.classList.add('active');
      if (navSearchInput) setTimeout(() => navSearchInput.focus(), 100);
    });
    closeSearch.addEventListener('click', () => searchOverlay.classList.remove('active'));
    searchOverlay.addEventListener('click', (e) => {
      if (e.target === searchOverlay) searchOverlay.classList.remove('active');
    });
  }

  const observer = new IntersectionObserver(function (entries, observerInstance) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observerInstance.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });

  document.querySelectorAll('.reveal, .feature-card, .pricing-card, .testimonial-card, .stat-card, .faq-item, .card').forEach(function (node) {
    observer.observe(node);
  });

  const stats = document.querySelectorAll('.stat-number[data-count]');
  const animateStat = function (node) {
    const count = Number(node.dataset.count || 0);
    const duration = 1400;
    let start = null;

    const step = function (timestamp) {
      if (!start) start = timestamp;
      const progress = Math.min((timestamp - start) / duration, 1);
      node.textContent = Math.round(progress * count).toLocaleString();
      if (progress < 1) {
        window.requestAnimationFrame(step);
      }
    };

    window.requestAnimationFrame(step);
  };

  const statsObserver = new IntersectionObserver(function (entries, statsObserverInstance) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        animateStat(entry.target);
        statsObserverInstance.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  stats.forEach(function (node) {
    statsObserver.observe(node);
  });

  document.querySelectorAll('.faq-question').forEach(function (button) {
    button.addEventListener('click', function () {
      const item = button.closest('.faq-item');
      if (item) {
        item.classList.toggle('open');
      }
    });
  });

  const toTop = document.createElement('button');
  toTop.id = 'back-to-top';
  toTop.type = 'button';
  toTop.title = 'Back to top';
  toTop.textContent = '↑';
  toTop.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
  document.body.appendChild(toTop);

  window.addEventListener('scroll', function () {
    if (window.scrollY > 360) {
      toTop.classList.add('show');
    } else {
      toTop.classList.remove('show');
    }
  });

  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (event) {
      const targetId = anchor.getAttribute('href').slice(1);
      const target = document.getElementById(targetId);
      if (target) {
        event.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // --- Exam Registration Form Handling ---
  const registerForm = document.getElementById('register-form');
  const formStatus = document.getElementById('form-status');

  if (registerForm) {
    registerForm.addEventListener('submit', function (event) {
      event.preventDefault();

      const name = document.getElementById('name').value.trim();
      const email = document.getElementById('email').value.trim();
      const phone = document.getElementById('phone').value.trim();
      const dobVal = document.getElementById('dob').value;
      const gender = document.getElementById('gender').value;
      const category = document.getElementById('exam_category').value;
      const priority_1 = document.getElementById('priority_1').value;
      const priority_2 = document.getElementById('priority_2').value;
      const priority_3 = document.getElementById('priority_3').value;
      const board = document.getElementById('education_board').value;

      // Client-side validations
      if (!name || !email || !phone || !dobVal || !gender || !category || !priority_1 || !priority_2 || !priority_3 || !board) {
        formStatus.textContent = '⚠️ Please fill in all fields.';
        formStatus.style.color = '#ef4444';
        return;
      }

      // Ensure priority cities are distinct
      if (priority_1 === priority_2 || priority_1 === priority_3 || priority_2 === priority_3) {
        formStatus.textContent = '⚠️ Please select three distinct city priorities.';
        formStatus.style.color = '#ef4444';
        return;
      }

      // Check phone number format (10 digits)
      const phoneRegex = /^[0-9]{10}$/;
      if (!phoneRegex.test(phone)) {
        formStatus.textContent = '⚠️ Please enter a valid 10-digit phone number.';
        formStatus.style.color = '#ef4444';
        return;
      }

      // Check candidate's age (must be >= 14 years old)
      const dob = new Date(dobVal);
      const today = new Date();
      let age = today.getFullYear() - dob.getFullYear();
      const m = today.getMonth() - dob.getMonth();
      if (m < 0 || (m === 0 && today.getDate() < dob.getDate())) {
        age--;
      }
      if (age < 14) {
        formStatus.textContent = '⚠️ Candidate must be at least 14 years old to register.';
        formStatus.style.color = '#ef4444';
        return;
      }

      // If validation succeeds, submit via AJAX
      formStatus.textContent = 'Submitting your registration... ⌛';
      formStatus.style.color = '#38bdf8';
      const submitBtn = registerForm.querySelector('button[type="submit"]');
      if (submitBtn) submitBtn.disabled = true;

      const formData = new FormData(registerForm);

      fetch(API_BASE_URL + '/register', {
        method: 'POST',
        body: formData
      })
        .then(response => {
          // Always parse the JSON, even for error responses
          return response.json().then(data => ({ ok: response.ok, data }));
        })
        .then(({ ok, data }) => {
          if (!ok) {
            // Show the server's specific error message (e.g. "already registered")
            formStatus.textContent = '❌ ' + (data.message || 'Registration failed. Please try again.');
            formStatus.style.color = '#ef4444';
            if (submitBtn) submitBtn.disabled = false;
            return;
          }

          // Populate the success slip
          document.getElementById('slip-reg-id').textContent = data.registration_id;
          document.getElementById('slip-name').textContent = data.name;
          document.getElementById('slip-email').textContent = data.email;
          document.getElementById('slip-phone').textContent = data.phone;
          document.getElementById('slip-dob').textContent = data.dob;
          document.getElementById('slip-gender').textContent = data.gender;
          document.getElementById('slip-category').textContent = data.exam_category;
          document.getElementById('slip-priority-1').textContent = data.priority_1;
          document.getElementById('slip-priority-2').textContent = data.priority_2;
          document.getElementById('slip-priority-3').textContent = data.priority_3;
          document.getElementById('slip-allocated-center').textContent = data.allocated_center;
          document.getElementById('slip-board').textContent = data.education_board;

          // Swap form with slip card
          document.getElementById('form-container').style.display = 'none';
          const successContainer = document.getElementById('success-container');
          successContainer.style.display = 'block';
          successContainer.classList.add('visible');

          // Scroll to top of the success card
          successContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        })
        .catch(error => {
          formStatus.textContent = '❌ ' + error.message;
          formStatus.style.color = '#ef4444';
          if (submitBtn) submitBtn.disabled = false;
        });
    });
  }

  // --- Contact Form Handling ---
  const contactForm = document.getElementById('contact-form');
  const contactStatus = document.getElementById('form-status');

  if (contactForm) {
    contactForm.addEventListener('submit', function (event) {
      event.preventDefault();

      const name = document.getElementById('name').value.trim();
      const email = document.getElementById('email').value.trim();
      const subject = document.getElementById('subject').value.trim();
      const message = document.getElementById('message').value.trim();
      const statusDiv = contactForm.querySelector('#form-status') || contactStatus;

      if (!name || !email || !subject || !message) {
        if (statusDiv) {
          statusDiv.textContent = '⚠️ Please fill in all fields.';
          statusDiv.style.color = '#ef4444';
        }
        return;
      }

      if (statusDiv) {
        statusDiv.textContent = 'Sending your message... ⌛';
        statusDiv.style.color = '#38bdf8';
      }

      const submitBtn = contactForm.querySelector('button[type="submit"]');
      if (submitBtn) submitBtn.disabled = true;

      const formData = new FormData(contactForm);

      fetch(API_BASE_URL + '/contact', {
        method: 'POST',
        body: formData
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to send message. Please try again.');
          }
          return response.json();
        })
        .then(data => {
          if (data.status === 'ok') {
            if (statusDiv) {
              statusDiv.textContent = '🚀 Message sent successfully!';
              statusDiv.style.color = '#10b981';
            }
            contactForm.reset();
          } else {
            if (statusDiv) {
              statusDiv.textContent = '❌ ' + (data.message || 'Error occurred.');
              statusDiv.style.color = '#ef4444';
            }
            if (submitBtn) submitBtn.disabled = false;
          }
        })
        .catch(error => {
          if (statusDiv) {
            statusDiv.textContent = '❌ ' + error.message;
            statusDiv.style.color = '#ef4444';
          }
          if (submitBtn) submitBtn.disabled = false;
        });
    });
  }

  // --- Print Handler for Admission Slip ---
  const printBtn = document.getElementById('btn-print-slip');
  if (printBtn) {
    printBtn.addEventListener('click', function () {
      window.print();
    });
  }

  // --- Admin Dashboard Script (Tabs & Search) ---
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');
  const searchInput = document.getElementById('admin-search');

  if (tabBtns.length > 0) {
    tabBtns.forEach(btn => {
      btn.addEventListener('click', function () {
        // Toggle tab button states
        tabBtns.forEach(b => {
          b.classList.remove('active');
          b.style.background = 'transparent';
          b.style.color = 'rgba(255, 255, 255, 0.7)';
        });
        btn.classList.add('active');
        btn.style.background = 'linear-gradient(135deg, #7c3aed, #2563eb)';
        btn.style.color = '#fff';

        // Toggle tab content display
        const activeTabId = btn.dataset.tab;
        tabContents.forEach(content => {
          if (content.id === 'tab-' + activeTabId) {
            content.style.display = 'block';
          } else {
            content.style.display = 'none';
          }
        });

        // Clear search input on tab switch
        if (searchInput) {
          searchInput.value = '';
          filterTable('');
        }
      });
    });
  }

  function filterTable(query) {
    // Find active tab content table body
    const activeTab = document.querySelector('.tab-content:not([style*="display: none"])');
    if (!activeTab) return;

    const rows = activeTab.querySelectorAll('tbody tr');
    rows.forEach(row => {
      const text = row.textContent.toLowerCase();
      if (text.includes(query.toLowerCase())) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    });
  }

  if (searchInput) {
    searchInput.addEventListener('input', function () {
      filterTable(searchInput.value);
    });
  }

  // --- Admin Center Allocation Handler ---
  const allocateSelects = document.querySelectorAll('.allocate-select');
  allocateSelects.forEach(select => {
    select.addEventListener('change', function () {
      const regId = select.dataset.regId;
      const allocatedCenter = select.value;
      const statusSpan = select.nextElementSibling;

      if (statusSpan) {
        statusSpan.textContent = '⏳';
        statusSpan.style.color = '#38bdf8';
      }

      const formData = new FormData();
      formData.append('registration_id', regId);
      formData.append('allocated_center', allocatedCenter);

      fetch(API_BASE_URL + '/admin/allocate-center', {
        method: 'POST',
        body: formData,
        credentials: 'include'       // ensures session cookie is sent cross-origin
      })
        .then(response => response.json().then(data => ({ ok: response.ok, status: response.status, data })))
        .then(({ ok, status, data }) => {
          if (ok && data.status === 'ok') {
            if (statusSpan) {
              statusSpan.textContent = '✅';
              statusSpan.style.color = '#10b981';
              setTimeout(() => { statusSpan.textContent = ''; }, 2000);
            }
          } else {
            console.error('Allocation error', status, data);
            if (statusSpan) {
              statusSpan.title = data.message || 'Error saving allocation';
              statusSpan.textContent = '❌';
              statusSpan.style.color = '#ef4444';
            }
          }
        })
        .catch(error => {
          console.error('Allocation fetch failed:', error);
          if (statusSpan) {
            statusSpan.textContent = '❌';
            statusSpan.style.color = '#ef4444';
          }
        });
    });
  });


  // --- Admin Broadcast Form Handler ---
  const broadcastForm = document.getElementById('broadcast-form');
  const broadcastStatus = document.getElementById('broadcast-status');

  if (broadcastForm) {
    broadcastForm.addEventListener('submit', function (event) {
      event.preventDefault();

      const title = document.getElementById('broadcast-title').value.trim();
      const content = document.getElementById('broadcast-content').value.trim();

      if (!title || !content) {
        if (broadcastStatus) {
          broadcastStatus.textContent = '⚠️ Please enter both a title and message.';
          broadcastStatus.style.color = '#ef4444';
        }
        return;
      }

      // Check document size limit (10MB)
      const docInput = document.getElementById('broadcast-document');
      if (docInput && docInput.files.length > 0) {
        if (docInput.files[0].size > 10 * 1024 * 1024) {
          if (broadcastStatus) {
            broadcastStatus.textContent = '⚠️ Document file size must be less than 10MB.';
            broadcastStatus.style.color = '#ef4444';
          }
          return;
        }
      }

      if (broadcastStatus) {
        broadcastStatus.textContent = 'Publishing broadcast... ⌛';
        broadcastStatus.style.color = '#38bdf8';
      }

      const submitBtn = broadcastForm.querySelector('button[type="submit"]');
      if (submitBtn) submitBtn.disabled = true;

      const formData = new FormData(broadcastForm);

      fetch(API_BASE_URL + '/admin/broadcast', {
        method: 'POST',
        body: formData,
        credentials: 'include'
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to post broadcast. Please check admin authorization.');
          }
          return response.json();
        })
        .then(data => {
          if (data.status === 'ok') {
            if (broadcastStatus) {
              broadcastStatus.textContent = '📢 Broadcast published successfully!';
              broadcastStatus.style.color = '#10b981';
            }
            broadcastForm.reset();
            setTimeout(() => {
              window.location.reload();
            }, 1000);
          } else {
            if (broadcastStatus) {
              broadcastStatus.textContent = '❌ ' + (data.message || 'Error occurred.');
              broadcastStatus.style.color = '#ef4444';
            }
            if (submitBtn) submitBtn.disabled = false;
          }
        })
        .catch(error => {
          if (broadcastStatus) {
            broadcastStatus.textContent = '❌ ' + error.message;
            broadcastStatus.style.color = '#ef4444';
          }
          if (submitBtn) submitBtn.disabled = false;
        });
    });
  }
  const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ? '' : 'https://surya-s2f5.onrender.com';

});
