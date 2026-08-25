(function () {
  'use strict';

  /* ---------- Theme (dark default, honours system preference) ---------- */
  var root = document.documentElement;
  var toggle = document.querySelector('[data-theme-toggle]');
  var mode = 'dark'; /* obsidian is the brand default; toggle offers a light variant */
  root.setAttribute('data-theme', mode);

  var SUN =
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"/></svg>';
  var MOON =
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8z"/></svg>';

  function paintToggle() {
    if (!toggle) return;
    toggle.innerHTML = mode === 'dark' ? SUN : MOON;
    toggle.setAttribute('aria-label', 'Switch to ' + (mode === 'dark' ? 'light' : 'dark') + ' mode');
  }
  paintToggle();

  if (toggle) {
    toggle.addEventListener('click', function () {
      mode = mode === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', mode);
      paintToggle();
    });
  }

  /* ---------- Mobile nav ---------- */
  var navBtn = document.querySelector('[data-nav-toggle]');
  var nav = document.getElementById('primary-nav');
  var BARS =
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>';
  var CLOSE =
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 5l14 14M19 5L5 19"/></svg>';

  if (navBtn && nav) {
    navBtn.innerHTML = BARS;
    navBtn.addEventListener('click', function () {
      var open = nav.classList.toggle('nav--open');
      navBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      navBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      navBtn.innerHTML = open ? CLOSE : BARS;
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A' && nav.classList.contains('nav--open')) {
        nav.classList.remove('nav--open');
        navBtn.setAttribute('aria-expanded', 'false');
        navBtn.innerHTML = BARS;
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('nav--open')) navBtn.click();
    });
  }

  /* ---------- Sticky header state ---------- */
  var header = document.querySelector('.site-header');
  function onScroll() {
    if (header) header.setAttribute('data-scrolled', window.scrollY > 24 ? 'true' : 'false');
  }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---------- Scroll reveal ---------- */
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && reveals.length) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-in');
            io.unobserve(entry.target);
          }
        });
      },
      { rootMargin: '0px 0px -8% 0px', threshold: 0.08 }
    );
    reveals.forEach(function (el, i) {
      el.style.transitionDelay = (i % 4) * 70 + 'ms';
      io.observe(el);
    });
  } else {
    reveals.forEach(function (el) {
      el.classList.add('is-in');
    });
  }

  /* ---------- Count-up numerals ---------- */
  var counters = document.querySelectorAll('[data-count]');
  if ('IntersectionObserver' in window && counters.length) {
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var co = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var el = entry.target;
          co.unobserve(el);
          var target = parseFloat(el.getAttribute('data-count'));
          var prefix = el.getAttribute('data-prefix') || '';
          var suffix = el.getAttribute('data-suffix') || '';
          if (reduce) {
            el.textContent = prefix + target + suffix;
            return;
          }
          var start = performance.now();
          var dur = 1100;
          function tick(now) {
            var p = Math.min((now - start) / dur, 1);
            var eased = 1 - Math.pow(1 - p, 3);
            el.textContent = prefix + Math.round(target * eased).toLocaleString('en-US') + suffix;
            if (p < 1) requestAnimationFrame(tick);
          }
          el.textContent = prefix + '0' + suffix;
          requestAnimationFrame(tick);
        });
      },
      { threshold: 0.4 }
    );
    counters.forEach(function (el) {
      co.observe(el);
    });
  }
})();
