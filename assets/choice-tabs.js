/* Progressive enhancement: valid anchors and all panels remain readable without JS. */
(() => {
  'use strict';
  const groups = [];
  const root = document.documentElement;
  const decodeHash = (hash) => {
    try { return decodeURIComponent(hash.slice(1)); } catch (_) { return ''; }
  };
  const hashTarget = () => document.getElementById(decodeHash(location.hash));
  const disabled = (tab) => tab.getAttribute('aria-disabled') === 'true' || tab.disabled;

  function syncMedia(group) {
    group.panels.forEach((panel) => panel.querySelectorAll('video').forEach((video) => {
      if (panel.hidden) video.pause();
      else if (video.autoplay || video.hasAttribute('data-tab-autoplay')) {
        const playing = video.play();
        if (playing) playing.catch(() => {});
      }
    }));
  }

  function select(group, index) {
    if (!group.tabs[index] || disabled(group.tabs[index])) return;
    group.tabs.forEach((tab, i) => {
      tab.setAttribute('aria-selected', String(i === index));
      tab.tabIndex = i === index ? 0 : -1;
      group.panels[i].hidden = i !== index;
    });
    syncMedia(group);
  }

  function updateHash(id) {
    const hash = '#' + encodeURIComponent(id);
    if (location.hash !== hash) {
      try { history.pushState(null, '', hash); } catch (_) { /* Selection still works without history access. */ }
    }
  }

  document.querySelectorAll('[data-tabs]').forEach((element) => {
    const list = element.querySelector('[data-tab-list]');
    if (!list) return;
    const tabs = Array.from(list.querySelectorAll('[data-tab]'));
    const panels = tabs.map((tab) => document.getElementById(decodeHash(tab.getAttribute('href') || '')));
    if (tabs.length < 2 || panels.some((panel) => !panel || !element.contains(panel)) || new Set(panels).size !== panels.length) return;
    const group = { element, list, tabs, panels };
    tabs.forEach((tab, i) => {
      if (!tab.id) tab.id = 'choice-' + panels[i].id;
      tab.setAttribute('role', 'tab');
      tab.setAttribute('aria-controls', panels[i].id);
      panels[i].setAttribute('role', 'tabpanel');
      panels[i].setAttribute('aria-labelledby', tab.id);
      panels[i].tabIndex = 0;
      tab.addEventListener('click', (event) => {
        if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        if (disabled(tab)) return;
        select(group, i);
        updateHash(panels[i].id);
        tab.focus({ preventScroll: true });
      });
      tab.addEventListener('keydown', (event) => {
        const available = tabs.filter((item) => !disabled(item));
        const current = available.indexOf(tab);
        let next;
        if (event.key === 'ArrowRight') next = available[(current + 1) % available.length];
        if (event.key === 'ArrowLeft') next = available[(current - 1 + available.length) % available.length];
        if (event.key === 'Home') next = available[0];
        if (event.key === 'End') next = available[available.length - 1];
        if (next) {
          event.preventDefault();
          tabs.forEach((item) => { item.tabIndex = item === next ? 0 : -1; });
          next.focus({ preventScroll: true });
        } else if (event.key === ' ') {
          event.preventDefault();
          tab.click();
        }
      });
    });
    list.setAttribute('role', 'tablist');
    element.classList.add('choice-tabs-ready');
    const target = hashTarget();
    const initial = panels.findIndex((panel) => target && panel.contains(target));
    select(group, initial >= 0 && !disabled(tabs[initial]) ? initial : tabs.findIndex((tab) => !disabled(tab)));
    groups.push(group);
  });
  if (!groups.length) return;
  root.classList.add('choice-tabs-page');

  function measure() {
    const header = document.querySelector('body > header');
    const height = header ? Math.ceil(header.getBoundingClientRect().height) : 0;
    root.style.setProperty('--choice-header-height', height + 'px');
    root.style.setProperty('--choice-bar-height', Math.ceil(Math.max(...groups.map((group) => group.list.getBoundingClientRect().height))) + 'px');
  }
  measure();
  if ('ResizeObserver' in window) {
    const observer = new ResizeObserver(measure);
    const header = document.querySelector('body > header');
    if (header) observer.observe(header);
    groups.forEach((group) => observer.observe(group.list));
  }
  window.addEventListener('resize', measure, { passive: true });

  function reveal(target, scroll) {
    if (!target) return;
    groups.forEach((group) => {
      const index = group.panels.findIndex((panel) => panel.contains(target));
      if (index >= 0) select(group, index);
    });
    let ancestor = target;
    while (ancestor && ancestor !== document.body) {
      if (ancestor.tagName === 'DETAILS') ancestor.open = true;
      ancestor = ancestor.parentElement;
    }
    if (scroll) requestAnimationFrame(() => target.scrollIntoView({ block: 'start', behavior: 'instant' }));
  }
  const restore = () => reveal(hashTarget(), true);
  window.addEventListener('hashchange', restore);
  window.addEventListener('popstate', () => {
    if (location.hash) restore();
    else groups.forEach((group) => select(group, 0));
  });
  // Open hidden panels before following existing links, including nested #courses.
  document.addEventListener('click', (event) => {
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const link = event.target.closest('a[href]');
    if (!link || link.target === '_blank' || link.hasAttribute('download')) return;
    const url = new URL(link.href, location.href);
    if (url.origin !== location.origin || url.pathname !== location.pathname || url.search !== location.search || !url.hash) return;
    const target = document.getElementById(decodeHash(url.hash));
    if (!target || !groups.some((group) => group.element.contains(target))) return;
    event.preventDefault();
    updateHash(target.id);
    reveal(target, true);
  });
  if (location.hash) restore();
  window.addEventListener('load', () => { measure(); if (location.hash) restore(); });
})();
