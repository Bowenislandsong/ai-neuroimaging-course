document.addEventListener('DOMContentLoaded', () => {
  // 0. Reader Theme (Light / Sepia / Dark) & Focus Mode & Equation Breakdown Toggle
  const rootEl = document.documentElement;
  const themeBtn = document.getElementById('theme-cycle-btn');
  const themes = ['light', 'sepia', 'dark'];
  const themeLabels = { light: '☀ Light', sepia: '📖 Sepia', dark: '🌙 Dark' };
  let curTheme = localStorage.getItem('neuro_theme') || 'light';
  if (!themes.includes(curTheme)) curTheme = 'light';
  function applyTheme(t) {
    rootEl.setAttribute('data-theme', t);
    localStorage.setItem('neuro_theme', t);
    if (themeBtn) themeBtn.textContent = themeLabels[t];
  }
  applyTheme(curTheme);
  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      curTheme = themes[(themes.indexOf(curTheme) + 1) % themes.length];
      applyTheme(curTheme);
    });
  }

  const focusBtn = document.getElementById('focus-mode-btn');
  if (focusBtn) {
    const savedFocus = localStorage.getItem('neuro_focus_mode') === '1';
    if (savedFocus) {
      document.body.classList.add('focus-mode');
      focusBtn.classList.add('active');
    }
    focusBtn.addEventListener('click', () => {
      const on = document.body.classList.toggle('focus-mode');
      focusBtn.classList.toggle('active', on);
      localStorage.setItem('neuro_focus_mode', on ? '1' : '0');
    });
  }

  const eqToggleBtn = document.getElementById('eq-logic-toggle-btn');
  const eqDetails = document.querySelectorAll('details.equation-logic-details');
  if (eqToggleBtn) {
    let eqOpen = localStorage.getItem('neuro_eq_open') !== '0';
    function applyEqOpen(openState) {
      eqDetails.forEach(d => { d.open = openState; });
      eqToggleBtn.textContent = openState ? '∑ Logic: Expanded' : '∑ Logic: Compact';
      eqToggleBtn.classList.toggle('active', openState);
      localStorage.setItem('neuro_eq_open', openState ? '1' : '0');
    }
    if (eqDetails.length) {
      applyEqOpen(eqOpen);
    }
    eqToggleBtn.addEventListener('click', () => {
      eqOpen = !eqOpen;
      applyEqOpen(eqOpen);
    });
  }

  // 0b. Mobile Sidebar Drawer Toggle
  const mobileToggle = document.getElementById('mobile-nav-toggle');
  const sidebarLeftEl = document.querySelector('.sidebar-left');
  if (mobileToggle && sidebarLeftEl) {
    mobileToggle.addEventListener('click', () => {
      const open = sidebarLeftEl.classList.toggle('mobile-open');
      mobileToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      const hint = mobileToggle.querySelector('.mobile-toggle-hint');
      if (hint) hint.textContent = open ? 'Hide ▴' : 'Show ▾';
    });
  }

  // 1. Sidebar Mode Switcher (26-Week Study Path vs. By Strand vs. Repo Docs)
  const modeBtns = document.querySelectorAll('.sidebar-mode-btn');
  const navPanels = document.querySelectorAll('.sidebar-nav-panel');
  const savedMode = localStorage.getItem('neuro_nav_mode') || 'chronological';
  function setNavMode(mode) {
    modeBtns.forEach(b => b.classList.toggle('active', b.dataset.mode === mode));
    navPanels.forEach(p => { p.style.display = (p.dataset.panel === mode) ? 'block' : 'none'; });
    localStorage.setItem('neuro_nav_mode', mode);
  }
  if (modeBtns.length) {
    setNavMode(savedMode);
    modeBtns.forEach(b => b.addEventListener('click', () => setNavMode(b.dataset.mode)));
  }

  // 2. Sidebar Class & Document Filter (and '/' keyboard shortcut)
  const searchInput = document.getElementById('sidebar-filter-input');
  if (searchInput) {
    searchInput.addEventListener('input', () => {
      const q = searchInput.value.trim().toLowerCase();
      document.querySelectorAll('.nav-item').forEach(li => {
        const txt = li.textContent.toLowerCase();
        li.style.display = (!q || txt.includes(q)) ? '' : 'none';
      });
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === '/' && !['INPUT', 'TEXTAREA'].includes(document.activeElement?.tagName)) {
        e.preventDefault();
        const homeSearch = document.getElementById('roadmap-search');
        (homeSearch || searchInput).focus();
      }
    });
  }

  // 3. Copy Code Buttons
  document.querySelectorAll('.copy-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const pre = btn.closest('.code-block-wrap')?.querySelector('pre');
      if (!pre) return;
      navigator.clipboard.writeText(pre.innerText).then(() => {
        const orig = btn.textContent;
        btn.textContent = 'Copied!';
        setTimeout(() => { btn.textContent = orig; }, 1400);
      });
    });
  });

  // 4. Image Zoom Lightbox
  const overlay = document.getElementById('img-lightbox');
  const overlayImg = document.getElementById('img-lightbox-target');
  if (overlay && overlayImg) {
    document.querySelectorAll('.commons-figure img, .cell-output-figure img, .content-card img.zoomable-img').forEach(img => {
      img.addEventListener('click', () => {
        overlayImg.src = img.dataset.fullsrc || img.src;
        overlay.classList.add('open');
      });
    });
    overlay.addEventListener('click', () => overlay.classList.remove('open'));
  }

  // 5. Home Page & Materials Explorer Filter
  const filterPills = document.querySelectorAll('.filter-pill');
  const homeSearch = document.getElementById('roadmap-search');
  const classCards = document.querySelectorAll('.class-card');
  let activeStrand = 'ALL';
  function filterCatalog() {
    const q = (homeSearch ? homeSearch.value : '').trim().toLowerCase();
    classCards.forEach(card => {
      const strandMatch = (activeStrand === 'ALL') || (card.dataset.strand === activeStrand) || (card.dataset.phase === activeStrand);
      const textMatch = !q || card.textContent.toLowerCase().includes(q);
      card.style.display = (strandMatch && textMatch) ? 'flex' : 'none';
    });
  }
  filterPills.forEach(pill => {
    pill.addEventListener('click', () => {
      filterPills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      activeStrand = pill.dataset.filter;
      filterCatalog();
    });
  });
  if (homeSearch) homeSearch.addEventListener('input', filterCatalog);

  // 6. Scroll active sidebar item into view inside sidebar container only (never hijack window scroll)
  const activeNav = document.querySelector('.sidebar-left .nav-item a.current');
  if (activeNav && sidebarLeftEl) {
    sidebarLeftEl.scrollTop = Math.max(0, activeNav.offsetTop - sidebarLeftEl.clientHeight / 2);
  }
});
