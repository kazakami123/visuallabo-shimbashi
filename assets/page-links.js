/* Document navigation: native anchors keep every section and legal clause readable. */
(() => {
  'use strict';
  const root = document.documentElement;
  const lists = Array.from(document.querySelectorAll('[data-page-links]'));
  if (!lists.length) return;
  const header = document.querySelector('body > header');
  const decode = (hash) => { try { return decodeURIComponent(hash.slice(1)); } catch (_) { return ''; } };
  const links = lists.flatMap((list) => Array.from(list.querySelectorAll('a[href]')));
  function measure() {
    root.style.setProperty('--choice-header-height', (header ? Math.ceil(header.getBoundingClientRect().height) : 0) + 'px');
    root.style.setProperty('--choice-bar-height', Math.ceil(Math.max(...lists.map((list) => list.getBoundingClientRect().height))) + 'px');
  }
  function current() {
    links.forEach((link) => {
      const url = new URL(link.href, location.href);
      if (url.pathname === location.pathname && url.hash === location.hash && url.hash) link.setAttribute('aria-current', 'location');
      else if (!link.hasAttribute('data-current-page')) link.removeAttribute('aria-current');
    });
  }
  links.forEach((link) => link.addEventListener('click', (event) => {
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const url = new URL(link.href, location.href);
    if (url.origin !== location.origin || url.pathname !== location.pathname || url.search !== location.search || !url.hash) return;
    const target = document.getElementById(decode(url.hash));
    if (!target) return;
    event.preventDefault();
    if (location.hash !== url.hash) history.pushState(null, '', url.hash);
    target.scrollIntoView({ block: 'start', behavior: 'instant' });
    if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
    target.focus({ preventScroll: true });
    current();
  }));
  measure(); current();
  if ('ResizeObserver' in window) {
    const observer = new ResizeObserver(measure);
    if (header) observer.observe(header);
    lists.forEach((list) => observer.observe(list));
  }
  window.addEventListener('resize', measure, { passive: true });
  window.addEventListener('hashchange', current);
  window.addEventListener('popstate', current);
  window.addEventListener('load', measure);
})();
