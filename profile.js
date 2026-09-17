/* Content-only enhancements: the original Framer motion/canvas runtime is untouched. */
(() => {
  const linkedin = 'https://www.linkedin.com/in/lea-irt-5a658329a/';
  const routes = {
    'dj-portfolio-website': 'druzabac',
    'meta-productivity-summit-2026': 'artist-classification',
    'fly-society': 'ai-spaceship-arena',
    'santander-mobile-for-teens': 'voterproof',
    'uup-festival': 'bomgerman',
  };
  const covers = {
    '7QT6pVQanEtNWsVA76U0vG7YBPA': ['BOARD / GAMES', 'druzabac'],
    'ga5uJgGS32FBzQ4Hs5ri0VqbEoc': ['ART / AI', 'artist-classification'],
    '2OUhedp1ZWdJChQhq3iWgjBoX2Y': ['SEARCH / SPACE', 'ai-spaceship-arena'],
    'ozy1vfUXwpro1HfvD14KQPalgk': ['DATA / PATTERNS', 'voterproof'],
    'p0QZS71mFctj7A3ACh5EI': ['PLAY / CREATE', 'bomgerman'],
    '7w139N0ZKy75rkl0Fe7swtT4oOE': ['LEA / IRT', 'portrait'],
    '6v6l202PxSixuk3wxIlNy6r9y4M': ['LEARN / SHARE', 'community'],
    'U6UaFG9JqPyGIzpz11hhkORyso': ['CODE / CREATE', 'community'],
    'B9hYtbmiMTkrQw0u4msBP5pazk': ['IDEAS / PEOPLE', 'community'],
  };
  document.addEventListener('click', event => {
    const anchor = event.target.closest('a');
    if (!anchor) return;
    const url = new URL(anchor.href, location.href);
    if (url.origin !== location.origin) return;
    const path = url.pathname.replace(/\/$/, '');
    const old = path.split('/').pop();
    const target = routes[old] ? '/work/' + routes[old] : ['/projects', '/playground'].includes(path) ? path : null;
    if (!target) return;
    // Use native links for personalized pages, bypassing the reference CMS router.
    event.stopImmediatePropagation();
    anchor.href = target;
    if (event.button === 0 && !event.metaKey && !event.ctrlKey && !event.shiftKey && !event.altKey) {
      event.preventDefault();
      location.assign(target);
    }
  }, true);
  // No message can be sent to the reference author's form endpoint.
  document.addEventListener('submit', event => {
    event.preventDefault();
    event.stopImmediatePropagation();
  }, true);
  function enhance() {
    document.querySelectorAll('img:not([data-profile-checked])').forEach(img => {
      img.dataset.profileChecked = 'true';
      const match = Object.entries(covers).find(([key]) => img.src.includes(key));
      const parent = img.parentElement;
      if (!parent || img.closest('nav, header')) return;
      parent.dataset.profileCover = match ? match[1][0] : 'IDEAS / IN MOTION';
      parent.dataset.profileProject = match ? match[1][1] : 'experiments';
      img.alt = '';
      img.setAttribute('aria-hidden', 'true');
    });
    document.querySelectorAll('video:not([data-profile-checked])').forEach(video => {
      video.dataset.profileChecked = 'true';
      if ((video.currentSrc || video.src).includes('gINlqya5HdnVsxd8Pwk3r7787Q')) return;
      video.pause();
      video.style.display = 'none';
    });
    document.querySelectorAll('form:not([data-profile-checked])').forEach(form => {
      form.dataset.profileChecked = 'true';
      form.hidden = true;
      const contact = document.createElement('a');
      contact.className = 'profile-contact';
      contact.href = linkedin;
      contact.target = '_blank';
      contact.rel = 'noopener noreferrer';
      contact.textContent = 'Connect on LinkedIn ↗';
      form.parentElement.append(contact);
    });
    for (const [selector, year] of [['.framer-14i2pnl-container', '2026'], ['.framer-jdvaec-container', '2028']]) {
      document.querySelectorAll(selector + ':not([data-profile-stat])').forEach(stat => {
        stat.dataset.profileStat = year;
        stat.setAttribute('aria-label', year);
        [...stat.children].forEach(child => child.setAttribute('aria-hidden', 'true'));
      });
    }
  }
  let queued = false;
  const observer = new MutationObserver(() => {
    if (queued) return;
    queued = true;
    requestAnimationFrame(() => { queued = false; enhance(); });
  });
  observer.observe(document.documentElement, {childList: true, subtree: true});
  enhance();
})();
