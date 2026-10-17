/* All preview images and original documents are served from this site. */
document.querySelectorAll('.document-preview').forEach(viewer => {
  if (viewer.dataset.unit === 'page') return;
  const stage = viewer.querySelector('.document-stage');
  const pages = Array.from(stage.querySelectorAll('img'));
  const controls = viewer.querySelector('.document-controls');
  const previous = controls.querySelector('[data-step="-1"]');
  const next = controls.querySelector('[data-step="1"]');
  const counter = controls.querySelector('.document-count');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let index = 0;
  let animation;
  const update = () => {
    previous.disabled = index === 0;
    next.disabled = index === pages.length - 1;
    counter.textContent = `${index + 1} / ${pages.length}`;
    if (pages[index + 1]) pages[index + 1].loading = 'eager';
  };
  const show = step => {
    const target = Math.max(0, Math.min(pages.length - 1, index + step));
    if (target === index) return;
    if (animation) animation.cancel();
    pages[index].hidden = true;
    index = target;
    const page = pages[index];
    page.loading = 'eager';
    page.hidden = false;
    update();
    if (!reducedMotion.matches) {
      animation = page.animate([
        { opacity: 0, transform: `translateX(${step > 0 ? 18 : -18}px) rotateY(${step > 0 ? -7 : 7}deg)` },
        { opacity: 1, transform: 'translateX(0) rotateY(0)' }
      ], { duration: 320, easing: 'ease-out' });
    }
  };
  controls.hidden = false;
  controls.addEventListener('click', event => {
    const button = event.target.closest('button[data-step]');
    if (button) show(Number(button.dataset.step));
  });
  stage.addEventListener('keydown', event => {
    if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
      event.preventDefault();
      show(event.key === 'ArrowRight' ? 1 : -1);
    }
  });
  let start;
  stage.addEventListener('pointerdown', event => { start = { x: event.clientX, y: event.clientY }; });
  stage.addEventListener('pointerup', event => {
    if (!start) return;
    const dx = event.clientX - start.x;
    const dy = event.clientY - start.y;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) show(dx < 0 ? 1 : -1);
    start = null;
  });
  stage.addEventListener('pointercancel', () => { start = null; });
  update();
});
