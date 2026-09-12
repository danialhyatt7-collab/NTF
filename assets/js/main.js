/* NTF — interactions & micro-animations */
(function () {
  'use strict';
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- theme ---------- */
  var root = document.documentElement;
  var toggle = document.querySelector('[data-theme-toggle]');
  function setTheme(t) {
    root.setAttribute('data-theme', t);
    try { localStorage.setItem('ntf-theme', t); } catch (e) {}
    if (toggle) toggle.setAttribute('aria-label', t === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
  }
  if (toggle) {
    toggle.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      if (document.startViewTransition && !reduced) { document.startViewTransition(function () { setTheme(next); }); }
      else { setTheme(next); }
    });
  }

  /* ---------- mobile nav ---------- */
  var burger = document.querySelector('.burger'), menu = document.querySelector('.menu');
  if (burger && menu) {
    burger.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      burger.setAttribute('aria-expanded', String(open));
      document.body.style.overflow = open ? 'hidden' : '';
    });
    menu.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        menu.classList.remove('open');
        burger.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      }
    });
  }

  /* ---------- header state + scroll progress + back to top ---------- */
  var header = document.querySelector('header.site');
  var bar = document.querySelector('.progress');
  var top = document.querySelector('.fab .top');
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle('scrolled', y > 8);
    if (bar) {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.transform = 'scaleX(' + (h > 0 ? Math.min(y / h, 1) : 0) + ')';
    }
    if (top) top.classList.toggle('show', y > 600);
  }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
  if (top) top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' }); });

  /* ---------- scroll reveals (rect sweep: reliable for clip-path elements) ---------- */
  var revealables = Array.prototype.slice.call(document.querySelectorAll('.reveal, .reveal-img'));
  revealables.forEach(function (el) {
    var idx = el.parentElement ? Array.prototype.indexOf.call(el.parentElement.children, el) : 0;
    el.style.transitionDelay = Math.min(idx, 5) * 80 + 'ms';
  });
  function sweep() {
    if (!revealables.length) return;
    var h = window.innerHeight || document.documentElement.clientHeight;
    revealables = revealables.filter(function (el) {
      if (reduced || el.getBoundingClientRect().top < h - 40) { el.classList.add('in'); return false; }
      return true;
    });
  }
  requestAnimationFrame(function () { requestAnimationFrame(sweep); });
  window.addEventListener('scroll', sweep, { passive: true });
  window.addEventListener('resize', sweep, { passive: true });
  window.addEventListener('load', sweep);

  /* ---------- lazy triggers (counters, meters) ---------- */
  var pending = [];
  function drain() { pending = pending.filter(function (fn) { return fn(); }); }
  window.addEventListener('scroll', drain, { passive: true });
  window.addEventListener('resize', drain, { passive: true });
  window.addEventListener('load', drain);
  requestAnimationFrame(function () { requestAnimationFrame(drain); });

  /* ---------- count up ---------- */
  document.querySelectorAll('[data-count]').forEach(function (el) {
    var target = parseFloat(el.dataset.count), suffix = el.dataset.suffix || '', dec = (el.dataset.dec | 0);
    var done = false;
    function run() {
      if (done) return; done = true;
      if (reduced) { el.textContent = target.toFixed(dec) + suffix; return; }
      var t0 = performance.now(), dur = 1500;
      (function step(t) {
        var p = Math.min((t - t0) / dur, 1);
        el.textContent = (target * (1 - Math.pow(1 - p, 3))).toFixed(dec) + suffix;
        if (p < 1) requestAnimationFrame(step);
      })(performance.now());
    }
    pending.push(function () {
      var r = el.getBoundingClientRect();
      if (r.top < (window.innerHeight || 800) - 20 && r.bottom > 0) { run(); return false; }
      return true;
    });
  });

  /* ---------- magnetic buttons ---------- */
  if (!reduced && window.matchMedia('(hover:hover)').matches) {
    document.querySelectorAll('[data-magnetic]').forEach(function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        var x = (e.clientX - r.left - r.width / 2) / r.width;
        var y = (e.clientY - r.top - r.height / 2) / r.height;
        el.style.transform = 'translate(' + (x * 7).toFixed(2) + 'px,' + (y * 7 - 2).toFixed(2) + 'px)';
      });
      el.addEventListener('pointerleave', function () { el.style.transform = ''; });
    });
  }

  /* ---------- hero parallax ---------- */
  var parallax = document.querySelectorAll('[data-parallax]');
  if (parallax.length && !reduced) {
    window.addEventListener('scroll', function () {
      var y = window.scrollY;
      parallax.forEach(function (el) {
        var s = parseFloat(el.dataset.parallax) || 0.05;
        el.style.transform = 'translate3d(0,' + (-y * s).toFixed(1) + 'px,0)';
      });
    }, { passive: true });
  }

  /* ---------- product gallery ---------- */
  var pdpMain = document.querySelector('[data-pdp-main]');
  if (pdpMain) {
    document.querySelectorAll('[data-pdp-thumb]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        document.querySelectorAll('[data-pdp-thumb]').forEach(function (b) { b.setAttribute('aria-selected', 'false'); });
        btn.setAttribute('aria-selected', 'true');
        pdpMain.style.opacity = '0';
        setTimeout(function () {
          pdpMain.src = btn.dataset.pdpThumb;
          pdpMain.alt = btn.dataset.alt || pdpMain.alt;
          pdpMain.style.opacity = '1';
        }, reduced ? 0 : 180);
      });
    });
  }

  /* ---------- quote form ---------- */
  var form = document.getElementById('quote-form');
  if (form) {
    var q = new URLSearchParams(location.search);
    var product = q.get('product'), category = q.get('category');
    var details = form.querySelector('[name=details]');
    if (product && details && !details.value) details.value = 'Product of interest: ' + product + '\n\n';
    if (category) {
      var sel = form.querySelector('[name=category]');
      if (sel) Array.prototype.forEach.call(sel.options, function (o) { if (o.value === category) sel.value = category; });
    }
    var validate = function (f) {
      var bad = !f.value.trim() || (f.type === 'email' && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.value));
      var slot = document.getElementById('err-' + f.name);
      if (slot) slot.textContent = bad ? (f.type === 'email' ? 'Enter a valid email address.' : 'This field is required.') : '';
      return !bad;
    };
    form.querySelectorAll('[required]').forEach(function (f) {
      f.addEventListener('blur', function () { validate(f); });
      f.addEventListener('input', function () {
        var slot = document.getElementById('err-' + f.name);
        if (slot && slot.textContent) validate(f);
      });
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true, first = null;
      form.querySelectorAll('[required]').forEach(function (f) {
        if (!validate(f)) { ok = false; if (!first) first = f; }
      });
      if (!ok) { first.focus(); return; }
      var data = {};
      new FormData(form).forEach(function (v, k) { data[k] = data[k] ? data[k] + ', ' + v : v; });
      var body = Object.keys(data).map(function (k) { return k.replace(/^\w/, function (c) { return c.toUpperCase(); }) + ': ' + data[k]; }).join('\n');
      var note = document.querySelector('.ok');
      if (note) { note.classList.add('show'); note.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'center' }); }
      window.location.href = 'mailto:support@ntf.com.pk'
        + '?subject=' + encodeURIComponent('Quote request - ' + (data.company || data.name || 'NTF'))
        + '&body=' + encodeURIComponent(body);
    });
  }

  /* ---------- meters ---------- */
  document.querySelectorAll('[data-meter]').forEach(function (el) {
    var fill = el.querySelector('.meter-fill'), pct = el.dataset.meter;
    if (!fill) return;
    if (reduced) { fill.style.width = pct + '%'; return; }
    pending.push(function () {
      var r = el.getBoundingClientRect();
      if (r.top < (window.innerHeight || 800) - 20 && r.bottom > 0) { fill.style.width = pct + '%'; return false; }
      return true;
    });
  });

  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();
