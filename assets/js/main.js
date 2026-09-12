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



  /* ---------- announcement bar ---------- */
  var announce = document.querySelector('[data-announce]');
  if (announce) {
    var items = announce.querySelectorAll('.announce-item');
    if (items.length > 1 && !reduced) {
      var at = 0, paused = false, timer;
      var advance = function () {
        if (paused) return;
        var current = items[at];
        at = (at + 1) % items.length;
        current.classList.remove('is-on');
        current.classList.add('is-out');
        items[at].classList.add('is-on');
        setTimeout(function () { current.classList.remove('is-out'); }, 500);
      };
      timer = setInterval(advance, 5200);
      announce.addEventListener('mouseenter', function () { paused = true; });
      announce.addEventListener('mouseleave', function () { paused = false; });
      announce.addEventListener('focusin', function () { paused = true; });
      announce.addEventListener('focusout', function () { paused = false; });
      document.addEventListener('visibilitychange', function () {
        paused = document.hidden;
      });
    }
  }

  /* ---------- mega panel ---------- */
  var mega = document.getElementById('mega-collections');
  var trigger = document.querySelector('.mega-trigger');
  if (mega && trigger) {
    var host = document.querySelector('header.site');
    var closeTimer;
    var desktop = function () { return window.matchMedia('(min-width:941px)').matches; };
    function openMega() {
      clearTimeout(closeTimer);
      if (!desktop()) return;
      mega.classList.add('open');
      trigger.setAttribute('aria-expanded', 'true');
    }
    function closeMega(delay) {
      clearTimeout(closeTimer);
      closeTimer = setTimeout(function () {
        mega.classList.remove('open');
        trigger.setAttribute('aria-expanded', 'false');
      }, delay || 0);
    }
    trigger.addEventListener('mouseenter', openMega);
    trigger.addEventListener('focus', openMega);
    mega.addEventListener('mouseenter', openMega);
    trigger.addEventListener('mouseleave', function () { closeMega(180); });
    mega.addEventListener('mouseleave', function () { closeMega(180); });
    host.addEventListener('focusout', function (e) {
      if (!host.contains(e.relatedTarget)) closeMega();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && mega.classList.contains('open')) { closeMega(); trigger.focus(); }
    });
    window.addEventListener('scroll', function () {
      if (mega.classList.contains('open')) closeMega();
    }, { passive: true });
  }

  /* ---------- search ---------- */
  var search = document.querySelector('[data-search]');
  if (search && window.NTF_INDEX) {
    var input = search.querySelector('[data-search-input]');
    var list = search.querySelector('[data-search-results]');
    var empty = search.querySelector('[data-search-empty]');
    var searchRoot = search.dataset.root || '';
    var cursor = -1;

    function esc(str) { return str.replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

    function highlight(text, q) {
      var i = text.toLowerCase().indexOf(q);
      if (q === '' || i < 0) return esc(text);
      return esc(text.slice(0, i)) + '<mark>' + esc(text.slice(i, i + q.length)) + '</mark>' + esc(text.slice(i + q.length));
    }

    function render(q) {
      var query = q.trim().toLowerCase();
      var hits = window.NTF_INDEX;
      if (query) {
        hits = hits.filter(function (it) { return it.k.indexOf(query) > -1; })
          .sort(function (a, b) {
            var ai = a.t.toLowerCase().indexOf(query), bi = b.t.toLowerCase().indexOf(query);
            return (ai < 0 ? 99 : ai) - (bi < 0 ? 99 : bi);
          });
      }
      hits = hits.slice(0, 8);
      cursor = -1;
      list.innerHTML = hits.map(function (it) {
        return '<li><a href="' + searchRoot + it.u + '"><span><b>' + highlight(it.t, query) +
               '</b></span><em>' + esc(it.s) + '</em></a></li>';
      }).join('');
      if (empty) empty.hidden = hits.length > 0;
    }

    function openSearch() {
      search.classList.add('open');
      document.body.classList.add('locked');
      render(input.value || '');
      setTimeout(function () { input.focus(); }, 60);
    }
    function closeSearch() {
      search.classList.remove('open');
      document.body.classList.remove('locked');
    }

    document.querySelectorAll('[data-search-open]').forEach(function (b) {
      b.addEventListener('click', openSearch);
    });
    search.querySelector('[data-search-close]').addEventListener('click', closeSearch);
    search.addEventListener('click', function (e) { if (e.target === search) closeSearch(); });
    input.addEventListener('input', function () { render(input.value); });

    document.addEventListener('keydown', function (e) {
      var isOpen = search.classList.contains('open');
      if ((e.key === '/' || (e.key === 'k' && (e.metaKey || e.ctrlKey))) && !isOpen) {
        var tag = (document.activeElement && document.activeElement.tagName) || '';
        if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;
        e.preventDefault(); openSearch(); return;
      }
      if (!isOpen) return;
      if (e.key === 'Escape') { closeSearch(); return; }
      var items = list.querySelectorAll('li');
      if (!items.length) return;
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        items[cursor] && items[cursor].classList.remove('on');
        cursor = e.key === 'ArrowDown'
          ? (cursor + 1) % items.length
          : (cursor - 1 + items.length) % items.length;
        items[cursor].classList.add('on');
        items[cursor].scrollIntoView({ block: 'nearest' });
      } else if (e.key === 'Enter' && cursor > -1) {
        e.preventDefault();
        items[cursor].querySelector('a').click();
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


  /* ---------- size + quantity pickers ---------- */
  function pickerState(scope) {
    var sizes = Array.prototype.slice.call(scope.querySelectorAll('.size[aria-pressed="true"]'))
      .map(function (b) { return b.dataset.size; });
    var input = scope.querySelector('.qty-input');
    var qty = input ? parseInt(input.value, 10) : NaN;
    return { sizes: sizes, qty: isNaN(qty) ? null : qty };
  }

  function syncPicker(scope) {
    var st = pickerState(scope);
    var cta = scope.querySelector('[data-quote-cta]');
    if (cta) {
      var q = new URLSearchParams();
      q.set('product', scope.dataset.product);
      q.set('category', scope.dataset.category);
      if (st.sizes.length) q.set('sizes', st.sizes.join(','));
      if (st.qty) q.set('qty', st.qty);
      cta.href = scope.dataset.quote + '?' + q.toString();
    }
    var summary = scope.querySelector('[data-picker-summary]');
    if (summary) {
      if (!st.sizes.length && !st.qty) {
        summary.textContent = 'Pick your sizes and quantity, and they travel with your quote request.';
      } else {
        var parts = [];
        parts.push(st.sizes.length ? st.sizes.join(', ') : 'all standard sizes');
        parts.push((st.qty || scope.dataset.moq) + ' pcs');
        summary.textContent = 'Quoting ' + parts.join(' \u00b7 ') + '.';
      }
    }
  }

  function clampQty(scope, flash) {
    var input = scope.querySelector('.qty-input');
    if (!input) return;
    var min = parseInt(input.min, 10) || 1;
    var v = parseInt(input.value, 10);
    if (isNaN(v) || v < min) {
      input.value = min;
      var hint = scope.querySelector('.qty-min');
      if (hint && flash && !reduced) {
        hint.classList.remove('flash');
        void hint.offsetWidth;
        hint.classList.add('flash');
      }
    }
  }

  document.querySelectorAll('[data-picker]').forEach(function (scope) {
    scope.addEventListener('click', function (e) {
      var size = e.target.closest('.size');
      if (size && !size.disabled) {
        e.preventDefault();
        size.setAttribute('aria-pressed', size.getAttribute('aria-pressed') === 'true' ? 'false' : 'true');
        syncPicker(scope);
        return;
      }
      var step = e.target.closest('.qty-step');
      if (step) {
        e.preventDefault();
        var input = scope.querySelector('.qty-input');
        if (!input) return;
        var min = parseInt(input.min, 10) || 1;
        var inc = parseInt(scope.dataset.stepSize, 10) || 1;
        var next = (parseInt(input.value, 10) || min) + parseInt(step.dataset.step, 10) * inc;
        input.value = Math.max(min, next);
        clampQty(scope, parseInt(step.dataset.step, 10) < 0);
        syncPicker(scope);
      }
    });
    var input = scope.querySelector('.qty-input');
    if (input) {
      input.addEventListener('input', function () { syncPicker(scope); });
      input.addEventListener('change', function () { clampQty(scope, true); syncPicker(scope); });
      input.addEventListener('blur', function () { clampQty(scope, true); syncPicker(scope); });
    }
    syncPicker(scope);
  });

  /* ---------- quote form ---------- */
  var form = document.getElementById('quote-form');
  if (form) {
    var q = new URLSearchParams(location.search);
    var product = q.get('product'), category = q.get('category');
    var sizes = q.get('sizes'), qty = q.get('qty');
    var details = form.querySelector('[name=details]');
    if (details && !details.value) {
      var lines = [];
      if (product) lines.push('Product of interest: ' + product);
      if (sizes) lines.push('Sizes: ' + sizes.split(',').join(', '));
      if (qty) lines.push('Quantity: ' + qty + ' pcs');
      if (lines.length) details.value = lines.join('\n') + '\n\n';
    }
    if (qty) {
      var qtyField = form.querySelector('[name=quantity]');
      if (qtyField && !qtyField.value) qtyField.value = qty;
    }
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
