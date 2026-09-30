(() => {
  const slides = [...document.querySelectorAll('.slide')];
  const range = document.querySelector('#slide-range');
  const current = document.querySelector('#slide-current');
  const previous = document.querySelector('#previous');
  const next = document.querySelector('#next');
  let index = Math.min(slides.length - 1, Math.max(0, (parseInt(location.hash.slice(1), 10) || 1) - 1));
  function show(value, updateHash = true) {
    index = Math.min(slides.length - 1, Math.max(0, value));
    slides.forEach((slide, i) => { slide.hidden = i !== index; });
    range.value = index + 1;
    current.textContent = `${index + 1} / ${slides.length}`;
    previous.disabled = index === 0;
    next.disabled = index === slides.length - 1;
    if (updateHash) history.replaceState(null, '', `#${index + 1}`);
    document.title = `${document.body.dataset.lesson} · ${index + 1}/${slides.length} · Lecture slides`;
  }
  previous.addEventListener('click', () => show(index - 1));
  next.addEventListener('click', () => show(index + 1));
  range.addEventListener('input', () => show(Number(range.value) - 1));
  window.addEventListener('hashchange', () => show((parseInt(location.hash.slice(1), 10) || 1) - 1, false));
  document.addEventListener('keydown', event => {
    if (/INPUT|BUTTON|SELECT|TEXTAREA/.test(event.target.tagName) || event.altKey || event.ctrlKey || event.metaKey) return;
    if (['ArrowRight', 'PageDown', ' '].includes(event.key)) { event.preventDefault(); show(index + 1); }
    if (['ArrowLeft', 'PageUp'].includes(event.key)) { event.preventDefault(); show(index - 1); }
    if (event.key === 'Home') { event.preventDefault(); show(0); }
    if (event.key === 'End') { event.preventDefault(); show(slides.length - 1); }
  });
  document.querySelector('#handout').addEventListener('click', event => {
    const active = document.body.classList.toggle('handout');
    event.target.setAttribute('aria-pressed', String(active));
    event.target.textContent = active ? 'Slide view' : 'Handout view';
  });
  document.querySelector('#print').addEventListener('click', () => window.print());
  document.querySelector('#fullscreen').addEventListener('click', async () => {
    try { if (document.fullscreenElement) await document.exitFullscreen(); else await document.documentElement.requestFullscreen(); } catch { /* Slide view remains usable when fullscreen is unavailable. */ }
  });
  show(index, false);
})();
