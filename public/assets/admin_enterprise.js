// Admin Enterprise Dashboard Logic
document.addEventListener('DOMContentLoaded', () => {
  // Initialize Lucide icons
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }

  // Set up Page Routing (Sidebar Navigation)
  const navItems = document.querySelectorAll('.admin-nav-item');
  const pages = document.querySelectorAll('.admin-page');

  navItems.forEach(item => {
    item.addEventListener('click', (e) => {
      const targetPageId = item.getAttribute('data-page');
      if (!targetPageId) return;
      
      navItems.forEach(nav => nav.classList.remove('active'));
      item.classList.add('active');

      pages.forEach(page => {
        page.classList.remove('active');
        if (page.id === targetPageId) {
          page.classList.add('active');
          // Re-trigger animation
          page.style.animation = 'none';
          page.offsetHeight; // trigger reflow
          page.style.animation = null;
        }
      });
    });
  });

  // Animated Counters for Analytics
  const counters = document.querySelectorAll('.counter-value');
  counters.forEach(counter => {
    const target = parseInt(counter.getAttribute('data-target') || 0);
    const duration = 1500; 
    const stepTime = Math.abs(Math.floor(duration / (target || 1)));
    let current = 0;
    
    if (target > 0) {
      const timer = setInterval(() => {
        current += Math.ceil(target / 20);
        if (current >= target) {
          counter.textContent = target.toLocaleString();
          clearInterval(timer);
        } else {
          counter.textContent = current.toLocaleString();
        }
      }, stepTime);
    } else {
      counter.textContent = "0";
    }
  });

  // --- Table Enhancement (Sorting, Filtering, Pagination, Drawer) ---
  const tbody = document.getElementById('registrations-body');
  if (tbody) {
    // 1. Parse existing table rows into JS objects
    const originalRows = Array.from(tbody.querySelectorAll('tr.table-row-item'));
    let data = originalRows.map((tr, index) => {
      const cells = Array.from(tr.querySelectorAll('td'));
      return {
        id: cells[0]?.textContent.trim(),
        name: cells[1]?.textContent.trim() || 'Unknown',
        email: cells[2]?.textContent.trim(),
        phone: cells[3]?.textContent.trim(),
        dob: cells[4]?.textContent.trim(),
        gender: cells[5]?.textContent.trim(),
        exam: cells[6]?.textContent.trim() || 'N/A',
        p1: cells[7]?.textContent.trim(),
        p2: cells[8]?.textContent.trim(),
        p3: cells[9]?.textContent.trim(),
        center: cells[10]?.querySelector('select') ? cells[10].querySelector('select').value : cells[10]?.textContent.trim(),
        board: cells[11]?.textContent.trim(),
        status: 'Pending', // Default
        originalRowElement: tr,
        rawCells: cells
      };
    });

    let currentData = [...data];
    let currentPage = 1;
    let rowsPerPage = 10;

    const renderTable = () => {
      tbody.innerHTML = '';
      const start = (currentPage - 1) * rowsPerPage;
      const end = start + rowsPerPage;
      const paginatedData = currentData.slice(start, end);

      if (paginatedData.length === 0) {
        tbody.innerHTML = '<tr><td colspan="10" style="text-align:center; padding:40px;">No records found.</td></tr>';
        return;
      }

      paginatedData.forEach(row => {
        // Create new row wrapper for click events (drawer)
        const tr = document.createElement('tr');
        tr.className = 'table-row-item';
        
        // Add Checkbox column
        const tdCheck = document.createElement('td');
        tdCheck.innerHTML = `<input type="checkbox" class="admin-checkbox row-select" value="${row.id}" onclick="event.stopPropagation()">`;
        tr.appendChild(tdCheck);

        // Copy original cells
        row.rawCells.forEach((cell, idx) => {
          const newCell = document.createElement('td');
          newCell.innerHTML = cell.innerHTML;
          // Apply badges for specific columns based on headers in admin.html
          if (idx === 4) { // Assuming index 4 is an important status or exam type
            newCell.innerHTML = `<span class="badge badge-info">${cell.textContent.trim()}</span>`;
          }
          tr.appendChild(newCell);
        });

        // Add action column
        const tdAction = document.createElement('td');
        tdAction.innerHTML = `
          <div style="display:flex; gap:8px;">
            <button class="admin-btn outline icon-only" title="View Profile" onclick="openCandidateDrawer('${row.id}')">
              <i data-lucide="eye"></i>
            </button>
            <button class="admin-btn outline icon-only" style="color:var(--admin-warning); border-color:rgba(245,158,11,0.3)" title="Edit" onclick="editCandidate('${row.id}')">
              <i data-lucide="edit-2"></i>
            </button>
          </div>
        `;
        tr.appendChild(tdAction);

        // Make row clickable to open drawer
        tr.addEventListener('click', (e) => {
          if (!e.target.closest('button') && !e.target.closest('select') && !e.target.closest('input')) {
            openCandidateDrawer(row.id);
          }
        });

        tbody.appendChild(tr);
      });

      if (typeof lucide !== 'undefined') lucide.createIcons();
      updatePagination();
    };

    const updatePagination = () => {
      const totalPages = Math.ceil(currentData.length / rowsPerPage);
      const paginationEl = document.getElementById('table-pagination');
      if (!paginationEl) return;
      paginationEl.innerHTML = `
        <div style="color: var(--admin-muted); font-size: 0.9rem;">
          Showing ${currentData.length === 0 ? 0 : (currentPage - 1) * rowsPerPage + 1} to ${Math.min(currentPage * rowsPerPage, currentData.length)} of ${currentData.length} entries
        </div>
        <div style="display: flex; gap: 8px;">
          <button class="admin-btn outline" ${currentPage === 1 ? 'disabled' : ''} onclick="changePage(-1)">Previous</button>
          <button class="admin-btn outline" ${currentPage === totalPages || totalPages === 0 ? 'disabled' : ''} onclick="changePage(1)">Next</button>
        </div>
      `;
    };

    window.changePage = (dir) => {
      currentPage += dir;
      renderTable();
    };

    // Filter Logic
    const searchInput = document.getElementById('admin-search-advanced');
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();
        currentData = data.filter(r => 
          r.name.toLowerCase().includes(term) || 
          r.id.toLowerCase().includes(term) || 
          r.email.toLowerCase().includes(term)
        );
        currentPage = 1;
        renderTable();
      });
    }

    // Initial render
    renderTable();

    // Drawer Logic
    window.openCandidateDrawer = (id) => {
      const row = data.find(r => r.id === id);
      if (!row) return;

      document.getElementById('drawer-candidate-name').textContent = row.name;
      document.getElementById('drawer-candidate-id').textContent = id;
      document.getElementById('drawer-candidate-initial').textContent = row.name.charAt(0).toUpperCase();

      // Populate mock data grids
      document.getElementById('drawer-content-personal').innerHTML = `
        <div class="detail-grid">
          <div class="detail-item"><span class="detail-label">Email</span><span class="detail-value">${row.email}</span></div>
          <div class="detail-item"><span class="detail-label">Mobile</span><span class="detail-value">${row.phone}</span></div>
          <div class="detail-item"><span class="detail-label">Exam Applied</span><span class="detail-value">${row.exam}</span></div>
          <div class="detail-item"><span class="detail-label">DOB</span><span class="detail-value">${row.dob}</span></div>
          <div class="detail-item"><span class="detail-label">Gender</span><span class="detail-value">${row.gender}</span></div>
          <div class="detail-item"><span class="detail-label">Education Board</span><span class="detail-value">${row.board}</span></div>
          <div class="detail-item"><span class="detail-label">Priority 1</span><span class="detail-value">${row.p1}</span></div>
          <div class="detail-item"><span class="detail-label">Priority 2</span><span class="detail-value">${row.p2}</span></div>
          <div class="detail-item"><span class="detail-label">Priority 3</span><span class="detail-value">${row.p3}</span></div>
          <div class="detail-item"><span class="detail-label">Status</span><span class="detail-value"><span class="badge badge-success">Verified</span></span></div>
        </div>
      `;

      document.getElementById('drawer-overlay').classList.add('active');
      document.getElementById('candidate-drawer').classList.add('active');
    };

    window.editCandidate = (id) => {
      const row = data.find(r => r.id === id);
      if (!row) return;
      
      document.getElementById('drawer-candidate-name').textContent = "Edit: " + row.name;
      document.getElementById('drawer-candidate-id').textContent = id;
      document.getElementById('drawer-candidate-initial').textContent = row.name.charAt(0).toUpperCase();

      document.getElementById('drawer-content-personal').innerHTML = `
        <div class="detail-grid">
          <div class="detail-item"><span class="detail-label">Name</span><input class="admin-input" id="edit-name" value="${row.name}"></div>
          <div class="detail-item"><span class="detail-label">Email</span><input class="admin-input" id="edit-email" value="${row.email}"></div>
          <div class="detail-item"><span class="detail-label">Mobile</span><input class="admin-input" id="edit-phone" value="${row.phone}"></div>
          <div class="detail-item"><span class="detail-label">DOB</span><input class="admin-input" id="edit-dob" value="${row.dob}"></div>
          <div class="detail-item"><span class="detail-label">Gender</span><input class="admin-input" id="edit-gender" value="${row.gender}"></div>
          <div class="detail-item"><span class="detail-label">Education Board</span><input class="admin-input" id="edit-board" value="${row.board}"></div>
          <div class="detail-item" style="grid-column: span 2; margin-top:10px;">
            <button class="admin-btn primary" onclick="saveCandidateEdits('${id}')">Save Changes</button>
          </div>
        </div>
      `;

      document.getElementById('drawer-overlay').classList.add('active');
      document.getElementById('candidate-drawer').classList.add('active');
      
      // Select the first tab automatically
      document.querySelector('.drawer-tab[data-target="drawer-content-personal"]').click();
    };

    window.saveCandidateEdits = (id) => {
      const row = data.find(r => r.id === id);
      if (!row) return;
      
      row.name = document.getElementById('edit-name').value;
      row.email = document.getElementById('edit-email').value;
      row.phone = document.getElementById('edit-phone').value;
      row.dob = document.getElementById('edit-dob').value;
      row.gender = document.getElementById('edit-gender').value;
      row.board = document.getElementById('edit-board').value;
      
      // Update the rawCells so renderTable renders the updated value
      row.rawCells[1].textContent = row.name;
      row.rawCells[2].textContent = row.email;
      row.rawCells[3].textContent = row.phone;
      row.rawCells[4].textContent = row.dob;
      row.rawCells[5].textContent = row.gender;
      row.rawCells[11].textContent = row.board;
      
      renderTable();
      closeCandidateDrawer();
      alert("Candidate updated successfully (Mock Enterprise Save).");
    };

    window.closeCandidateDrawer = () => {
      document.getElementById('drawer-overlay').classList.remove('active');
      document.getElementById('candidate-drawer').classList.remove('active');
    };
    
    document.getElementById('drawer-overlay')?.addEventListener('click', closeCandidateDrawer);
    
    // Drawer Tabs
    const drawerTabs = document.querySelectorAll('.drawer-tab');
    const drawerSections = document.querySelectorAll('.drawer-section');
    drawerTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        drawerTabs.forEach(t => t.classList.remove('active'));
        drawerSections.forEach(s => s.classList.remove('active'));
        tab.classList.add('active');
        document.getElementById(tab.getAttribute('data-target')).classList.add('active');
      });
    });
  }

  // --- Real Backend Handlers ---
  // The center allocation dropdowns use the existing API, we ensure it's still attached dynamically
  document.addEventListener('change', (e) => {
    if (e.target.classList.contains('allocate-select')) {
      const select = e.target;
      const regId = select.getAttribute('data-reg-id');
      const center = select.value;
      const statusSpan = select.nextElementSibling;
      
      statusSpan.textContent = '⏳';
      
      // Preserve the existing logic which posts to /admin/allocate-center
      const API_BASE_URL = window.location.hostname === 'localhost' ? 'http://127.0.0.1:5000' : 'https://surya-s2f5.onrender.com';
      
      fetch(API_BASE_URL + '/admin/allocate-center', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/x-www-form-urlencoded',
          'Authorization': 'Basic YWRtaW46c3VyeWEyMDI1' 
        },
        body: `registration_id=${encodeURIComponent(regId)}&center=${encodeURIComponent(center)}`
      })
      .then(r => r.json())
      .then(res => {
        if(res.status === 'ok') {
          statusSpan.textContent = '✅';
          setTimeout(() => statusSpan.textContent = '', 2000);
        } else {
          statusSpan.textContent = '❌';
          alert('Allocation failed: ' + res.message);
        }
      })
      .catch(err => {
        statusSpan.textContent = '❌';
        alert('Error: ' + err);
      });
    }
  });

  // Bulk Selection Logic
  document.getElementById('select-all-rows')?.addEventListener('change', (e) => {
    const isChecked = e.target.checked;
    document.querySelectorAll('.row-select').forEach(cb => {
      cb.checked = isChecked;
    });
  });
});
