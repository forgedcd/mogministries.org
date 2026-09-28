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

  // ================= Lightbox =================
  // Auto-attaches to any content image. Skips logos and small brand marks.
  var SKIP = /mog-logo|mog-shield|favicon/i;

  function bestSrc(img) {
    // Prefer the largest source in srcset if present, else the src.
    var ss = img.getAttribute('srcset');
    if (ss) {
      var best = null;
      var bestW = 0;
      ss.split(',').forEach(function (part) {
        var p = part.trim().split(/\s+/);
        var url = p[0];
        var w = parseInt((p[1] || '0').replace('w', ''), 10) || 0;
        if (w >= bestW) { bestW = w; best = url; }
      });
      if (best) return best;
    }
    return img.currentSrc || img.src;
  }

  var overlay = null;
  var overlayImg = null;
  var overlayCap = null;
  var lastFocus = null;

  function buildOverlay() {
    if (overlay) return;
    overlay = document.createElement('div');
    overlay.className = 'lightbox';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-label', 'Image viewer');
    overlay.innerHTML = ''
      + '<button class="lightbox__close" type="button" aria-label="Close">&times;</button>'
      + '<figure class="lightbox__figure">'
      +   '<img class="lightbox__img" alt="" />'
      +   '<figcaption class="lightbox__cap"></figcaption>'
      + '</figure>';
    document.body.appendChild(overlay);
    overlayImg = overlay.querySelector('.lightbox__img');
    overlayCap = overlay.querySelector('.lightbox__cap');

    overlay.addEventListener('click', function (e) {
      if (e.target === overlay || e.target.classList.contains('lightbox__close') || e.target.classList.contains('lightbox__figure')) {
        closeLightbox();
      }
    });
    document.addEventListener('keydown', function (e) {
      if (overlay.classList.contains('is-open') && (e.key === 'Escape' || e.key === 'Esc')) {
        closeLightbox();
      }
    });
  }

  function openLightbox(img) {
    buildOverlay();
    lastFocus = document.activeElement;
    overlayImg.src = bestSrc(img);
    overlayImg.alt = img.alt || '';
    var fig = img.closest('figure');
    var cap = fig ? fig.querySelector('figcaption') : null;
    overlayCap.textContent = cap ? cap.textContent.trim() : (img.alt || '');
    overlayCap.style.display = overlayCap.textContent ? '' : 'none';
    overlay.classList.add('is-open');
    document.documentElement.style.overflow = 'hidden';
    var closeBtn = overlay.querySelector('.lightbox__close');
    if (closeBtn) closeBtn.focus();
  }

  function closeLightbox() {
    if (!overlay) return;
    overlay.classList.remove('is-open');
    document.documentElement.style.overflow = '';
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  function attachImage(img) {
    if (img.dataset.lightboxBound === '1') return;
    var src = (img.getAttribute('src') || '') + ' ' + (img.getAttribute('srcset') || '');
    if (SKIP.test(src)) return;
    // Don't open lightboxes when the image is inside an anchor (e.g., audio-player card links).
    if (img.closest('a')) return;
    img.dataset.lightboxBound = '1';
    img.classList.add('is-zoomable');
    img.setAttribute('tabindex', '0');
    img.setAttribute('role', 'button');
    img.setAttribute('aria-label', (img.alt || 'Open image') + ' — tap to view full size');
    img.addEventListener('click', function () { openLightbox(img); });
    img.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openLightbox(img); }
    });
  }

  document.querySelectorAll('img').forEach(attachImage);
})();

// ================= Eulogy carousel + share =================
(function () {
  var track = document.querySelector('[data-eul-track]');
  if (track) {
    var slides = Array.prototype.slice.call(track.querySelectorAll('.eul-slide'));
    var cur = document.querySelector('[data-eul-cur]');
    var prev = document.querySelector('[data-eul-prev]');
    var next = document.querySelector('[data-eul-next]');
    var dotsWrap = document.querySelector('[data-eul-dots]');
    var idx = 0;
    var dots = slides.map(function (s, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('aria-label', 'Go to page ' + (i + 1));
      b.addEventListener('click', function () { go(i); });
      dotsWrap.appendChild(b);
      return b;
    });
    function go(i) {
      i = Math.max(0, Math.min(slides.length - 1, i));
      var s = slides[i];
      track.scrollTo({ left: s.offsetLeft - (track.clientWidth - s.clientWidth) / 2, behavior: 'smooth' });
    }
    function update() {
      var center = track.scrollLeft + track.clientWidth / 2;
      var best = 0, bestD = Infinity;
      slides.forEach(function (s, i) {
        var d = Math.abs(s.offsetLeft + s.clientWidth / 2 - center);
        if (d < bestD) { bestD = d; best = i; }
      });
      idx = best;
      cur.textContent = idx + 1;
      prev.disabled = idx === 0;
      next.disabled = idx === slides.length - 1;
      dots.forEach(function (d, i) { d.setAttribute('aria-current', i === idx ? 'true' : 'false'); });
    }
    var t;
    track.addEventListener('scroll', function () { clearTimeout(t); t = setTimeout(update, 60); }, { passive: true });
    prev.addEventListener('click', function () { go(idx - 1); });
    next.addEventListener('click', function () { go(idx + 1); });
    track.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); go(idx + 1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); go(idx - 1); }
    });
    window.addEventListener('resize', update);
    update();
  }

  var share = document.querySelector('[data-share]');
  if (share) {
    share.addEventListener('click', function () {
      var data = { title: 'A Eulogy From Behind the Walls', text: 'A handwritten testimony from a man serving two life sentences. Read what Jesus has done.', url: location.href.split('#')[0] };
      if (navigator.share) { navigator.share(data).catch(function () {}); return; }
      var done = function () { var o = share.textContent; share.textContent = 'Link copied'; setTimeout(function () { share.textContent = o; }, 2000); };
      if (navigator.clipboard) navigator.clipboard.writeText(data.url).then(done, function () { prompt('Copy this link:', data.url); });
      else prompt('Copy this link:', data.url);
    });
  }
})();
